"""Compare two impressions of one copper plate and mark where the engraving differs.

Four steps, each borrowed from a field that already compares two copies of the same thing
(sources in docs/method.md):

  1. ink layer   thin dark line work only: black-hat of max(R, G, B), divided by the local paper level.
                 Watercolour leaves one channel high, so max(R, G, B) ignores it; broad paint is wider than
                 the black-hat kernel, so it drops out too.                          (pathology stain separation)
  2. alignment   SIFT + RANSAC similarity transform, then a dense DIS optical flow smoothed with an
                 ink-weighted Gaussian of sigma ~120 native px. That absorbs uneven paper shrinkage but is
                 far too wide to bend around a numeral.                        (stamp plating: per-cell offsets)
  3. photometry  per-tile gain fitted only on strokes present in both copies, so a paler impression matches
                 a darker one without a genuinely different tile rescaling the other.   (astronomy subtraction)
  4. difference  ink in one copy where the other has under 30% of that strength within ~8 px.
                 Wear fades a line to about half; an alteration or proof state removes it. (print inspection)

Writes results/<pair>.json (regions, native pixel boxes) and results/<pair>.jpg (the sheet, red = ink only
in copy A, cyan = ink only in copy B, green boxes = largest regions).
Run:  make compare            all pairs
      make compare PAIR=K1-01 one pair
"""

import argparse
import json
import pathlib

import cv2
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMAGES = ROOT / "data" / "images"
RESULTS = ROOT / "results"

S = 0.5  # working scale
FLOW_SIGMA = 60  # px at working scale (~120 native): wider than any numeral, so it cannot bend to one
TILE = 256  # gain tiles
T_INK = 0.35  # ink threshold
RATIO = 0.3  # "absent": the other copy has under 30% of this ink strength nearby
R_TOL = 4  # tolerance radius, px at working scale (~8 native)
MIN_AREA = 40  # smallest region kept, px at working scale
BORDER = 24  # margin of the common area that is ignored


def load_pairs() -> dict:
    return json.loads((ROOT / "data" / "pairs.json").read_text(encoding="utf-8"))


def load(pi: str, flags: int = cv2.IMREAD_COLOR) -> np.ndarray:
    img = cv2.imread(str(IMAGES / f"{pi}.jpg"), flags)
    if img is None:
        raise FileNotFoundError(f"{pi}.jpg not in data/images; run `make fetch`")
    return img


def align(a_gray: np.ndarray, b_gray: np.ndarray) -> np.ndarray | None:
    """2x3 similarity transform taking B's native pixels to A's, or None if the sheets share no plate.

    SIFT on high-passed images at a 1600 px long edge (the high-pass removes paper tone and colour), ratio test
    0.75, RANSAC with a 3 px threshold, at least 20 inliers.
    """

    def small(img):
        s = 1600 / max(img.shape)
        f = cv2.resize(img, None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32)
        hp = f - cv2.GaussianBlur(f, (0, 0), 8.0 * s)
        return np.clip(hp / (4 * (hp.std() or 1)) * 127 + 128, 0, 255).astype(np.uint8), s

    (ha, sa), (hb, sb) = small(a_gray), small(b_gray)
    sift = cv2.SIFT_create()
    ka, da = sift.detectAndCompute(ha, None)
    kb, db = sift.detectAndCompute(hb, None)
    if da is None or db is None:
        return None
    good = [
        m
        for m, n in (p for p in cv2.BFMatcher().knnMatch(db, da, k=2) if len(p) == 2)
        if m.distance < 0.75 * n.distance
    ]
    if len(good) < 20:
        return None
    src = np.float32([kb[m.queryIdx].pt for m in good])
    dst = np.float32([ka[m.trainIdx].pt for m in good])
    M, inl = cv2.estimateAffinePartial2D(
        src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0, maxIters=5000, confidence=0.999
    )
    if M is None or int(inl.sum()) < 20:
        return None
    M[:, :2] *= sb / sa  # small frames -> native frames
    M[:, 2] /= sa
    return M


