# /App/AppLib/plugin_handler.py
# This is a plugin handler library

# Importing libraries and modules
import json
import os


# PluginHandler class
class PluginHandler:
    @staticmethod
    def get_plugin_folder():
        # TODO: Replace os.getcwd() with os.getenv('LOCALAPPDATA')
        plugins_folder = os.path.join(
            os.getcwd(), "0x1de-NX", "Plugins",
        )
        # Creating the directories if they don't exist
        if not os.path.exists(plugins_folder):
            os.makedirs(plugins_folder)
        return plugins_folder

    @staticmethod
    def get_plugins():

        plugins_folder = PluginHandler.get_plugin_folder()

        # Creating the folder list
        folder_list = os.listdir(plugins_folder)
        print(folder_list)

        # Creating the plugin config file if it doesn't exist
        if not os.path.join(plugins_folder, 'plugins.json'):

            json_contents = {}

            for item in folder_list:
                json_contents[item] = False

            with open(os.path.join(plugins_folder, 'plugins.json'), 'w') as f_out:
                json.dump(json_contents, f_out)

        # Returning the contents
        with open(os.path.join(plugins_folder, 'plugins.json'), 'r') as f_in:
            return json.load(f_in)

