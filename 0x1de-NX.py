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
