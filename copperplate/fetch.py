"""Fetch the native-resolution scans named in data/pairs.json from the Allard Pierson IIIF server.

Scans are not redistributed with this repository; they are open access at the source.
Skips sheets already on disk, and stops after three HTTP 503s in a row (the server has outages).
Run:  make fetch
"""

import json
import pathlib
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMAGES = ROOT / "data" / "images"
UA = {"User-Agent": "copperplate-states (research; https://github.com/joeljose/copperplate-states)"}


def main(delay: float = 1.5) -> int:
    sheets = json.loads((ROOT / "data" / "pairs.json").read_text(encoding="utf-8"))["sheets"]
    IMAGES.mkdir(parents=True, exist_ok=True)
    todo = [pi for pi in sheets if not (IMAGES / f"{pi}.jpg").exists()]
    print(f"{len(sheets)} sheets, {len(sheets) - len(todo)} on disk, {len(todo)} to fetch")
    n503 = 0
    for i, pi in enumerate(todo, 1):
        url = f"{sheets[pi]['iiif']}/full/max/0/default.jpg"
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=600) as r:
                data = r.read()
        except urllib.error.HTTPError as e:
            n503 = n503 + 1 if e.code == 503 else 0
            print(f"[{i}/{len(todo)}] {pi}  HTTP {e.code}")
            if n503 >= 3:
                print("image server down (3 x 503); try again later")
                return 1
            continue
        n503 = 0
        (IMAGES / f"{pi}.jpg").write_bytes(data)
        print(f"[{i}/{len(todo)}] {pi}  {sheets[pi]['shelfmark']}  {len(data) / 1e6:.1f} MB", flush=True)
        time.sleep(delay)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
