# /0x1de-NX.py
# Holds main program code

from App.AppLib.app import App
from App.AppLib.index import Index

app = App()

while app.returnStatement != "exit":

    match app.returnStatement:

        case "main":
            Index.main_menu(app)
