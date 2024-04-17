# App/AppLib/index.py
# Contains GUI index

# Importing GUI
from App.GUI.project_editor import project_editor as project_editor_redirect
from App.GUI.SubWin.project_editor.settings_menu import settings_menu as settings_menu_redirect
from App.GUI.main_menu import main_menu as main_menu_redirect

# Importing local modules
from App.AppLib.plugin_handler import PluginHandler

# Importing packages
from functools import partial
import importlib.util
import os


# Index class (Holds menu functions)
class Index:

    @staticmethod
    def main_menu(app):

        main_menu_redirect(app)

    @staticmethod
    def project_editor(app):

        project_editor_redirect(app)

    @staticmethod
    def launch_plugin_menu_node(app, current_menu_node, plugin_dir):

        # Getting all the variables
        command_name = current_menu_node["CommandName"]
        command_file = current_menu_node["CommandFile"]
        raw_params = current_menu_node["CommandParams"]

        # Getting the command
        file_path = os.path.join(
            plugin_dir, command_file
        )
        spec = importlib.util.spec_from_file_location(command_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Creating command
        command = getattr(module, command_name)

        # Configuring command params
        command_params_dict = {}

        for item in raw_params:
            if item == 'App':
                command_params_dict["App"] = app

        command = partial(command, command_params_dict)

        # Running command
        command()
        print("Done!")

