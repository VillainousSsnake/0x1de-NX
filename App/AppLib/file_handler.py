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
        ".zs": "ZStandardCompressedFile"
}


# The file handler class
class FileHandler:

    @staticmethod
    def get_file_info_from_name(file_name):
        for key in ValidFileFormats:
            if key in file_name:
                return ValidFileFormats[key]

    @staticmethod
    def get_file_info_from_data(file_data):
        pass    # TODO: Stub

    @staticmethod
    def get_file_info_from_path(file_path):
        pass    # TODO: Stub
