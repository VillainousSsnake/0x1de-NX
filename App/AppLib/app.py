# /App/AppLib/app.py
# Contains App class

# Importing Modules
from App.AppLib.config import Config


# App class
class App:
    def __init__(self):
        self.returnStatement = "main"
        self.settings = {
            "current_theme": Config.get_setting("current_theme"),
            "romfs_path": Config.get_setting("romfs_path"),
            "ainb_code_format": Config.get_setting("ainb_code_format"),
            "font_size": Config.get_setting("font_size"),
            "author_name": Config.get_setting("author_name"),
            "emulator_path": Config.get_setting("emulator_path"),
            "rom_path": Config.get_setting("rom_path"),
            "mod_folder_path": Config.get_setting("mod_folder_path"),
        }
        self.variables = {
            "open_project_fp": None,
        }
