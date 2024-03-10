# /0x1de-NX.py
# Holds main program code

# Importing modules
from App.AppLib.app import App
from App.AppLib.index import Index

# Creating App variable
app = App()

# Mainloop
while app.returnStatement != "exit":

    # Menu System
    match app.returnStatement:

        case "main":  # Main Menu
            Index.main_menu(app)

        case "project_editor":  # Project Editor Menu
            Index.project_editor(app)
