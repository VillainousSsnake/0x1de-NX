# App/AppLib/index.py
# Contains GUI index

# Importing GUI
from App.GUI.project_editor import project_editor as project_editor_redirect
from App.GUI.SubWin.project_editor.settings_menu import settings_menu as settings_menu_redirect
from App.GUI.main_menu import main_menu as main_menu_redirect

# Importing local modules
from App.AppLib.plugin_handler import PluginHandler


# Index class (Holds menu functions)
class Index:

    @staticmethod
    def main_menu(app):

        main_menu_redirect(app)

    @staticmethod
    def project_editor(app):

        project_editor_redirect(app)

    @staticmethod
    def launch_plugin_menu_node(app, node_name):
        enabled_plugins_data = PluginHandler.get_enabled_plugins()  # TODO: Finish

