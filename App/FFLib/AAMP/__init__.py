# /App/FFLib/AAMP/__init__.py
# Contains AAMP Class

# Importing packages and modules
import subprocess
import tempfile
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

    def to_xml(self):

        # Creating a temporary directory
        temp_dir = tempfile.TemporaryDirectory()

        # Creating the temporary aamp file with self.data
        with open(os.path.join(temp_dir.name, "file.aamp"), "wb") as f_out:
            f_out.write(self.data)

        # TODO: Finish
