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

    def to_png(self, out_path):
        """
        Converting the TXTG file to PNG data and writing it to a file.
        """

        # Getting the file contents and loading the file controller
        with open(self.file_path, "rb") as f_in:
            buffer = io.BytesIO(f_in.read())
            self.controller.Load(buffer)

        # Converting the image to PNG format using the converter
        Converter.to_png(self.controller, self.controller.GetImageData(), out_path)

    def to_txtg(self, img_type, tex_format, filepath_in, out_path):

        Converter.to_txtg(self.controller, img_type, tex_format, filepath_in, out_path)

    def export_current_image(self):
        pass    # TODO: Stub
