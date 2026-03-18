# /App/FFLib/TeXToGo/__init__.py
# Contains TexToGo Class

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

        # Detecting if the path is real
        if not os.path.exists(file_path):
            raise FileExistsError("File path given doesn't point to a real file! File path: " + str(file_path))

        # Detecting if it has texture data
        with open(file_path, "rb") as f_in:
            if not txtgLib.Identify(f_in):
                raise TypeError(
                    "File given does not contain correct texture data or might be corrupt! File path: " +
                    str(file_path)
                )

        pass    # TODO: Stub
