# Crypt Image

A script to encrypt text into a picture file using a secret key

[![wakatime](https://wakatime.com/badge/user/f1d329ab-b4f3-48bd-8ee8-20a2da432d3c/project/9d905800-e6b8-4480-a51e-fa573f119535.svg)](https://wakatime.com/badge/user/f1d329ab-b4f3-48bd-8ee8-20a2da432d3c/project/9d905800-e6b8-4480-a51e-fa573f119535)

## Requirements

`python 3.6.x`

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Encode Usage

```bash
python3 main.py encode -i <input> -o <output> -f <file> -k <key>
```

Example

```bash
python3 main.py encode -i example/th.jpeg -o output.jpg -f example/test_txt -k example/key.file
```

## Decode Usage

```bash
python3 main.py decode -i <input> -o <output> -k <key>
```

Example

```bash
python3  main.py decode -i output.png -o text_out.txt -k example/key.file
```
