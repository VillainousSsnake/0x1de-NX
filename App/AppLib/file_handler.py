# /App/AppLib/texture_handler.py
# This is a file handler module

# Importing libraries
from pygments.lexers import data as pylexers
from tkinter import messagebox, ttk
from functools import partial
import customtkinter as ctk
from chlorophyll import *
import os

# Importing modules and file dependencies
from App.FFLib.StandardArchive import Sarc
import json
import yaml


# The types of files that this class can detect and handle
ValidFileFormats = {
        # Standard File Formats
        ".json": "JavaScriptObjectNotation",
        ".yaml": "YetAnotherMarkupLanguage",
        ".yml": "YetAnotherMarkupLanguage",
        ".txt": "TextFile",
        # AINB
        ".ainb": "AINodeBinary",
        # Sarc Archives
        ".bfarc": "SarcArchive",
        ".bkres": "SarcArchive",
        ".blarc": "SarcArchive",
        ".genvb": "SarcArchive",
        ".pack": "SarcArchive",
        ".sarc": "SarcArchive",
        ".ta": "SarcArchive",
        # Binary Yaml
        "byml": "BinaryYAML",
        "bgyml": "BinaryYAML",
        # ZStandard
        ".zs": "ZStandard",
}

FileFormatIcons = {
    "JavaScriptObjectNotation": chr(0x1F5CF),
    "YetAnotherMarkupLanguage": chr(0x1F5CF),
    "SarcArchive": chr(0x1F5C4),
    "BinaryYAML": chr(0x1F5CE),
    "ZStandard": chr(0xf15b),
    "AINodeBinary": chr(0x1F916),
    "TextFile": chr(0x1F5CF),
    None: chr(0x1F5CB),
}

