# /App/FFLib/AAMP/__init__.py
# Contains AAMP Class
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

    def to_yaml(self):

        temp_dir = tempfile.TemporaryDirectory()
        dest = os.path.join(temp_dir.name, "out.yml")

        botw_tools.aamp.yml_to_aamp(args=argparse.Namespace(src=self.file_path, dst=dest), data=self.data)

        with open(dest, "r") as f_in:
            data = f_in.read()

        temp_dir.cleanup()

        return data
