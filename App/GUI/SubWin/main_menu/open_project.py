# /App/GUI/SubWin/open_project.py


# Importing modules and libraries\
from App.AppLib.project_handler import ProjectHandler
from tkinter import filedialog


# Defining open_project function
def open_project(root, app):

    folder_select = filedialog.askdirectory(
        initialdir=ProjectHandler.get_project_directory(),
        title="Open Folder...",
        mustexist=True,
    )

    # Detecting if the user canceled
    if folder_select == "":
        return 0

    app.variables["open_project_fp"] = folder_select

    # Exiting the current menu and summoning the next one
    root.destroy()
    app.returnStatement = "project_editor"