CodeViewColorScheme = {
  "editor": {
    "bg": "#242424",
    "fg": "#9FAABD",
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
    "string": "#699252",
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
    "affix": "#699252",
    "char": "#699252",
    "delimeter": "#699252",
    "doc": "#699252",
    "double": "#699252",
    "escape": "#699252",
    "heredoc": "#699252",
    "interpol": "#699252",
    "regex": "#699252",
    "single": "#699252",
    "symbol": "#699252"
  },
  "number": {
    "binary": "#2AACB8",
    "float": "#2AACB8",
    "hex": "#2AACB8",
    "integer": "#2AACB8",
    "long": "#2AACB8",
    "octal": "#2AACB8"
  },
  "comment": {
    "hashbang": "#6272a4",
    "multiline": "#6272a4",
    "preproc": "#ff79c6",
    "preprocfile": "#f1fa8c",
    "single": "#787D73",
    "special": "#787D73"
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
    def display_file_to_tabview_from_info(app, tabview: ctk.CTkTabview, item_info: dict, file_editor_obj=None) -> None:

        # Creating file format variable
        file_format = item_info["tags"][1]

        # Creating master variable
        master = tabview.tab(item_info["text"])

        # Match statement for displaying the different file formats
        match file_format:

            case "JavaScriptObjectNotation":        # Displaying JSON format

                # Creating the top navigation frame
                top_navigation_frame = ctk.CTkFrame(
                    master=master,
                    height=30,
                    fg_color="#242424"
                )
                top_navigation_frame.pack(fill="x")

                # Creating the Save, Import, and Export buttons
                save_button = ctk.CTkButton(
                    master=top_navigation_frame,
                    text=chr(0x0001F5AB) + " Save",
                    font=("Inter", 15),
                    anchor="w",
                )
                save_button.pack(anchor="w", side="left")

                export_button = ctk.CTkButton(
                    master=top_navigation_frame,
                    text=chr(0x21EE) + " Export",
                    font=("Inter", 15),
                    anchor="w",
                )
                export_button.pack(anchor="w", side="left")

                # Creating code_view
                code_view = CodeView(
                    master=master,
                    lexer=pylexers.JsonLexer,
                    color_scheme=CodeViewColorScheme,
                    width=999999,
                    height=999999,
                    font=("Cascadia Code", app.settings["font_size"]),
                )
                code_view.pack(fill="both", side="top", anchor="w")

                # Inserting the json data into the code view widget
                with open(item_info["values"][0], "r") as file_in:
                    parsed_data = json.loads(file_in.read())
                    pretty_json = json.dumps(parsed_data, indent=4) + "\n"
                    code_view.insert(0.0, pretty_json)

                # Creating the button functions
                def save_file():
                    code_view_contents = code_view.get("0.0", "end")
                    with open(item_info["values"][0], "w") as f:
                        f.write(code_view_contents)

                # Assigning the button functions
                save_button.configure(command=save_file)

                # Exiting function
                return None

            case "YetAnotherMarkupLanguage":        # Displaying YAML format

                # Creating the top navigation frame
                top_navigation_frame = ctk.CTkFrame(
                    master=master,
                    height=30,
                    fg_color="#242424"
                )
                top_navigation_frame.pack(fill="x")

                # Creating the Save, Import, and Export buttons
                save_button = ctk.CTkButton(
                    master=top_navigation_frame,
                    text=chr(0x0001F5AB) + " Save",
                    font=("Inter", 15),
                    anchor="w",
                )
                save_button.pack(anchor="w", side="left")

                export_button = ctk.CTkButton(
                    master=top_navigation_frame,
                    text=chr(0x21EE) + " Export",
                    font=("Inter", 15),
                    anchor="w",
                )
                export_button.pack(anchor="w", side="left")

                # Creating code_view
                code_view = CodeView(
                    master=master,
                    lexer=pylexers.YamlLexer,
                    color_scheme=CodeViewColorScheme,
                    width=999999,
                    height=999999,
                    font=("Cascadia Code", app.settings["font_size"]),
                )
                code_view.pack(fill="both", side="top", anchor="w")

                # Inserting the yaml data into the code view widget
                with open(item_info["values"][0], "r") as file_in:
                    parsed_data = yaml.safe_load(file_in)
                    pretty_yaml = yaml.dump(parsed_data, default_flow_style=False)
                    code_view.insert(0.0, pretty_yaml)

                # Creating the update function
                def save_file(event=None):
                    code_view_contents = code_view.get("0.0", "end")
                    with open(item_info["values"][0], "w") as f:
                        f.write(code_view_contents)

                # Assigning the button functions
                save_button.configure(command=save_file)

                # Exiting function
                return None

            case "TextFile":                        # Displaying Text format

                # Creating the top navigation frame
                top_navigation_frame = ctk.CTkFrame(
                    master=master,
                    height=30,
                    fg_color="#242424"
                )
                top_navigation_frame.pack(fill="x")

                # Creating the Save, Import, and Export buttons
                save_button = ctk.CTkButton(
                    master=top_navigation_frame,
                    text=chr(0x0001F5AB) + " Save",
                    font=("Inter", 15),
                    anchor="w",
                )
                save_button.pack(anchor="w", side="left")

                export_button = ctk.CTkButton(
                    master=top_navigation_frame,
                    text=chr(0x21EE) + " Export",
                    font=("Inter", 15),
                    anchor="w",
                )
                export_button.pack(anchor="w", side="left")

                # Creating code_view
                code_view = CodeView(
                    master=master,
                    color_scheme=CodeViewColorScheme,
                    width=999999,
                    height=999999,
                    font=("Cascadia Code", app.settings["font_size"]),
                )
                code_view.pack(fill="both", side="top", anchor="w")

                # Inserting the yaml data into the code view widget
                with open(item_info["values"][0], "r") as file_in:
                    code_view.insert(0.0, file_in.read())

                # Creating the update function
                def save_file(event=None):
                    code_view_contents = code_view.get("0.0", "end")
                    with open(item_info["values"][0], "w") as f:
                        f.write(code_view_contents)

                # Assigning the button functions
                save_button.configure(command=save_file)

                # Exiting function
                return None

            case "SarcArchive":                     # TODO: Finish opening files (Displaying SARC format)

                # Creating the top navigation frame
                top_navigation_frame = ctk.CTkFrame(
                    master=master,
                    height=30,
                    fg_color="#242424"
                )
                top_navigation_frame.pack(fill="x")

                # Creating the Save, Import, and Export buttons
                save_button = ctk.CTkButton(
                    master=top_navigation_frame,
                    text=chr(0x0001F5AB) + " Save",
                    font=("Inter", 15),
                    anchor="w",
                )
                save_button.pack(anchor="w", side="left")

                import_button = ctk.CTkButton(
                    master=top_navigation_frame,
                    text=chr(0x2913) + " Import",
                    font=("Inter", 15),
                    anchor="w",
                )
                import_button.pack(anchor="w", side="left")

                export_button = ctk.CTkButton(
                    master=top_navigation_frame,
                    text=chr(0x21EE) + " Export",
                    font=("Inter", 15),
                    anchor="w",
                )
                export_button.pack(anchor="w", side="left")

                # Getting the list of sarc files
                sarc_list = Sarc.list_sarc_contents(item_info["values"][0], mode='fp')

                # Creating path variables
                sarc_extract_folder = os.path.join(
                    os.path.join(os.getenv("LOCALAPPDATA"), "0x1de-NX", "_temp_"),
                    str(os.path.basename(item_info["values"][0])).replace(".", "_"),
                )

                # Creating the sarc_extract_folder
                os.makedirs(sarc_extract_folder)

                # Extracting the sarc into the folder
                Sarc.extract_sarc_to_dir(item_info["values"][0], sarc_extract_folder)

                # Configuring children of project_tree_treeview_frame
                FONT = ("monospace", int(app.settings["font_size"]))
                ROW_HEIGHT = int(int(app.settings["font_size"]) * 2.5)

                # Minimum and maximum for font size for project Treeview widget
                if int(app.settings["font_size"]) > 25:
                    FONT = ("monospace", 25)
                    ROW_HEIGHT = 50
                if int(app.settings["font_size"]) < 18:
                    FONT = None

                # Creating tree-view style
                tree_style = ttk.Style()
                tree_style.theme_use('default')
                tree_style.configure(
                    "sarcStyle.Treeview",
                    background="#242424",
                    foreground="white",
                    fieldbackground="#242424",
                    borderwidth=0,
                )

                # Applying fonts
                if FONT is not None:
                    tree_style.configure(
                        "Treeview",
                        font=FONT,
                        rowheight=ROW_HEIGHT
                    )

                sarc_treeview = ttk.Treeview(  # Project treeview
                    master=master,
                    show="tree",
                    height=99999999,
                    style="sarcStyle.Treeview"
                )
                sarc_treeview.pack(fill="both", side="top")

                # Defining the on_double_click function for sarc_treeview
                def on_double_click(file_editor, event=None):
                    curItem = sarc_treeview.focus()
                    itemInfo = sarc_treeview.item(curItem)
                    file_editor.open_file(app, item_info=itemInfo)

                # Binding the open function to sarc treeview
                sarc_treeview.bind(
                    "<Double-Button-1>",
                    partial(on_double_click, file_editor_obj)
                )

                # Inserting all the folders into tree view
                dir_list = []

                for file_path in sarc_list:

                    if os.path.split(file_path)[0] not in dir_list:
                        dir_list.append(os.path.split(file_path)[0])

                for item in dir_list:

                    if "/" not in item:  # Adding the items that don't have sub-folders
                        if not sarc_treeview.exists(item):
                            sarc_treeview.insert(
                                parent="",
                                index="end",
                                iid=item,
                                text=chr(0x0001F4C1) + " " + item,
                                tags=["Directory"]
                            )
                    else:   # If there is "/" in item

                        # Creating item_folders_dict
                        item_folders_dict = dict()
                        parent = ""

                        for name in item.split("/"):
                            parent += name + "/"
                            item_folders_dict[parent[:len(parent)-1]] = sarc_treeview.exists(parent[:len(parent)-1])

                        del parent

                        # Check each item to see if it exists and if not create the item
                        for key in item_folders_dict:

                            # If the item doesn't exist
                            if not item_folders_dict[key]:

                                # Creating the item
                                sarc_treeview.insert(
                                    parent=os.path.split(key)[0],
                                    index="end",
                                    iid=key,
                                    text=chr(0x0001F4C1) + " " + os.path.basename(key),
                                    tags=["Directory"],
                                )

                # Inserting all the files into tree view
                for item_path in sarc_list:
                    sarc_treeview.insert(
                        index="end",
                        parent=os.path.split(item_path)[0],
                        iid=item_path,
                        text=(FileHandler.get_file_info_from_name(os.path.basename(item_path))["icon"]
                              + " " + os.path.basename(item_path)),
                        tags=[
                            "File",
                            FileHandler.get_file_info_from_name(os.path.basename(item_path))["format"]
                        ],
                        values=[os.path.join(sarc_extract_folder, item_path)],
                    )

                # Exiting function
                return None

            case "ZStandard":                       # TODO: Displaying ZSTD format
                # Exiting function
                return None

        messagebox.showerror(
            title="file_format Error",
            message="This file is not supported!\n" + f"Unsupported File Format: " + file_format
        )
        tabview.delete(item_info["text"])
