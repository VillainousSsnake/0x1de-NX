
# Importing dependencies
from PIL import Image
import texture2ddecoder
import py_tegra_swizzle
from App.FFLib.TeXToGo import TexToGo_base
import math


def get_block_height(height):
    block_height = 16
    while block_height > 1 and (math.ceil(height / 8) < block_height):
        block_height >>= 1
    return block_height


# To Png functions
def bc1_to_png(controller: TexToGo_base.TXTG, data, out_path):

    # Getting block height
    block_h = get_block_height(math.ceil(controller.Height / 4))

    # Deswizzling bytes
    deswizzled_bytes = py_tegra_swizzle.deswizzle_block_linear(
        width=controller.Width,
        height=controller.Height,
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
    img.save(out_path)
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
