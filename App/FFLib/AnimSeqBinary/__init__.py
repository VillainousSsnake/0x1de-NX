# /App/FFLib/AinimSeqBinary/__init__.py
# Contains ASB class

# Importing modules, libraries, and packages
from App.FFLib.AnimSeqBinary.asb_dt import asb
from App.FFLib.TotkZsDic import ZsDic
import zstandard
import tempfile
import os


# ASB Class
class ASB:
    def __init__(self, file_path: os.PathLike | str):
        """
        ASB class to convert ASB files to json and back.
        :param file_path: input to the ASB file
        """

        # Creating file path variable
        self.file_path = file_path

        # Getting file magic
        with open(self.file_path, "rb") as f_in:
            self.magic = f_in.read(4)

        # Detecting if the file is zstandard compressed
        if self.magic == b"\x28\xb5\x2f\xfd":   # ZStandard compressed, getting decompressed data

            # Creating ZStandard decompressor
            self.data = ZsDic.auto_decompress_file(self.file_path)

        else:   # Not ZStandard compressed, getting raw data

            # Getting raw file data
            with open(self.file_path, "rb") as f_in:
                self.data = f_in.read()

        # Creating asb controller
        self.asb_controller = asb.ASB(self.data)

    def to_json(self) -> str:
        """
        Converts ASB to JSON.
        :return: JSON string
        """

        # Creating temporary directory
        temp_dir = tempfile.TemporaryDirectory()

        # Writing JSON file to out.json in temporary directory
        self.asb_controller.filename = "out"
        self.asb_controller.to_json(temp_dir.name)

        # Getting the json data from the temporary file
        with open(os.path.join(temp_dir.name, "out.json"), "r") as f_in:
            json_data = f_in.read()

        # Returning the json data
        return json_data

    def to_asb(self, data) -> bytes:
        """
        Converts JSON string to ASB data.
        :param data: JSON string
        :return: ASB data (in bytes)
        """
        pass    # TODO: Stub
