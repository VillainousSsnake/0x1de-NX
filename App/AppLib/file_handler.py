# /App/AppLib/texture_handler.py
# This is a file handler module

# Importing modules and libraries
import os


# The types of files that this class can detect and handle
ValidFileFormats = {
        # Sarc Archives
        ".bfarc": "SarcArchive",
        ".bkres": "SarcArchive",
        ".blarc": "SarcArchive",
        ".genvb": "SarcArchive",
        ".pack": "SarcArchive",
        ".sarc": "SarcArchive",
        ".ta": "SarcArchive",
        # ZStandard
        ".zs": "ZStandard"
}

FileFormatIcons = {
    "SarcArchive": "\uF3BF",
    "ZStandard": "\uf15b",
}


# The file handler class
class FileHandler:

    @staticmethod
    def get_file_info_from_name(file_name) -> dict:

        # Creating the empty output dictionary
        output = dict()

        # Getting the file format
        for key in ValidFileFormats:
            if key in file_name:
                output["FileFormat"] = ValidFileFormats[key]
                break

        # Getting the file icon
        for key in FileFormatIcons:
            if key == output["FileFormat"]:
                output["Icon"] = FileFormatIcons[key]

        # Returning the output dictionary
        return output





    @staticmethod
    def get_file_info_from_data(file_data):
        pass    # TODO: Stub

    @staticmethod
    def get_file_info_from_path(file_path):
        pass    # TODO: Stub
