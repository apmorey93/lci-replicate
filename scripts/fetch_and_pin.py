#!/usr/bin/env python3
import argparse, hashlib, json, os, re
from pathlib import Path
from urllib.request import urlopen

def sha256sum(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def fetch_to(url: str, dest: Path):
    if url.startswith(("http://","https://")):
        with urlopen(url) as r, open(dest, "wb") as f:
            f.write(r.read())
    else:
        src = Path(url); dest.write_bytes(src.read_bytes())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--checksums", required=True)
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    checks = Path(args.checksums); checks.parent.mkdir(parents=True, exist_ok=True)

    text = Path(args.sources).read_text(encoding="utf-8")
    jsonish = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', text).replace("'", '"')
    if not jsonish.strip().startswith("{"): jsonish = "{"+jsonish+"}"
    data = json.loads(jsonish)

    rows = []
    for item in data.get("items", []):
        url = item["url"]; dest = out_dir / item["out"]
        print(f">> Fetch: {url} -> {dest}")
        fetch_to(url, dest)
        rows.append((dest.name, sha256sum(dest)))

    with open(checks, "w", encoding="utf-8") as f:
        for name, h in rows:
            f.write(f"{h}  {name}\n")
    print(f"✓ Checksums -> {checks}")

if __name__ == "__main__":
    main()
