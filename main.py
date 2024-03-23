#!/usr/bin/env python
# coding:UTF-8
"""main.py

Usage:
  main.py encode -i <input> -o <output> -f <file> -k <key>
  main.py decode -i <input> -o <output> -k <key>
  main.py generate_key -o <output>

Options:
  -h, --help                Show this help
  -f,--file=<file>          File to hide
  -k,--key=<key>            Key to encrypt or decrypt file content
  -i,--in=<input>           Input image (carrier)
  -o,--out=<output>         Output image (or extracted file)
"""

import docopt
import cv2
import logging
import os
from src.cryptography import Cryptography
from src.steganography import Steganography

# Configure logging
logging.basicConfig(filename="steganography.log", level=logging.INFO)


def generate_key_pair(output):
    private_key, public_key = Cryptography.generate_rsa_key_pair()
    key_file = output
    with open(key_file, "w") as f:
        f.write("PRIV_KEY:\n")
        f.write(private_key.decode("utf-8"))
        f.write("\nPUB_KEY:\n")
        f.write(public_key.decode("utf-8"))

    logging.info(f"Key pair saved to: {key_file}")


def read_key_file(key_file):
    if not os.path.isfile(key_file):
        logging.error(f"Key file {key_file} does not exist.")
        return None, None
    def concat(text:str, text2:str):
        if text is "":
            return text2
        else:
            return text+text2

    try:
        with open(key_file, "r") as f:
            lines = f.readlines()

        private_key = ""
        public_key = ""

        key_cursor =None

        for line in lines:
            if line.startswith("PRIV_KEY:"):
                key_cursor="private"
            elif line.startswith("PUB_KEY:"):
                key_cursor="public"
            else:
              if key_cursor is "public":
                  public_key += line
              else:
                  private_key += line

        print("\n\nPub:{}\n\n".format(public_key))
        print("\n\nPri:{}\n\n".format(private_key))
        if private_key is "" or public_key is "":
            logging.error("Private key or public key not found in the key file.")
            return None, None

        return private_key.encode("utf-8"), public_key.encode("utf-8")
    except Exception as e:
        logging.error(f"Error occurred while reading key file: {str(e)}")
        return None, None


def main():
    args = docopt.docopt(__doc__)
    in_f = args["--in"]
    out_f = args["--out"]
    key_f = args["--key"]

    if args["generate_key"]:
        generate_key_pair(out_f)
        return

    in_img = cv2.imread(in_f)

    private_key, public_key = read_key_file(key_f)
    crypto = Cryptography(private_key, public_key)
    steg = Steganography(in_img, crypto)
    lossy_formats = ["jpeg", "jpg"]

    if args["encode"]:
        # Handling lossy format
        out_f, out_ext = out_f.split(".")
        if out_ext in lossy_formats:
            out_f = out_f + ".png"
            print("Output file changed to ", out_f)

        data = open(args["--file"], "r").read()
        res = steg.encode_text(data)
        cv2.imwrite(out_f, res)
        logging.info("Text encoded successfully.")

    elif args["decode"]:
        raw = steg.decode_text()
        with open(out_f, "w") as f:
            f.write(raw)
        logging.info("Text decoded successfully.")


if __name__ == "__main__":
    main()
