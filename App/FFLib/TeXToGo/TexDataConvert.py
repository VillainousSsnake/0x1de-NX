
import numpy as np
from PIL import Image

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