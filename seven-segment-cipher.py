import json
from argparse import ArgumentParser

from PIL import Image, ImageDraw

height = 60
parser = ArgumentParser(
    prog="seven_segment_cipher",
    description="Encrypt/Decrypt the seven segment cipher",
)

operation = parser.add_mutually_exclusive_group(required=True)
output = parser.add_mutually_exclusive_group(required=True)
operation.add_argument("-e", "--encrypt")
operation.add_argument("-d", "--decrypt", nargs="?", const="dummy value")
output.add_argument("--graphic", nargs="?", const="encrypted.png")
output.add_argument("--binary", action="store_true")
args = parser.parse_args()


def main():
    if args.encrypt:
        if args.graphic:
            encrypt_graphic(args.encrypt)
        elif args.binary:
            encrypt_binary(args.encrypt)
    elif args.decrypt:
        if args.binary:
            decrypt_binary(args.decrypt)
        elif args.graphic:
            decrypt_graphic(args.graphic)


def decrypt_binary(cipher):
    with open("binary-map.json") as raw_json:
        bin_map = json.load(raw_json)
    cipher_map = cipher.split(" ")
    for c in cipher_map:
        print([key for key, value in bin_map.items() if value == c][0], end="")
    print()


def decrypt_graphic(cipher_file):
    with open("color-map.json") as raw_json:
        color_map = json.load(raw_json)
    im = Image.open(cipher_file)
    pixels = list(im.getdata())
    width, _ = im.size
    pixels = [pixels[i * width : (i + 1) * width] for i in range(height)]
    for y in range(10, width, 20):
        print(
            [
                key
                for key, value in color_map.items()
                if value
                == {
                    "top": list(pixels[0][y]),
                    "middle": list(pixels[29][y]),
                    "bottom": list(pixels[59][y]),
                }
            ][0],
            end="",
        )
    print()


def draw_character(draw, x, color):
    draw.rectangle((x, 0, x + 20, 20), fill=tuple(color["top"]))
    draw.rectangle((x, 20, x + 20, 40), fill=tuple(color["middle"]))
    draw.rectangle((x, 40, x + 20, 60), fill=tuple(color["bottom"]))


def encrypt_binary(message):
    with open("binary-map.json") as raw_json:
        bin_map = json.load(raw_json)
    for m in message:
        print(bin_map[m.lower()], end=" ")
    print()


def encrypt_graphic(message):
    with open("color-map.json") as raw_json:
        color_map = json.load(raw_json)
    width = 20 * len(message)
    img = Image.new(mode="RGB", size=(width, height))
    draw = ImageDraw.Draw(img)
    for idx, m in enumerate(message):
        draw_character(draw, idx * 20, color_map[m.lower()])
    img.save(args.graphic)


if __name__ == "__main__":
    main()
