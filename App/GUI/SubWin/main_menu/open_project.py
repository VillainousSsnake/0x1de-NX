# /App/GUI/SubWin/open_project.py


# Importing modules and libraries
from App.AppLib.project_handler import ProjectHandler
from tkinter import filedialog


# Defining open_project function
def open_project(root, app, project_path=None):

    if project_path is None:

        # Asking user for the project folder
        folder_select = filedialog.askdirectory(
            initialdir=ProjectHandler.get_project_directory(),
            title="Open Project...",
            mustexist=True,
        )

        # Detecting if the user canceled
        if folder_select == "":
            return 0

        # Setting project_path to the given directory path
        project_path = folder_select

    # Setting the open project variable to the project path
    app.variables["open_project_fp"] = project_path

    # Exiting the current menu and summoning the next one
    root.destroy()
    app.returnStatement = "project_editor"
