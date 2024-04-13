# /App/AppLib/texture_handler.py
# This is a file handler module


# Importing libraries
from tkinter import messagebox, ttk, filedialog
from pygments.lexers import data as pylexers
from tkinterdnd2 import DND_FILES
from functools import partial
import customtkinter as ctk
from chlorophyll import *
import shutil
import os

# Importing modules and file dependencies
from App.FFLib.StandardArchive import Sarc
from App.FFLib.AAMP import AAMP
from App.FFLib.AINB import AINB
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
        # AAMP
        ".baglblm": "AAMP",
        ".baglccr": "AAMP",
        ".baglclwd": "AAMP",
        ".baglcube": "AAMP",
        ".bagldof": "AAMP",
        ".baglenv": "AAMP",
        ".baglenvset": "AAMP",
        ".baglfila": "AAMP",
        ".bagllmap": "AAMP",
        ".baglmf": "AAMP",
        ".baglshpp": "AAMP",
        ".baglsky": "AAMP",
        ".bgapkginfo": "AAMP",
        ".bgapkglist": "AAMP",
        ".bgenv": "AAMP",
        ".bglght": "AAMP",
        ".bgmsconf": "AAMP",
        ".bgsdw": "AAMP",
        ".bphhb": "AAMP",
        ".bptcl": "AAMP",
        ".bptclconf": "AAMP",
}

