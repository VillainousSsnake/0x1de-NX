# Importing dependencies
import zstandard

from App.FFLib.TeXToGo import TexToGo_base
from App.FFLib.TotkZsDic import ZsDic
from tkinter import messagebox
import texture2ddecoder
import py_tegra_swizzle
from PIL import Image
import numpy as np
import math
import os
import io


# Converter class
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
        print("Detecting texture format...")
        match str(controller.Format):

            case "TEX_FORMAT.BC1_UNORM":   # BC1 decoding
                print("BC1_UNORM detected!")
                bc1_to_png(controller, data, out_path)

            case "TEX_FORMAT.BC4_UNORM":  # BC4 decoding
                print("BC4_UNORM detected!")
                bc4_to_png(controller, data, out_path)

            case "TEX_FORMAT.BC5_UNORM":    # BC5 decoding
                print("BC5_UNORM detected!")

                # Not fully implemented message
                # TODO: Finish bc5 support then remove this
                if not messagebox.askyesno(
                        "Not Implemented Message",
                        "BC5_UNORM Format is not fully implemented, proceed?"):
                    return None

                bc5_to_png(controller, data, out_path)

            case "TEX_FORMAT.BC7_UNORM":
                print("BC4_UNORM detected!")
                bc7_to_png(controller, data, out_path)

            case _:     # Throwing type error
                TypeError("Image isn't a valid texture format")

    @staticmethod
    def to_txtg(controller: TexToGo_base.TXTG,
                img_type: str,
                tex_format: str,
                filepath_in: bytes,
                out_path: os.PathLike | str):
        """
        Converts regular image formats (eg. PNG, JPG) to TextureToGo format (eg. '.txtg')
        @param controller: TexToGo_Base.TXTG object
        @param img_type: Regular Image Format (Eg. 'PNG', etc.)
        @param tex_format: The compression used (Eg. 'TEX_FORMAT.BC1_UNORM', etc.)
        @param filepath_in: input png file path
        @param out_path: the path where the export file will be generated
        """
        # Matching input image type
        match img_type.lower():

            case "png":     # From png

                # Matching output texture format
                match tex_format.upper():

                    case "TEX_FORMAT.BC1_UNORM":  # Into BC1
                        print("bc1 detected!")
                        png_to_bc1(controller, filepath_in, out_path)

                    case _:     # Unsupported texture format
                        print("Unsupported convert INTO texture format: '" + tex_format + "'")

            case _:     # Unsupported image type
                print("Unsupported convert FROM image type: '" + img_type + "'")


"""
            |--------------------------------|
            | Functions for converter class: |
            |--------------------------------|
"""


def get_block_height(height):
    block_height = 16
    while block_height > 1 and (math.ceil(height / 8) < block_height):
        block_height >>= 1
    return block_height


