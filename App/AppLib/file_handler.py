# /App/AppLib/texture_handler.py
# This is a file handler module

# Importing modules and libraries
from tkinter import messagebox
import customtkinter as ctk
import pygments.lexers.data
from chlorophyll import *
import pprint
import json


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

CodeViewColorScheme = {
  "editor": {
    "bg": "#282a36",
    "fg": "#f8f8f2",
    "select_bg": "#44475a",
    "select_fg": "#f8f8f2",
    "inactive_select_bg": "#402725",
    "caret": "#f8f8f0",
    "caret_width": 1,
    "border_width": 0,
    "focus_border_width": 0
  },
  "general": {
    "comment": "#6272a4",
    "error": "#f8f8f0",
    "escape": "#f8f8f2",
    "keyword": "#ff79c6",
    "name": "#50fa7b",
    "string": "#99c794",
    "punctuation": "#ff79c6"
  },
  "keyword": {
    "constant": "#bd93f9",
    "declaration": "#ff79c6",
    "namespace": "#ff79c6",
    "pseudo": "#ff79c6",
    "reserved": "#ff79c6",
    "type": "#ff79c6"
  },
  "name": {
    "attr": "#50fa7b",
    "builtin": "#ffb86c",
    "builtin_pseudo": "#ffb86c",
    "class": "#8be9fd",
    "class_variable": "#f8f8f2",
    "constant": "#bd93f9",
    "decorator": "#8be9fd",
    "entity": "#50fa7b",
    "exception": "#8be9fd",
    "function": "#50fa7b",
    "global_variable": "#f8f8f2",
    "instance_variable": "#f8f8f2",
    "label": "#50fa7b",
    "magic_function": "#50fa7b",
    "magic_variable": "#f8f8f2",
    "namespace": "#f8f8f2",
    "tag": "#ff79c6",
    "variable": "#ffb86c"
  },
  "operator": {
    "symbol": "#ff79c6",
    "word": "#ff79c6"
  },
  "string": {
    "affix": "#f1fa8c",
    "char": "#f1fa8c",
    "delimeter": "#f1fa8c",
    "doc": "#f1fa8c",
    "double": "#f1fa8c",
    "escape": "#f1fa8c",
    "heredoc": "#f1fa8c",
    "interpol": "#f1fa8c",
    "regex": "#f1fa8c",
    "single": "#f1fa8c",
    "symbol": "#f1fa8c"
  },
  "number": {
    "binary": "#bd93f9",
    "float": "#bd93f9",
    "hex": "#bd93f9",
    "integer": "#bd93f9",
    "long": "#bd93f9",
    "octal": "#bd93f9"
  },
  "comment": {
    "hashbang": "#6272a4",
    "multiline": "#6272a4",
    "preproc": "#ff79c6",
    "preprocfile": "#f1fa8c",
    "single": "#6272a4",
    "special": "#6272a4"
  }
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
    def display_file_to_tabview_from_info(tabview: ctk.CTkTabview, item_info: dict) -> None:

        # Creating file format variable
        file_format = item_info["tags"][1]

        # Creating master variable
        master = tabview.tab(item_info["text"])

        # Match statement for displaying the different file formats
        match file_format:

            case "JavaScriptObjectNotation":        # Displaying JSON format

                # Creating code_view
                code_view = CodeView(
                    master=master,
                    lexer=pygments.lexers.data.JsonLexer,
                    color_scheme=CodeViewColorScheme,
                    width=999999,
                    height=999999,
                )
                code_view.pack(fill="both", side="top", anchor="w")

                # Inserting the json data into the code view widget
                with open(item_info["values"][0], "r") as file_in:
                    parsed_data = json.loads(file_in.read())
                    pretty_json = json.dumps(parsed_data, indent=4) + "\n"
                    code_view.insert(0.0, pretty_json)

                code_view.update()

                # Exiting function
                return None

            case "YetAnotherMarkupLanguage":        # Displaying YAML format
                return None    # TODO: Stub

            case "SarcArchive":                     # Displaying SARC format
                return None    # TODO: Stub

            case "ZStandard":                       # Displaying ZSTD format
                return None    # TODO: Stub

        messagebox.showerror(title="file_format Error", message="This file is not supported!")
        tabview.delete(item_info["text"])
