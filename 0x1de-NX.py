# /0x1de-NX.py
# Holds main program code

# Importing packages
from tkinter import messagebox, filedialog
import shutil
import sys
import os

# Importing modules
from App.AppLib.plugin_handler import PluginHandler
from App.AppLib.config import Config
from App.AppLib.index import Index
from App.AppLib.app import App

# Clearing the temp folder
temp_folder = os.path.join(os.getenv("LOCALAPPDATA"), "0x1de-NX", "_temp_")
if os.path.exists(temp_folder):
    shutil.rmtree(temp_folder)

# Creating App variable
app = App()

# Removing the splash screen
if getattr(sys, 'frozen', False):
    import pyi_splash
    pyi_splash.close()

# Detecting if romfs_path is real
if not os.path.exists(str(app.settings["romfs_path"])):

    # Asking user to provide romfs path
    continue_prompt = False

    # While continue prompt is no, loop
    while continue_prompt is False:

        messagebox.showinfo(
            "Select ROMFS Path",
            "Please select your Zelda: Tears of the Kingdom RomFS dump folder.",
        )
        romfs_folder = filedialog.askdirectory(title="Select RomFS Folder Path")

        if romfs_folder == "":

            message = """Do you want to continue without a romfs dump?
This will most likely cause a lot of errors in the future."""
            continue_prompt = messagebox.askyesno(
                "0x1de-NX Pop-up", message
            )

        else:
            app.settings["romfs_path"] = romfs_folder
            Config.overwrite_setting("romfs_path", romfs_folder)
            continue_prompt = True

# Checking if ROM path is real
if not os.path.exists(str(app.settings["rom_path"])):
    # Asking user to provide game ROM path
    continue_prompt = False
    supported_file_formats = (
        ("Nintendo Switch ROM File", ["*.xci", ".nsp"]),
    )

    # While continue prompt is no, loop
    while continue_prompt is False:

        messagebox.showinfo(
            "Select The \"Legend of Zelda: Tears of the Kingdom\" Game ROM",
            """Please select your \"Legend of Zelda: Tears of the Kingdom\" Game ROM file. 
(NOTE: Make sure that this is the Game ROM file that is connected to your emulator)"""
        )
        rom_path = filedialog.askopenfile(
            title="Select Game ROM File",
            filetypes=supported_file_formats,
        )
        rom_path = rom_path.name

        if rom_path == "":

            message = """Do you want to continue without a Game ROM File?
    This will most likely cause a lot of errors in the future."""
            continue_prompt = messagebox.askyesno(
                "Continue without Game ROM? (UNSAFE!!!)", message
            )

        else:
            app.settings["rom_path"] = rom_path
            Config.overwrite_setting("rom_path", rom_path)
            continue_prompt = True

# Checking if emulator path is real
if not os.path.exists(str(app.settings["emulator_path"])):
    # Asking user to provide game ROM path
    continue_prompt = False
    supported_file_formats = (
        ("Windows Executable File", "*.exe"),
        ("All Files", "")
    )

    # While continue prompt is no, loop
    while continue_prompt is False:

        messagebox.showinfo(
            "0x1de-NX | Select The \"Legend of Zelda: Tears of the Kingdom\" Emulator EXE",
            """Please select your Nintendo Switch Emulator EXE file."""
        )
        emulator_path = filedialog.askopenfile(
            title="Select Nintendo Switch Emulator EXE",
            filetypes=supported_file_formats,
        )
        emulator_path = emulator_path.name

        if emulator_path == "":

            message = """Do you want to continue without an Emulator?
        This will most likely cause a lot of errors in the future."""
            continue_prompt = messagebox.askyesno(
                "0x1de-NX | Continue without Emulator? (UNSAFE!!!)", message
            )

        else:
            app.settings["emulator_path"] = emulator_path
            Config.overwrite_setting("emulator_path", emulator_path)
            continue_prompt = True

# Checking if mod folder path is real
if not os.path.exists(str(app.settings["mod_folder_path"])):

    # Asking user to provide mod folder path
    continue_prompt = False

    # While continue prompt is no, loop
    while continue_prompt is False:

        messagebox.showinfo(
            "0x1de-NX | Select The Mod Folder Path",
            """Please select your Nintendo Switch Emulator's mod folder path for "The Legend of Zelda: Tears of the Kingdom"."""
        )
        mod_folder_path = filedialog.askdirectory(
            title="Select Zelda Mod Folder Path",
        )
        emulator_path = mod_folder_path

        if mod_folder_path == "":

            message = """Do you want to continue without a Zelda: TOTK Mod Folder?
        This will most likely cause a lot of errors in the future."""
            continue_prompt = messagebox.askyesno(
                "0x1de-NX | Continue without \"Zelda: TOTK\" Mod Folder? (UNSAFE!!!)", message
            )

        else:
            app.settings["mod_folder_path"] = mod_folder_path
            Config.overwrite_setting("mod_folder_path", mod_folder_path)
            continue_prompt = True


# Mainloop
while app.returnStatement != "exit":

    # Menu System
    match app.returnStatement:

        case "main":  # Main Menu
            Index.main_menu(app)

        case "project_editor":  # Project Editor Menu
            Index.project_editor(app)

        case _:     # If no cases are matched

            # If there are no enabled plugins
            if PluginHandler.get_enabled_plugins() == {}:
                print(
                    "Bad Index Parameter '" + app.returnStatement + "'"
                )

            else:   # Otherwise, looking for enabled plugins with menu nodes

                enabled_plugins = PluginHandler.get_enabled_plugins()

                menu_node_plugins = {}

                for key in enabled_plugins:
                    if PluginHandler.get_menu_node_from_json(enabled_plugins[key]) is not None:
                        pass    # TODO: Stub

# Clearing the temp folder
temp_folder = os.path.join(os.getenv("LOCALAPPDATA"), "0x1de-NX", "_temp_")
if os.path.exists(temp_folder):
    shutil.rmtree(temp_folder)
