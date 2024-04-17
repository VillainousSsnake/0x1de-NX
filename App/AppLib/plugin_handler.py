# /App/AppLib/plugin_handler.py
# This is a plugin handler library

# Importing libraries and modules
import json
import os


# PluginHandler class
class PluginHandler:
    @staticmethod
    def get_plugin_folder() -> str:
        """
        Gets plugins folder and refreshes 'plugins.json' file located in plugins folder.
        :return: The path to the plugins' folder.
        """

        # Getting the plugins folder
        plugins_folder = os.path.join(
            os.getenv('LOCALAPPDATA'), "0x1de-NX", "Plugins",
        )

        # Creating the directories if they don't exist
        if not os.path.exists(plugins_folder):
            os.makedirs(plugins_folder)

        # Refreshing the plugins folder
        json_contents = {}
        for item in os.listdir(plugins_folder):
            if item != 'plugins.json':
                json_contents[item] = False

        # Writing the JSON data to the plugins.json file
        with open(os.path.join(plugins_folder, 'plugins.json'), 'w') as f_out:
            json.dump(json_contents, f_out)

        # Returning the plugins folder path
        return plugins_folder

    @staticmethod
    def get_plugins() -> dict:
        """
        Reads the plugins.json file in the plugins folder and returns its contents.
        :return: A dict with the plugins.json data
        """

        # Getting the plugins folder
        plugins_folder = PluginHandler.get_plugin_folder()

        # Returning the contents of plugin.json
        with open(os.path.join(plugins_folder, 'plugins.json'), 'r') as f_in:
            return json.load(f_in)

    @staticmethod
    def get_enabled_plugins() -> dict:
        """
        Reads the plugins.json file in the plugins folder and returns a
        dictionary with the enabled plugins name, and the enabled plugin data.
        :return:{"(Plugin Name Here)", (Plugin json dict here)}
        """

        # Getting the plugins folder
        plugins_folder = PluginHandler.get_plugin_folder()

        # Getting the contents of plugin.json
        with open(os.path.join(plugins_folder, 'plugins.json'), 'r') as f_in:
            raw_dict = json.load(f_in)

        # Creating a new list with only the enabled ones
        enabled_plugins_list = {}
        for key in raw_dict:
            if raw_dict[key]:

                # Reading the plugins info.json
                info_json = os.path.join(plugins_folder, key, "info.json")
                with open(info_json, "r") as f_in:
                    json_dict = json.load(f_in)

                # Creating the dictionary entry
                enabled_plugins_list[key] = json_dict

        # Returning the enabled plugins list
        return enabled_plugins_list

    @staticmethod
    def get_menu_node_from_json(json_dict) -> None | dict:
        """
        Returns the menu node data from the given plugin info.json data.
        :param json_dict: The dict with the info.json data
        :return: the Dict with the menu node data (or none if the given data has no menu node)
        """

        print(json_dict)    # TODO: Stub