FileFormatIcons = {
    "JavaScriptObjectNotation": chr(0x1F5CF),
    "YetAnotherMarkupLanguage": chr(0x1F5CF),
    "SarcArchive": chr(0x1F5C4),
    "BinaryYAML": chr(0x1F5CE),
    "ZStandard": chr(0xf15b),
    "AINodeBinary": chr(0x1F916),
    "TextFile": chr(0x1F5CF),
    "AAMP": chr(0x1F5CF),   # TODO: Find unicode to fit AAMP
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

ValidSarcExportFormats = (
            ('SARC formats', [
                # Plain sarc formats
                "*.bfarc",
                "*.bkres",
                "*.blarc",
                "*.genvb",
                "*.pack",
                "*.sarc",
                "*.ta",
                # Zstandard compressed
                "*.bfarc.zs",
                "*.bkres.zs",
                "*.blarc.zs",
                "*.genvb.zs",
                "*.pack.zs",
                "*.sarc.zs",
                "*.ta.zs",
            ]),
            ('Zip File', '.zip'),
        )


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
        master = ctk.CTkFrame(
            master=tabview.tab(item_info["text"]),
            width=99999999,
            height=99999999,
        )
        master.pack(anchor="nw", fill="both")

        # Match statement for displaying the different file formats
        match file_format:

            case "JavaScriptObjectNotation":        # Displaying JSON format

                # Creating the top navigation frame
                top_navigation_frame = ctk.CTkFrame(
                    master=master,
                    height=30,
                    fg_color="#242424",
                    corner_radius=0,
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

                # Removing the extra new line at the end of file
                code_view.delete(str(float(code_view.index("end"))-1), "end")

                # Creating the button functions
                def save_file():
                    code_view_contents = code_view.get("0.0", "end")
                    with open(item_info["values"][0], "w") as f:
                        f.write(code_view_contents)

                    # Showing output
                    messagebox.showinfo(
                        "0x1de-NX - Save Completed",
                        "Saved JSON file to '" + item_info["values"][0] + "'",
                    )

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

                # Removing the extra new line at the end of file
                code_view.delete(str(float(code_view.index("end")) - 1), "end")

                # Creating the update function
                def save_file(event=None):
                    code_view_contents = code_view.get("0.0", "end")
                    with open(item_info["values"][0], "w") as f:
                        f.write(code_view_contents)

                    # Showing output
                    messagebox.showinfo(
                        "0x1de-NX - Save Completed",
                        "Saved YAML file to '" + item_info["values"][0] + "'",
                    )

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

                # Removing the extra new line at the end of file
                code_view.delete(str(float(code_view.index("end")) - 1), "end")

                # Creating the update function
                def save_file(event=None):
                    code_view_contents = code_view.get("0.0", "end")
                    with open(item_info["values"][0], "w") as f:
                        f.write(code_view_contents)

                    # Showing output
                    messagebox.showinfo(
                        "0x1de-NX - Save Completed",
                        "Saved text file to '" + item_info["values"][0] + "'",
                    )

                # Assigning the button functions
                save_button.configure(command=save_file)

                # Exiting function
                return None

            case "SarcArchive":                     # Displaying SARC format

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
                                tags=["Directory"],
                                values=[os.path.join(sarc_extract_folder, item)]
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
                                    values=[os.path.join(sarc_extract_folder, item)]
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

                # Creating the button commands for the Save, Import, and Export buttons
                def save_command():

                    # Getting the new sarc data
                    new_sarc_data = Sarc.compress_sarc_from_dir(sarc_extract_folder)

                    # Getting the file's magic number
                    with open(item_info["values"][0], "rb") as f_in:
                        file_magic = f_in.read(4)

                    # Detecting if the file is zstandard
                    if file_magic == b"(\xb5/\xfd":
                        new_sarc_data = Sarc.compress_sarc_from_dir(
                            input_dir=sarc_extract_folder,
                            compress_with_zstd=True
                        )

                    # Overwriting the file
                    with open(item_info["values"][0], "wb") as f_out:
                        f_out.write(new_sarc_data)

                    # Showing output
                    messagebox.showinfo(
                        "0x1de-NX - Save Completed",
                        "Saved SARC file to '" + item_info["values"][0] + "'",
                    )

                def import_command():
                    pass    # TODO: Stub

                def export_command():

                    # Getting the file path to save the new file
                    file_explorer_prompt = filedialog.asksaveasfilename(
                        title="Save SARC file as...",
                        filetypes=ValidSarcExportFormats,
                        confirmoverwrite=True,
                    )

                    # Exiting function on cancel
                    if file_explorer_prompt is None:
                        return 0

                    # Getting the file basename from the path
                    file_basename = os.path.basename(file_explorer_prompt)

                    # Detecting if the file is a zip or not
                    if ".zip" not in file_basename:     # Compressing the file in SARC format

                        # Detecting the file extension
                        file_extension = Sarc.get_sarc_extension_from_file_name(file_basename)

                        # Getting the new sarc data
                        new_sarc_data = Sarc.compress_sarc_from_dir(sarc_extract_folder)

                        # Detecting if the file is zstandard
                        if ".zs" in file_extension:

                            # Asking to compress with zstandard
                            compress_with_zstandard = messagebox.askyesno(
                                "0x1de-NX | SARC Export",
                                "Compress with ZStandard?",
                            )

                            # Compressing with zstandard
                            if compress_with_zstandard:

                                new_sarc_data = Sarc.compress_sarc_from_dir(
                                    input_dir=sarc_extract_folder,
                                    compress_with_zstd=True
                                )

                        # Writing SARC to export path
                        with open(file_explorer_prompt, "wb") as f_out:
                            f_out.write(new_sarc_data)

                    else:   # Compressing the file in Zip format

                        # Compressing the SARC export directory as a ZIP file
                        shutil.make_archive(
                            os.path.join(   # output file name
                                os.path.split(file_explorer_prompt)[0],
                                os.path.basename(file_explorer_prompt).replace(".zip", "")
                            ),
                            'zip',
                            sarc_extract_folder
                        )

                    # Showing output
                    messagebox.showinfo(
                        "0x1de-NX | SARC Export",
                        "Successfully exported file to '" + file_explorer_prompt + "'",
                    )

                # Assigning the button commands for the Save, Import, and Export buttons
                save_button.configure(command=save_command)
                import_button.configure(command=import_command)
                export_button.configure(command=export_command)

                # Defining the on key command
                def on_key(self: ttk.Treeview, file_editor, event=None):

                    curItem = self.item(self.focus())

                    # Detecting the key symbol
                    if event.keysym == "Delete":  # If the key is "delete"

                        # Asking for confirmation
                        ok_cancel_prompt = messagebox.askokcancel(
                            "0x1de-NX | Delete File from SARC?",
                            """Are you sure you want to delete this file from the SARC?
WARNING: THIS CANNOT BE UNDONE YET!!!"""
                        )

                        # If confirmed
                        if ok_cancel_prompt:

                            # Removing the item from the tabview
                            item_name = self.focus()
                            self.delete(item_name)
                            if curItem["text"] in file_editor.tabview._tab_dict:
                                file_editor.tabview.delete(curItem["text"])

                            if file_editor.tabview.get() == "":
                                file_editor.tabview.pack_forget()
                                file_editor.nothing_opened_label.pack(anchor="center")

                            # Getting the recently deleted directory
                            recently_deleted_dir = os.path.join(
                                os.getenv("LOCALAPPDATA"), "0x1de-NX", "_temp_", "_0_RECENTLY_0_DELETED_0_"
                            )

                            # Creating the recently deleted directory if it doesn't exist
                            if not os.path.exists(recently_deleted_dir):
                                os.makedirs(recently_deleted_dir)

                            # Creating the destination directory variables
                            folders_list = os.listdir(recently_deleted_dir)
                            dest_dir = os.path.join(recently_deleted_dir, str(len(folders_list)))

                            # Creating the destination directory
                            os.makedirs(dest_dir)

                            # Moving the file to the destination
                            shutil.move(src=curItem["values"][0], dst=dest_dir)

                # Assigning the on key command to the treeview
                sarc_treeview.bind("<Key>", partial(on_key, sarc_treeview, file_editor_obj))

                # Defining the drop file command
                def drop_file(event=None):
                    path = event.data
                    if event.data[0] == "{":
                        path = event.data[1:len(event.data)-1]
                    current_treeview_item = sarc_treeview.focus()

                    if "." in current_treeview_item:
                        current_treeview_item = os.path.split(current_treeview_item)[0]

                    if current_treeview_item != "":

                        if os.path.isfile(path):
                            shutil.copy(
                                path,
                                os.path.join(sarc_extract_folder, current_treeview_item)
                            )
                        elif os.path.isdir(path):
                            yesnopopup = messagebox.askokcancel(
                                "0x1de-NX | Moving Folder",
                                "Are you sure you want to move this folder into the SARC?",
                            )
                            if not yesnopopup:
                                return 0
                            shutil.move(
                                path,
                                os.path.join(sarc_extract_folder, current_treeview_item)
                            )
                        else:
                            raise TypeError("Unknown object")

                    else:

                        if os.path.isfile(path):
                            shutil.copy(path, sarc_extract_folder)
                        elif os.path.isdir(path):
                            yesnopopup = messagebox.askokcancel(
                                "0x1de-NX | Moving Folder",
                                "Are you sure you want to move this folder into the SARC?",
                            )
                            if not yesnopopup:
                                return 0
                            shutil.move(path, sarc_extract_folder)
                        else:
                            raise TypeError("Unknown object")

                    # Deleting all the treeview items
                    sarc_treeview.delete(*sarc_treeview.get_children())

                    # Re-inserting all the items
                    for root, dirs, files in os.walk(sarc_extract_folder):

                        if os.path.basename(os.path.split(root)[0]) == "_temp_":
                            for _ITEM in dirs:
                                sarc_treeview.insert(
                                    parent="",
                                    index='end',
                                    iid=os.path.join(root, _ITEM),
                                    text=chr(0x0001F4C1) + " " + _ITEM,
                                    tags=["Directory"],
                                    values=[os.path.join(root, _ITEM)]
                                )

                            for ITEM in files:
                                sarc_treeview.insert(
                                    parent='',
                                    index='end',
                                    iid=ITEM,
                                    text=FileHandler.get_file_info_from_name(os.path.basename(item_path))["icon"]
                                          + " " + ITEM,
                                    tags=[
                                        "File",
                                        FileHandler.get_file_info_from_name(os.path.basename(item_path))["format"]
                                    ],
                                    values=[os.path.join(root, ITEM)]
                                )

                        else:
                            for _ITEM in dirs:
                                sarc_treeview.insert(
                                    parent=root,
                                    index='end',
                                    iid=os.path.join(root, _ITEM),
                                    text=chr(0x0001F4C1) + " " + _ITEM,
                                    tags=["Directory"],
                                    values=[os.path.join(root, _ITEM)]
                                )

                            for ITEM in files:
                                sarc_treeview.insert(
                                    parent=root,
                                    index='end',
                                    iid=os.path.join(root, ITEM),
                                    text=FileHandler.get_file_info_from_name(os.path.basename(item_path))["icon"]
                                          + " " + ITEM,
                                    tags=[
                                        "File",
                                        FileHandler.get_file_info_from_name(os.path.basename(item_path))["format"]
                                    ],
                                    values=[os.path.join(root, ITEM)],
                                )

                # Assigning the drag-and-drop commands
                master.drop_target_register(DND_FILES)
                master.dnd_bind('<<Drop>>', drop_file)

                # Exiting function
                return None

            case "AINodeBinary":                    # Displaying AINB Format

                # Creating the AINB controller
                ainb_controller = AINB(input_=item_info["values"][0], mode="fp")

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
                match app.settings["ainb_code_format"]:
                    case "YAML":
                        code_view.configure(lexer=pylexers.YamlLexer)
                    case "JSON":
                        code_view.configure(lexer=pylexers.JsonLexer)
                code_view.pack(fill="both", side="top", anchor="w")

                # Inserting the yaml data into the code view widget
                if app.settings["ainb_code_format"] == "YAML":
                    code_view.insert(0.0, ainb_controller.yaml)
                else:
                    code_view.insert(0.0, ainb_controller.json)

                # Creating the update function
                def save_file(event=None):
                    code_view_contents = code_view.get("0.0", "end")
                    with open(item_info["values"][0], "wb") as f:
                        match app.settings["ainb_code_format"]:
                            case "JSON":
                                f.write(AINB.json_to_ainb(code_view_contents))
                            case "YAML":
                                f.write(AINB.yaml_to_ainb(code_view_contents))

                    # Showing output
                    messagebox.showinfo(
                        "0x1de-NX - Save Completed",
                        "Saved AINB file to '" + item_info["values"][0] + "'",
                    )

                # Assigning the button functions
                save_button.configure(command=save_file)

                # Exiting function
                return None

            case "AAMP":                            # TODO: Displaying AAMP format

                # Creating the AAMP Controller
                aamp_controller = AAMP(item_info["values"][0])

                # Getting the XML data
                xml_data = aamp_controller.to_xml()

                # Exiting function
                return None

            case "BinaryYAML":                      # TODO: Displaying BYML format
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
