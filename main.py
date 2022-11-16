#!/usr/bin/env python
# coding:UTF-8
"""main.py

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

import docopt
import cv2
from src.cryptography import Cryptography
from src.steganography import Steganography

def main():
    args = docopt.docopt(__doc__)
    in_f = args["--in"]
    out_f = args["--out"]
    key_f = args["--key"]

    
    in_img = cv2.imread(in_f)
    
    key = open(key_f, "r").read()
    crypto = Cryptography(key)
    steg = Steganography(in_img, crypto)
    lossy_formats = ["jpeg", "jpg"]

    if args['encode']:
        # Handling lossy format
        out_f, out_ext = out_f.split(".")
        if out_ext in lossy_formats:
            out_f = out_f + ".png"
            print("Output file changed to ", out_f)

        data = open(args["--file"], "r").read()
        res = steg.encode_text(data)    
        cv2.imwrite(out_f, res)

    elif args["decode"]:
        raw = steg.decode_text()
        with open(out_f, "w") as f:
            f.write(raw)


if __name__ == "__main__":
    main()
