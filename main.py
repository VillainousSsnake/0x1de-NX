
from Project.App.Program import *
import os

app = Program()
app.main_menu()

while app.returnStatement != "Closed":

    if app.returnStatement == "MAIN_MENU":
        app.main_menu()

    elif app.returnStatement == "SELECT_EDITOR":
        app.select_editor()

    elif app.returnStatement == "SETTINGS":
        app.settings()

    elif app.returnStatement == "FILE_EDITOR":
        app.file_editor()

    elif app.returnStatement == "MESH_CODEC_EDITOR":
        app.mesh_codec_editor()

    elif app.returnStatement == "GAME_PATH_SELECT":
        app.game_path_select()

    else:
        app.display_error_code("#001", "returnStatment Doesn't Exist")


#  Deleting files in Project\__Cache__\_temp_  #
# Getting the _temp_ directory location
tempDir = os.path.join(os.getcwd(), "Project", "__Cache__", "_temp_")

# Getting the file names of all the files in _temp_
filenames = os.listdir(tempDir)

# Making a list called files and putting the
# full filepath to the file name as each list item
files = []
for filename in filenames:
    files.append(os.path.join(tempDir, filename))

# Removing the files
for file in files:
    os.remove(file)
