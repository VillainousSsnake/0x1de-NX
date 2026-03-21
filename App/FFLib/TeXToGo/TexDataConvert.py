from PIL import Image
import texture2ddecoder


# noinspection PyPep8Naming
class BC1_UNORM:

    @staticmethod
    def bc1_to_png(data, width, height, out_path):
        # Decode BC1 to raw RGBA bytes
        rgba_bytes = texture2ddecoder.decode_bc1(data, width, height)

        # Create an image from RGBA bytes
        img = Image.frombytes("RGBA", (width, height), rgba_bytes)

        # Save as PNG
        img.save(out_path)
        print(f"Decoded texture saved to {out_path}")
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
        print("Detecting texture format...")
        match str(controller.format):

            case "TEX_FORMAT.BC1_UNORM":   # BC1 decoding
                print("bc1_unorm detected!")
                BC1_UNORM.bc1_to_png(data, width=256, height=256, out_path=out_path)

            case _:     # Throwing type error
                TypeError("Image isn't a valid texture format")
