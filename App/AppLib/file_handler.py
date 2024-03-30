# /App/AppLib/texture_handler.py
# This is a file handler module

# Importing modules and libraries
from tkinter import messagebox
import customtkinter as ctk


# The types of files that this class can detect and handle
ValidFileFormats = {
        # Standard File Formats
        ".json": "JavaScriptObjectNotation",
        ".yaml": "YetAnotherMarkupLanguage",
        ".yml": "YetAnotherMarkupLanguage",
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
    "JavaScriptObjectNotation": chr(0x1F5CF),
    "YetAnotherMarkupLanguage": chr(0x1F5CF),
    "SarcArchive": chr(0x1F5C4),
    "ZStandard": chr(0xf15b),
    None: chr(0x1F5CB),
}


# The file handler class
class FileHandler:

    @staticmethod
    def get_file_info_from_name(file_name) -> dict:

        # Creating empty variables
        file_format = None
        file_icon = None

        # Getting the file format
        for key in ValidFileFormats:
            if key in file_name:
                file_format = ValidFileFormats[key]
                break

        # Getting the file icon
        for key in FileFormatIcons:
            if key == file_format:
                file_icon = FileFormatIcons[key]

        # Returning the output dictionary
        return {"format": file_format, "icon": file_icon}

    @staticmethod
    def display_file_to_frame_from_info(master: ctk.CTkTabview, item_info: dict) -> None:

        # Creating file format variable
        file_format = item_info["tags"][1]

        # Detecting if the format is recognized
        if file_format is None:
            messagebox.showerror(title="file_format Error", message="This file is not supported!")
            return None

        match file_format:

            case "JavaScriptObjectNotation":
                return None    # TODO: Stub

            case "YetAnotherMarkupLanguage":
                return None    # TODO: Stub

            case "SarcArchive":
                return None    # TODO: Stub

            case "ZStandard":
                return None    # TODO: Stub

        messagebox.showerror(title="file_format Error", message="This file is not supported!")
        master.delete(item_info["text"])
