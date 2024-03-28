# /App/AppLib/texture_handler.py
# This is a file handler module

# Importing modules and libraries
import os


# The types of files that this class can detect and handle
ValidFileFormats = {
    "ZStandardFile": {
        ".zs": b"\x37\xA4\x30\xEC",
    },
    "SarcArchive": {
        ".bfarc": b"\x53\x41\x52\x43",
        ".bkres": b"\x53\x41\x52\x43",
        ".blarc": b"\x53\x41\x52\x43",
        ".genvb": b"\x53\x41\x52\x43",
        ".pack": b"\x53\x41\x52\x43",
        ".sarc": b"\x53\x41\x52\x43",
        ".ta": b"\x53\x41\x52\x43",
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
