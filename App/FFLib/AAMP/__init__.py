# /App/FFLib/AAMP/__init__.py
# Contains AAMP Class
import pathlib
import tempfile

# Importing packages and modules
import botw_tools.aamp
import argparse
import os


# AAMP Class
class AAMP:
    def __init__(self, file_path: os.PathLike | str):
        """
        An AAMP Class to manage AAMP file formats.
        :param file_path: The path to the AAMP file.
        """

        # Creating self variables
        self.file_path = file_path

        # Getting the file's data
        with open(file_path, "rb") as f_in:
            self.data = f_in.read()

    def to_yaml(self) -> str:

        temp_dir = tempfile.TemporaryDirectory()
        dest = os.path.join(temp_dir.name, "out.yml")

        botw_tools.aamp.aamp_to_yml(args=argparse.Namespace(
            src=pathlib.Path(self.file_path),
            dst=pathlib.Path(dest)), data=self.data)

        with open(dest, "r") as f_in:
            yaml_data = f_in.read()

        temp_dir.cleanup()

        return yaml_data

    def to_aamp(self) -> bytes:
        pass    # TODO: Stub
