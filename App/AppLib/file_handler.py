# /App/AppLib/texture_handler.py
# This is a file handler module

# Importing modules and libraries
import os


# The types of files that this class can detect and handle
ValidFileFormats = {
    "ZStandardFile": {
        ".zs": "",
    },
    "SarcArchive": {
        ".bfarc": "",
        ".bkres": "",
        ".blarc": "",
        ".genvb": "",
        ".pack": "",
        ".sarc": "",
        ".ta": "",
    },
}


# The file handler class
class FileHandler:

    @staticmethod
    def get_file_info_from_name(file_name):
        pass    # TODO: Stub

    @staticmethod
    def get_file_info_from_data(file_data):
        pass    # TODO: Stub

    @staticmethod
    def get_file_info_from_path(file_path):
        pass    # TODO: Stub
