# /0x1de-NX.py
# Holds main program code

from App.AppLib.app import App
from App.AppLib.index import Index

app = App()

# Mainloop
while app.returnStatement != "exit":

    # Menu System
    match app.returnStatement:

        case "main":  # Main Menu
            Index.main_menu(app)
