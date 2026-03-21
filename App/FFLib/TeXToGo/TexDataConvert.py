
# Importing dependencies
from App.FFLib.TeXToGo import TexToGo_base
from App.FFLib.TotkZsDic import ZsDic
import texture2ddecoder
import py_tegra_swizzle
from PIL import Image
import math


def get_block_height(height):
    block_height = 16
    while block_height > 1 and (math.ceil(height / 8) < block_height):
        block_height >>= 1
    return block_height


def bc1_to_png(controller: TexToGo_base.TXTG, data, out_path):

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
    rgba_bytes = texture2ddecoder.decode_bc1(deswizzled_bytes, controller.Width, controller.Height)

    # Create an image from RGBA bytes
    img = Image.frombytes("RGBA", (controller.Width, controller.Height), rgba_bytes)

    # Save as PNG
    img.save(out_path, format="PNG")
    print(f"Decoded texture saved to {out_path}")
    print("saved!")


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
                print("bc1_unorm detected!")
                bc1_to_png(controller, data, out_path=out_path)

            case _:     # Throwing type error
                TypeError("Image isn't a valid texture format")

    @staticmethod
    def to_txtg(controller, file_in, out_path):
        pass    # TODO: Stub
