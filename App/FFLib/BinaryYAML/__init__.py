from App.FFLib.BinaryYAML.byml_base import Byml
import os


class BYML:
    def __init__(self, file_path: os.PathLike | str) -> None:
        """
        :param file_path: The input file path to the Binary YAML file
        """

        # Detecting if the path is real
        if not os.path.exists(file_path):
            raise FileExistsError("File path given doesn't point to a real file! File path: " + str(file_path))

        # Getting the file data
        with open(file_path, "rb") as f_in:
            raw_data = f_in.read()

        self.byml_controller = Byml(raw_data, os.path.basename(file_path))
