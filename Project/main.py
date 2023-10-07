from App.Program import *

app = Program()
app.main()

while app.returnStatement != "Closed":
    if app.returnStatement == "SELECT_EDITOR":
        app.select_editor()
    if app.returnStatement == "SETTINGS":
        app.settings()
