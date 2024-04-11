# /0x1de-NX.py
# Holds main program code

# Importing libraries
import shutil
import sys
import os

# Importing modules
from App.AppLib.app import App
from App.AppLib.index import Index

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

# Detecting if the romfs_path is None
if app.settings["romfs_path"] is None:

    # Asking user to provide romfs path
    continue_prompt = False

    # While continue prompt is no, loop
    while continue_prompt is False:

        messagebox.showinfo(
            "0x1de-NX Pop-up",
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


# Mainloop
while app.returnStatement != "exit":

    # Menu System
    match app.returnStatement:

        case "main":  # Main Menu
            Index.main_menu(app)

        case "project_editor":  # Project Editor Menu
            Index.project_editor(app)

# Clearing the temp folder
temp_folder = os.path.join(os.getenv("LOCALAPPDATA"), "0x1de-NX", "_temp_")
if os.path.exists(temp_folder):
    shutil.rmtree(temp_folder)
