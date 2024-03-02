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
        }
