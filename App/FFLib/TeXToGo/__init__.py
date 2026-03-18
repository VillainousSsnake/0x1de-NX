# /App/FFLib/TeXToGo/__init__.py
# Contains TexToGo Class
import io

# Importing modules
import App.FFLib.TeXToGo.TexToGo_base as txtgLib
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
            if not self.controller.Identify(f_in):
                raise TypeError(
                    "File given does not contain correct texture data or might be corrupt! File path: " +
                    str(file_path)
                )

    def to_bitmap(self):

        self.controller.FilePath = self.file_path

        with open(self.file_path, "rb") as f_in:
            buffer = io.BytesIO(f_in.read())
            self.controller.Load(buffer)
            print(self.controller.GetImageData())


        pass    # TODO: Stub
