"""!/usr/bin/env python
coding:UTF-8

Usage:
  main.py encode -i <input> -o <output> -f <file>
  main.py decode -i <input> -o <output>

Options:
  -h, --help                Show this help
  --version                 Show the version
  -f,--file=<file>          File to hide
  -i,--in=<input>           Input image (carrier)
  -o,--out=<output>         Output image (or extracted file)
"""

import docopt
import cv2
from src.steganography import Steganography


def main():
    args = docopt.docopt(__doc__)
    in_f = args["--in"]
    out_f = args["--out"]
    in_img = cv2.imread(in_f)
    steg = Steganography(in_img)
    lossy_formats = ["jpeg", "jpg"]

    if args['encode']:
        # Handling lossy format
        out_f, out_ext = out_f.split(".")
        if out_ext in lossy_formats:
            out_f = out_f + ".png"
            print("Output file changed to ", out_f)

        data = open(args["--file"], "rb").read()
        res = steg.encode_binary(data)
        cv2.imwrite(out_f, res)

    elif args["decode"]:
        raw = steg.decode_binary()
        with open(out_f, "wb") as f:
            f.write(raw)


if __name__ == "__main__":
    main()
