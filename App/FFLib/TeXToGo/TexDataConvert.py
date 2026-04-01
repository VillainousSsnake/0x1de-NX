# Importing dependencies
import pathlib

import zstandard
from App.FFLib.TeXToGo.TexToGo_base import *

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
import texfury


import struct


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

def encode_bc1(pil_image, alpha_cutoff=128):
    """
    Encode a Pillow RGBA image into BC1 (DXT1) compressed data (bytes).
    Handles any RGBA image, divides into 4x4 blocks, and encodes each block.
    Returns a bytes object containing BC1 blocks in row-major order.
    """
    # Ensure RGBA mode
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    width, height = pil_image.size
    pixels = pil_image.tobytes()
    stride = width * 4

    # Helper: Quantize 8-bit RGB to R5G6B5
    def rgb_to_565(r, g, b):
        r5 = (r * 31 + 127) // 255
        g6 = (g * 63 + 127) // 255
        b5 = (b * 31 + 127) // 255
        return (r5 << 11) | (g6 << 5) | b5

    # Helper: Expand R5G6B5 to 8-bit RGB
    def _565_to_rgb(c):
        r = (c >> 11) & 0x1F
        g = (c >> 5) & 0x3F
        b = c & 0x1F
        r8 = (r << 3) | (r >> 2)
        g8 = (g << 2) | (g >> 4)
        b8 = (b << 3) | (b >> 2)
        return (r8, g8, b8)

    # Helper: Interpolate between two colors
    def interp(c0, c1, w0, w1):
        return (
            (w0 * c0[0] + w1 * c1[0]) // (w0 + w1),
            (w0 * c0[1] + w1 * c1[1]) // (w0 + w1),
            (w0 * c0[2] + w1 * c1[2]) // (w0 + w1)
        )

    # Helper: Compute luminance for endpoint selection
    def luminance(rgb):
        return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]

    # Output buffer
    blocks = []

    # Process each 4x4 block
    for by in range(0, height, 4):
        for bx in range(0, width, 4):
            block_rgba = []
            has_alpha = False
            for y in range(4):
                py = min(by + y, height - 1)
                for x in range(4):
                    px = min(bx + x, width - 1)
                    idx = (py * width + px) * 4
                    r, g, b, a = pixels[idx:idx+4]
                    block_rgba.append((r, g, b, a))
                    if a < alpha_cutoff:
                        has_alpha = True

            # Endpoint selection: min/max luminance (fast heuristic)
            opaque_pixels = [c for c in block_rgba if c[3] >= alpha_cutoff]
            if opaque_pixels:
                min_c = max_c = opaque_pixels[0][:3]
                min_l = max_l = luminance(min_c)
                for c in opaque_pixels:
                    l = luminance(c[:3])
                    if l < min_l:
                        min_l = l
                        min_c = c[:3]
                    if l > max_l:
                        max_l = l
                        max_c = c[:3]
            else:
                # All transparent: use black
                min_c = max_c = (0, 0, 0)

            # Quantize endpoints to R5G6B5
            c0_565 = rgb_to_565(*max_c)
            c1_565 = rgb_to_565(*min_c)
            c0_rgb = _565_to_rgb(c0_565)
            c1_rgb = _565_to_rgb(c1_565)

            # Determine mode: 4-color (opaque) or 3-color (1-bit alpha)
            if has_alpha:
                # 3-color mode: c0_565 <= c1_565
                if c0_565 > c1_565:
                    c0_565, c1_565 = c1_565, c0_565
                    c0_rgb, c1_rgb = c1_rgb, c0_rgb
                palette = [
                    c0_rgb,
                    c1_rgb,
                    interp(c0_rgb, c1_rgb, 1, 1),
                    (0, 0, 0)  # Transparent
                ]
            else:
                # 4-color mode: c0_565 > c1_565
                if c0_565 <= c1_565:
                    c0_565, c1_565 = c1_565, c0_565
                    c0_rgb, c1_rgb = c1_rgb, c0_rgb
                palette = [
                    c0_rgb,
                    c1_rgb,
                    interp(c0_rgb, c1_rgb, 2, 1),
                    interp(c0_rgb, c1_rgb, 1, 2)
                ]

            # Assign indices
            indices = 0
            for i, (r, g, b, a) in enumerate(block_rgba):
                if has_alpha and a < alpha_cutoff:
                    idx = 3  # Transparent
                else:
                    # Find nearest palette color
                    min_err = float('inf')
                    idx = 0
                    for j in range(4):
                        pr, pg, pb = palette[j]
                        err = (int(r) - pr) ** 2 + (int(g) - pg) ** 2 + (int(b) - pb) ** 2
                        if err < min_err:
                            min_err = err
                            idx = j
                indices |= (idx & 0x3) << (2 * i)

            # Pack block: color0, color1, indices (little-endian)
            block = struct.pack('<HHI', c0_565, c1_565, indices)
            blocks.append(block)

    return b''.join(blocks)


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


def png_to_bc1(controller: TexToGo_base.TXTG, filepath_in, out_path):   # TODO: Fix

    # Storing input image to Texture container
    tex = texfury.Texture.from_image(
        source=pathlib.Path(filepath_in),
        format=texfury.BCFormat.BC1,
    )

    # Apply generic properties
    for k, v in TXTG.FormatList.items():
        if v == controller.Format:
            controller.HeaderInfo.Format = k
            break

    controller.HeaderInfo.Width = int(tex.width)
    controller.HeaderInfo.Height = int(tex.height)
    controller.HeaderInfo.Depth = int(controller.ArrayCount)
    controller.HeaderInfo.MipCount = int(tex.mip_count)

    with open(out_path, "wb") as stream:

        with FileWriter(stream) as writer:
            writer.WriteStruct(controller.HeaderInfo)
            writer.SeekBegin(controller.HeaderInfo.HeaderSize)

            surfaceSizes = []
            surfaceData = []

            for mip in range(controller.MipCount):
                for array in range(controller.ArrayCount):
                    writer.Write(array)  # ushort
                    writer.Write(mip)  # byte
                    writer.Write(1)  # byte

                    surface = Zstb.SCompress(controller.ImageList[array][mip], 20)
                    surfaceSizes.append(len(surface))
                    surfaceData.append(surface)

            for size in surfaceSizes:
                writer.Write(size)  # uint
                writer.Write(6)  # uint

            for data in surfaceData:
                writer.Write(data)



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


