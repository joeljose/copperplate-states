"""The README gallery: for each highlighted state change, copy A | copy B aligned to A | overlay.

Overlay: dark = ink in both copies, red = ink only in copy A, cyan = ink only in copy B.
Crop centres are fractions of copy A's width and height; sizes are native pixels.
Run:  make figures
"""

import cv2
import numpy as np

from copperplate.compare import RESULTS, align, load, load_pairs

GALLERY = RESULTS / "gallery"

# name, pair, centre (x, y) as fractions of A, crop side in native px
HIGHLIGHTS = [
    ("ship", "K1-01", (0.815, 0.55), 900),
    ("coat_of_arms", "K7-27", (0.775, 0.655), 700),
    ("longitude_figures", "K4-13", (0.30, 0.19), 700),
    ("coordinate_grid", "K5-14", (0.15, 0.12), 900),
]


def triptych(A_pi: str, B_pi: str, centre: tuple[float, float], side: int) -> np.ndarray | None:
    A = load(A_pi)
    M = align(cv2.cvtColor(A, cv2.COLOR_BGR2GRAY), load(B_pi, cv2.IMREAD_GRAYSCALE))
    if M is None:
        return None
    H, W = A.shape[:2]
    x0 = int(np.clip(centre[0] * W - side / 2, 0, W - side))
    y0 = int(np.clip(centre[1] * H - side / 2, 0, H - side))
    a = A[y0 : y0 + side, x0 : x0 + side]
    Mc = M.copy()
    Mc[:, 2] -= (x0, y0)  # warp straight into the crop's frame
    b = cv2.warpAffine(load(B_pi), Mc, (side, side), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))

    # residual local shift left by paper shrinkage, by phase correlation on high-passed grey
    def hp(x):
        g = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY).astype(np.float32)
        return g - cv2.GaussianBlur(g, (0, 0), 8)

    (dx, dy), _ = cv2.phaseCorrelate(hp(b), hp(a), cv2.createHanningWindow((side, side), cv2.CV_32F))
    b = cv2.warpAffine(b, np.float32([[1, 0, dx], [0, 1, dy]]), (side, side), borderValue=(255, 255, 255))

    def norm(x):
        g = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY).astype(np.float32)
        lo, hi = np.percentile(g, [2, 98])
        return np.clip((g - lo) / max(hi - lo, 1e-6), 0, 1)

    na, nb = norm(a), norm(b)
    overlay = (np.dstack([na, na, nb]) * 255).astype(np.uint8)  # BGR: only-A ink -> red, only-B ink -> cyan
    gap = np.full((side, 12, 3), 255, np.uint8)
    return np.hstack([a, gap, b, gap, overlay])


def main() -> int:
    data = load_pairs()
    pairs = {p["id"]: p for p in data["pairs"]}
    GALLERY.mkdir(parents=True, exist_ok=True)
    for name, pid, centre, side in HIGHLIGHTS:
        p = pairs[pid]
        img = triptych(p["A"], p["B"], centre, side)
        if img is None:
            print(f"{name}: no common plate found")
            continue
        f = 1800 / img.shape[1]
        img = cv2.resize(img, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(GALLERY / f"{name}.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 85])
        print(f"{name:18} {pid}  {data['sheets'][p['A']]['shelfmark']} vs {data['sheets'][p['B']]['shelfmark']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
