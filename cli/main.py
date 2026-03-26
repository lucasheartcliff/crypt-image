#!/usr/bin/env python
# coding:UTF-8
"""crypt-image CLI

Usage:
  main.py encode -i <input> -o <output> -f <file> -k <key>
  main.py decode -i <input> -o <output> -k <key>

Options:
  -h, --help                Show this help
  -f,--file=<file>          File to hide
  -k,--key=<key>            Key to encrypt or decrypt file content
  -i,--in=<input>           Input image (carrier)
  -o,--out=<output>         Output image (or extracted file)
"""

import os
import sys

# Allow imports from project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import docopt
import cv2
from backend.app.core.cryptography import Cryptography, IntegrityError
from backend.app.core.steganography import Steganography


def print_progress(current: int, total: int) -> None:
    pct = (current / total) * 100
    bar = "=" * int(pct // 2) + ">" + " " * (50 - int(pct // 2))
    print(f"\r[{bar}] {pct:.1f}%", end="", flush=True)
    if current == total:
        print()


def main():
    args = docopt.docopt(__doc__)
    in_f = args["--in"]
    out_f = args["--out"]
    key_f = args["--key"]

    if not os.path.isfile(in_f):
        print(f"Error: Input file '{in_f}' not found.")
        sys.exit(1)
    if not os.path.isfile(key_f):
        print(f"Error: Key file '{key_f}' not found.")
        sys.exit(1)

    in_img = cv2.imread(in_f)
    if in_img is None:
        print(f"Error: Could not read image '{in_f}'.")
        sys.exit(1)

    with open(key_f, "r") as f:
        key = f.read().strip()

    crypto = Cryptography(key)
    steg = Steganography(in_img, crypto)
    lossy_formats = [".jpeg", ".jpg"]

    if args["encode"]:
        file_f = args["--file"]
        if not os.path.isfile(file_f):
            print(f"Error: File '{file_f}' not found.")
            sys.exit(1)

        stem, ext = os.path.splitext(out_f)
        if ext.lower() in lossy_formats:
            out_f = stem + ".png"
            print(f"Output file changed to {out_f} (lossy formats destroy hidden data)")

        with open(file_f, "rb") as f:
            data = f.read()

        capacity = steg.capacity_bytes()
        print(f"Image capacity: {capacity:,} bytes | Data size: {len(data):,} bytes")

        res = steg.encode_text(data.decode("utf-8"))
        cv2.imwrite(out_f, res)
        print(f"Data encoded successfully into {out_f}")

    elif args["decode"]:
        try:
            raw = steg.decode_text()
        except IntegrityError:
            print("Error: Decryption failed. Wrong key or corrupted data.")
            sys.exit(1)

        with open(out_f, "w") as f:
            f.write(raw)
        print(f"Data decoded successfully into {out_f}")


if __name__ == "__main__":
    main()
