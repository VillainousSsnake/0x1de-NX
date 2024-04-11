from App.FFLib.BinaryYAML.byml_base import Byml
import os


class BYML:
    def __init__(self, file_path: os.PathLike | str):   # TODO: Finish

        if not os.path.exists(file_path):
            raise FileExistsError("File path given doesn't point to a real file! File path: " + str(file_path))

        with open(file_path, "rb") as f_in:
            raw_data = f_in.read()

        self.byml_controller = Byml(raw_data)
