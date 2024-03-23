# /App/AppLib/plugin_handler.py
# This is a plugin handler library

# Importing libraries and modules
import json
import os


# PluginHandler class
class PluginHandler:
    @staticmethod
    def get_plugin_folder() -> os.path:

        # TODO: Replace os.getcwd() with os.getenv('LOCALAPPDATA')
        plugins_folder = os.path.join(
            os.getcwd(), "0x1de-NX", "Plugins",
        )

        # Creating the directories if they don't exist
        if not os.path.exists(plugins_folder):
            os.makedirs(plugins_folder)

        # Refreshing the plugins folder

        json_contents = {}

        for item in os.listdir(plugins_folder):
            if item != 'plugins.json':
                json_contents[item] = False

        with open(os.path.join(plugins_folder, 'plugins.json'), 'w') as f_out:
            json.dump(json_contents, f_out)

        # Returning the plugins folder path
        return plugins_folder

    @staticmethod
    def get_plugins() -> dict:

        plugins_folder = PluginHandler.get_plugin_folder()

        # Returning the contents
        with open(os.path.join(plugins_folder, 'plugins.json'), 'r') as f_in:
            return json.load(f_in)
