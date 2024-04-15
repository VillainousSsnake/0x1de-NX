# /App/FFLib/AinimSeqBinary/__init__.py
# Contains ASB class

# Importing modules, libraries, and packages
from App.FFLib.AnimSeqBinary.asb_dt import baev, converter
from App.FFLib.TotkZsDic import ZsDic
import tempfile
import os


# BAEV Class
class BAEV:
    def __init__(self, file_path: os.PathLike | str, romfs_path: os.PathLike | str):
        """
        BAEV class to convert BAEV files to json and back.
        :param file_path: input to the BAEV file
        """

        # Creating file path variable
        self.file_path = file_path
        self.romfs_path = romfs_path

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

        # Getting the file name
        file_name = os.path.basename(file_path)
        if ".zs" in file_name:
            file_name.replace(".zs", "")
        if ".baev" in file_name:
            file_name.replace(".baev", "")

        # Creating BAEV controller
        self.baev_controller = baev.BAEV.from_binary(self.data, filename=file_name)

    def to_json(self) -> str:
        """
        Converts BAEV to JSON.
        :return: JSON string
        """

        # Creating temporary directory
        temp_dir = tempfile.TemporaryDirectory()

        # Writing JSON file to out.json in temporary directory
        self.baev_controller.to_json(temp_dir.name)

        # Getting the json data from the temporary file
        with open(os.path.join(temp_dir.name, self.baev_controller.filename + ".json"), "r", encoding="utf-8") as f_in:
            json_data = f_in.read()

        # Cleaning the temp_dir
        temp_dir.cleanup()

        # Returning the json data
        return json_data

    def to_baev(self, data: str) -> bytes:
        """
        Converts JSON string to BAEV data.
        :param data: JSON string
        :return: ASB data (in bytes)
        """

        # Creating the temporary directory
        temp_dir = tempfile.TemporaryDirectory()

        # Creating the file paths
        json_file_path = os.path.join(temp_dir.name, self.baev_controller.filename + ".json")
        baev_file_path = os.path.join(temp_dir.name, self.baev_controller.filename + ".baev")

        # Dumping the JSON data into a temporary file
        with open(json_file_path, "w") as f_out:
            f_out.write(data)

        # Converting JSON file into ASB file
        converter.json_to_baev(
            filepath=json_file_path,
            output_dir=temp_dir.name,
            romfs_path=self.romfs_path,
        )

        # Getting BAEV data
        with open(baev_file_path, "rb") as f_in:
            baev_data = f_in.read()

        # Cleaning the temp_dir
        temp_dir.cleanup()

        # Returning BAEV data
        return baev_data