def ink_layer(bgr: np.ndarray) -> np.ndarray:
    mx = bgr.max(axis=2).astype(np.float32)
    closed = cv2.morphologyEx(mx, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    # ponytail: solid engraved fills wider than the kernel (~30 native px) are lost; fine for line engraving.
    return np.clip((closed - mx) / np.maximum(closed, 1.0), 0.0, 1.0)


def gain_field(a: np.ndarray, b: np.ndarray, valid: np.ndarray) -> np.ndarray:
    h, w = a.shape
    gy, gx = -(-h // TILE), -(-w // TILE)
    g = np.ones((gy, gx), np.float32)
    both = valid & (a > T_INK) & (b > T_INK / 2)
    for j in range(gy):
        for i in range(gx):
            sl = np.s_[j * TILE : (j + 1) * TILE, i * TILE : (i + 1) * TILE]
            m = both[sl]
            if m.sum() >= 200:
                g[j, i] = np.clip(np.median(a[sl][m] / b[sl][m]), 0.5, 4.0)
    return cv2.resize(g, (w, h), interpolation=cv2.INTER_LINEAR)


def compare(A_pi: str, B_pi: str) -> tuple[dict, np.ndarray, np.ndarray, np.ndarray]:
    """Returns (record, A at working scale, ink only in A, ink only in B)."""
    M = align(load(A_pi, cv2.IMREAD_GRAYSCALE), load(B_pi, cv2.IMREAD_GRAYSCALE))
    if M is None:
        return {"same_plate": False}, None, None, None
    Ms = M.copy()
    Ms[:, 2] *= S

    def half(pi):
        return cv2.resize(load(pi), None, fx=S, fy=S, interpolation=cv2.INTER_AREA)

    Ac, Bc = half(A_pi), half(B_pi)
    h, w = Ac.shape[:2]
    a = ink_layer(Ac)
    b = cv2.warpAffine(ink_layer(Bc), Ms, (w, h), flags=cv2.INTER_LINEAR, borderValue=-1)
    valid = b >= 0
    b = np.clip(b, 0, 1)

    flow = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM).calc(
        (a * 255).astype(np.uint8), (b * 255).astype(np.uint8), None
    )
    wgt = cv2.GaussianBlur(a, (0, 0), 3)
    wb = cv2.GaussianBlur(wgt, (0, 0), FLOW_SIGMA) + 1e-6
    flow = np.dstack([cv2.GaussianBlur(flow[..., i] * wgt, (0, 0), FLOW_SIGMA) / wb for i in (0, 1)])
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    mx, my = gx + flow[..., 0], gy + flow[..., 1]
    b = cv2.remap(b, mx, my, cv2.INTER_LINEAR)
    valid &= cv2.remap(valid.astype(np.uint8), mx, my, cv2.INTER_NEAREST).astype(bool)
    valid = cv2.erode(valid.astype(np.uint8), np.ones((2 * BORDER + 1,) * 2, np.uint8)).astype(bool)

    a, b = cv2.GaussianBlur(a, (0, 0), 1.0), cv2.GaussianBlur(b, (0, 0), 1.0)
    b = b * gain_field(a, b, valid)

    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * R_TOL + 1,) * 2)
    op = np.ones((3, 3), np.uint8)
    only_a = cv2.morphologyEx(
        ((a > T_INK) & (cv2.dilate(b, k) < RATIO * a) & valid).astype(np.uint8), cv2.MORPH_OPEN, op
    )
    only_b = cv2.morphologyEx(
        ((b > T_INK) & (cv2.dilate(a, k) < RATIO * b) & valid).astype(np.uint8), cv2.MORPH_OPEN, op
    )

    regions = []
    for side, m in (("A", only_a), ("B", only_b)):
        # strokes of one alteration are grouped: gaps up to ~10 px close before labelling
        n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m, np.ones((21, 21), np.uint8)), 8)
        for i in range(1, n):
            ink = int(m[lab == i].sum())
            if ink >= MIN_AREA:
                regions.append({"only_in": side, "ink_px": ink, "box": [int(v / S) for v in st[i, :4]]})
    regions.sort(key=lambda r: -r["ink_px"])

    ink_a = int(((a > T_INK) & valid).sum())
    rec = {
        "same_plate": True,
        "scale": round(float(np.sqrt(abs(np.linalg.det(M[:, :2])))), 5),
        "changed_share_of_ink": round(int(only_a.sum() + only_b.sum()) / max(ink_a, 1), 5),
        "n_regions": len(regions),
        "regions": regions,
        "transform_B_to_A": M.round(5).tolist(),
    }
    return rec, Ac, only_a, only_b


def render(path: pathlib.Path, title: str, Ac, only_a, only_b, regions) -> None:
    g = cv2.cvtColor(cv2.cvtColor(Ac, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    g = (g * 0.55 + 110).astype(np.uint8)
    d = np.ones((5, 5), np.uint8)
    g[cv2.dilate(only_a, d) > 0] = (0, 0, 230)  # red: ink only in A
    g[cv2.dilate(only_b, d) > 0] = (220, 200, 0)  # cyan: ink only in B
    for r in regions[:15]:
        x, y, bw, bh = (int(v * S) for v in r["box"])
        cv2.rectangle(g, (x - 8, y - 8), (x + bw + 8, y + bh + 8), (0, 160, 0), 4)
    f = 1600 / g.shape[1]
    g = cv2.resize(g, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    cv2.putText(g, title, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.imwrite(str(path), g, [cv2.IMWRITE_JPEG_QUALITY, 80])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", action="append", help="pair id, e.g. K1-01 (default: all)")
    args = ap.parse_args()
    data = load_pairs()
    RESULTS.mkdir(exist_ok=True)
    for p in data["pairs"]:
        if args.pair and p["id"] not in args.pair:
            continue
        sa, sb = data["sheets"][p["A"]], data["sheets"][p["B"]]
        rec, Ac, only_a, only_b = compare(p["A"], p["B"])
        rec = {
            "pair": p["id"],
            "family": p["family"],
            "A": p["A"],
            "B": p["B"],
            "A_shelfmark": sa["shelfmark"],
            "B_shelfmark": sb["shelfmark"],
            **rec,
        }
        (RESULTS / f"{p['id']}.json").write_text(json.dumps(rec, indent=1))
        if rec["same_plate"]:
            render(
                RESULTS / f"{p['id']}.jpg",
                f"{p['id']}  A = {sa['shelfmark']}  B = {sb['shelfmark']}   red = only in A, cyan = only in B",
                Ac,
                only_a,
                only_b,
                rec["regions"],
            )
        print(
            f"{p['id']:6}  same_plate={rec['same_plate']}  changed={rec.get('changed_share_of_ink', 0):.3%}  "
            f"regions={rec.get('n_regions', 0)}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
