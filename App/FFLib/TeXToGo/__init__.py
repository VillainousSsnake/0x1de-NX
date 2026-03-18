# /App/FFLib/TeXToGo/__init__.py
# Contains TexToGo Class
import io

# Importing modules
import App.FFLib.TeXToGo.TexToGo_base as txtgLib
from App.FFLib.TeXToGo.TexDataConvert import Converter
import os


# TexToGo controller
class TexToGo:
    """
    Controller for TextureToGo format (.txtg files)
    that can read, and write TexToGo files in bitmap data.
    """

    def __init__(self, file_path: os.PathLike | str) -> None:

        # Creating self variables
        self.file_path = file_path
        self.controller = txtgLib.TXTG()

        # Detecting if the path is real
        if not os.path.exists(file_path):
            raise FileExistsError("File path given doesn't point to a real file! File path: " + str(file_path))

        # Detecting if it has texture data
        with open(file_path, "rb") as f_in:
            buffer = io.BytesIO(f_in.read())
            if not self.controller.Identify(buffer):
                raise TypeError(
                    "File given does not contain correct texture data or might be corrupt! File path: " +
                    str(file_path)
                )

        # Getting height and width of the image
        self.controller.FilePath = self.file_path

        with open(self.file_path, "rb") as f_in:
            buffer = io.BytesIO(f_in.read())
            self.controller.Load(buffer)

        self.height = self.controller.Height
        self.width = self.controller.Width
        self.format = self.controller.Format

        print(self.height)
        print(self.width)
        print(self.format)

    def to_png(self, out_path):    # TODO: Finish

        self.controller.FilePath = self.file_path

        with open(self.file_path, "rb") as f_in:
            buffer = io.BytesIO(f_in.read())
            self.controller.Load(buffer)

        Converter.to_png(self, self.controller.GetImageData(), out_path)
        print("saved!")

        pass    # TODO: Stub
