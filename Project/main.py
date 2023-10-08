from App.Program import *

app = Program()
app.main_menu()

while app.returnStatement != "Closed":
    if app.returnStatement == "MAIN_MENU":
        app.main_menu()
    if app.returnStatement == "SELECT_EDITOR":
        app.select_editor()
    if app.returnStatement == "SETTINGS":
        app.settings()
    if app.returnStatement == "ZSTANDARD_EDITOR":
        app.zstandard_editor()
    if app.returnStatement == "MESH_CODEC_EDITOR":
        app.mesh_codec_editor()
    if app.returnStatement == "GAME_PATH_SELECT":
        app.game_path_select()