def bc1_to_png(controller: TexToGo_base.TXTG, data, out_path):

    # Decompressing zstandard data
    data = ZsDic.auto_decompress_bytes(data)

    # Getting image data for de-swizzling
    block_width = max(1, controller.Width // 4)
    block_height_dim = max(1, controller.Height // 4)

    block_h = get_block_height(block_height_dim)

    # De-swizzling bytes
    deswizzled_bytes = py_tegra_swizzle.deswizzle_block_linear(
        width=block_width,
        height=block_height_dim,
        depth=controller.HeaderInfo.Depth,
        source=data,
        block_height=block_h,
        bytes_per_pixel=8,
    )

    # Decode BC1 to raw RGBA bytes
    rgba_bytes = texture2ddecoder.decode_bc1(deswizzled_bytes, controller.Width, controller.Height)

    # Create an image from RGBA bytes
    img = Image.frombytes("RGBA", (controller.Width, controller.Height), rgba_bytes)

    # Save as PNG
    img.save(out_path, format="PNG")


def png_to_bc1(controller: TexToGo_base.TXTG, filepath_in, out_path):

    pass    # TODO: Stub


def bc4_to_png(controller: TexToGo_base.TXTG, data, out_path):

    # Decompressing zstandard data
    data = ZsDic.auto_decompress_bytes(data)

    block_width = max(1, controller.Width // 4)
    block_height_dim = max(1, controller.Height // 4)

    block_h = get_block_height(block_height_dim)

    print(f"Data length: {len(data)}, Expected: {controller.Width * controller.Height // 2}")
    print(f"Block dims: {block_width}x{block_height_dim}, GOB block_height: {block_h}")

    deswizzled_bytes = py_tegra_swizzle.deswizzle_block_linear(
        width=block_width,
        height=block_height_dim,
        depth=controller.HeaderInfo.Depth,
        source=data,
        block_height=block_h,
        bytes_per_pixel=8,
    )

    # Decode BC1 to raw RGBA bytes
    rgba_bytes = texture2ddecoder.decode_bc4(deswizzled_bytes, controller.Width, controller.Height)

    # Create an image from RGBA bytes
    img = Image.frombytes("RGBA", (controller.Width, controller.Height), rgba_bytes)

    # Converting image to greyscale
    img = img.convert(mode="L")

    # Save as PNG
    img.save(out_path, format="PNG")
    print(f"Decoded texture saved to {out_path}")
    print("saved!")


def bc5_to_png(controller: TexToGo_base.TXTG, data, out_path):  # TODO: Fix this later

    # TODO: Add de-swizzling

    # Decompressing zstandard data
    data = ZsDic.auto_decompress_bytes(data)

    def decode_bc4_block(data):
        """Decode an 8-byte BC4 block into a 4x4 numpy array of uint8."""
        red0, red1 = data[0], data[1]
        # 48-bit index data (6 bytes)
        indices = int.from_bytes(data[2:8], byteorder='little')

        # Build the 8-entry lookup table
        lookup = [0] * 8
        lookup[0] = red0
        lookup[1] = red1
        if red0 > red1:
            for i in range(2, 8):
                lookup[i] = ((8 - i) * red0 + (i - 1) * red1) // 7
        else:
            for i in range(2, 6):
                lookup[i] = ((6 - i) * red0 + (i - 1) * red1) // 5
            lookup[6] = 0
            lookup[7] = 255

        # Decode 16 pixels (3 bits each)
        pixels = np.zeros((4, 4), dtype=np.uint8)
        for y in range(4):
            for x in range(4):
                idx = (indices >> (3 * (4 * y + x))) & 0x07
                pixels[y, x] = lookup[idx]

        return pixels

    def decode_bc5(data, width, height):
        """Decode BC5 compressed data into an RGBA numpy array."""
        blocks_x = (width + 3) // 4
        blocks_y = (height + 3) // 4
        img = np.zeros((height, width, 4), dtype=np.uint8)

        offset = 0
        for by in range(blocks_y):
            for bx in range(blocks_x):
                # Decode red channel
                red_block = decode_bc4_block(data[offset:offset + 8])
                offset += 8
                # Decode green channel
                green_block = decode_bc4_block(data[offset:offset + 8])
                offset += 8

                # Place into image
                for y in range(4):
                    for x in range(4):
                        px = bx * 4 + x
                        py = by * 4 + y
                        if px < width and py < height:
                            r = red_block[y, x]
                            g = green_block[y, x]
                            # If BC5 is a normal map, reconstruct B
                            nx = (r / 255.0) * 2 - 1
                            ny = (g / 255.0) * 2 - 1
                            nz = (1.0 - min(1.0, nx * nx + ny * ny)) ** 0.5
                            b = int((nz * 0.5 + 0.5) * 255)
                            img[py, px] = [r, g, b, 255]

        return img

    # Save as PNG
    image = decode_bc5(data, controller.Width, controller.Height)

    # Save as PNG (requires Pillow)
    Image.fromarray(image, 'RGBA').save(out_path)

    print(f"Decoded texture saved to {out_path}")
    print("saved!")


def bc7_to_png(controller: TexToGo_base.TXTG, data, out_path):
    # TODO: Test and review

    # Decompressing zstandard data
    data = ZsDic.auto_decompress_bytes(data)

    # Getting image data for de-swizzling
    block_width = max(1, controller.Width // 4)
    block_height_dim = max(1, controller.Height // 4)

    block_h = get_block_height(block_height_dim)

    # De-swizzling bytes
    deswizzled_bytes = py_tegra_swizzle.deswizzle_block_linear(
        width=block_width,
        height=block_height_dim,
        depth=controller.HeaderInfo.Depth,
        source=data,
        block_height=block_h,
        bytes_per_pixel=8,
    )

    # Decode BC1 to raw RGBA bytes
    rgba_bytes = texture2ddecoder.decode_bc7(deswizzled_bytes, controller.Width, controller.Height)

    # Create an image from RGBA bytes
    img = Image.frombytes("RGBA", (controller.Width, controller.Height), rgba_bytes)

    # Save as PNG
    img.save(out_path, format="PNG")


