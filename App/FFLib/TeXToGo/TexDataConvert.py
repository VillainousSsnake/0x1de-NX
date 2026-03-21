import io

import numpy as np
from PIL import Image
import struct
import texture2ddecoder


# Functions for classes
def rgb565_to_rgb888(c):
    r = (c >> 11) & 0x1F
    g = (c >> 5) & 0x3F
    b = c & 0x1F
    return (
        (r << 3) | (r >> 2),
        (g << 2) | (g >> 4),
        (b << 3) | (b >> 2)
    )


def decode_bc1_block(block):
    print(block)
    print(len(block))
    if len(block) > 8:  # TODO: Stub code
        return []


    c0, c1, bits = struct.unpack("<HHI", block)

    color0 = rgb565_to_rgb888(c0)
    color1 = rgb565_to_rgb888(c1)

    colors = [color0, color1]

    if c0 > c1:
        # 4-color mode
        colors.append(tuple((2*a + b) // 3 for a, b in zip(color0, color1)))
        colors.append(tuple((a + 2*b) // 3 for a, b in zip(color0, color1)))
    else:
        # 3-color mode + transparent
        colors.append(tuple((a + b) // 2 for a, b in zip(color0, color1)))
        colors.append((0, 0, 0, 0))

    out = []
    for i in range(16):
        idx = (bits >> (2 * i)) & 3
        col = colors[idx]
        if len(col) == 3:
            out.append((*col, 255))
        else:
            out.append(col)
    return out

# noinspection PyPep8Naming
class R8_UNORM:
    def to_r8(self, fp):


        # Load PNG
        img = Image.open(fp)

        # Convert to 8-bit grayscale (L mode)
        img = img.convert("L")

        # Extract raw R8_UNORM bytes
        r8_data = np.array(img, dtype=np.uint8).tobytes()

        return r8_data

    def to_png(self, data):
        raw = data

        # You MUST know the width and height
        width = 512  # TODO: Get height and width
        height = 512

        # Convert raw bytes → NumPy array → Pillow image
        arr = np.frombuffer(raw, dtype=np.uint8).reshape((height, width))
        img = Image.fromarray(arr, mode="L")

        # Save as PNG
        img.save("output.png")


# noinspection PyPep8Naming
class BC1_UNORM:

    @staticmethod
    def bc1_to_png(raw_bc1, width, height, out_path):
        img = Image.new("RGBA", (width, height))
        blocks_x = width // 4
        blocks_y = height // 4

        offset = 0
        for by in range(blocks_y):
            for bx in range(blocks_x):
                block = raw_bc1[offset:offset+8]
                offset += 8
                pixels = decode_bc1_block(block)

                for i, px in enumerate(pixels):
                    x = bx * 4 + (i % 4)
                    y = by * 4 + (i // 4)
                    img.putpixel((x, y), px)

        img.save(out_path)
        print("saved!")


class Converter:
    """
    This class contains functions to convert
    raw texture data to popular image formats
    like png, jpg, etc.
    """

    @staticmethod
    def to_png(controller, data, out_path):
        """
        takes image format and read-binary io stream and returns png data
        """
        print("entered")
        match str(controller.format):

            case "TEX_FORMAT.BC1_UNORM":   # BC1 decoding
                print("bc1_unorm detected!")
                BC1_UNORM.bc1_to_png(data, width=256, height=256, out_path=out_path)

            case _:     # Throwing type error
                TypeError("Image isn't a valid texture format")
