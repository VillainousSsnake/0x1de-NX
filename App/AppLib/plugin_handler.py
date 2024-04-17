# /App/AppLib/plugin_handler.py
# This is a plugin handler library

# Importing libraries and modules
import importlib.util
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

                # Getting the contents of info.json
                info_json_path = os.path.join(plugins_folder, item, "info.json")
                with open(info_json_path, "r") as f_in:
                    plugin_info = json.load(f_in)

                # Adding the entry to the json contents
                json_contents[item] = plugin_info["Info"]["IsEnabled"]

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

    @staticmethod
    def get_plugins_menu_dropdown() -> list:
        """
        Returns list of options for the plugins menu dropdown, and the command for the option.
        This makes it possible to calculate enabled plugins in real time, without having to restart.
        :return: [["Option Name", SpecifiedCommandFromPluginInfo], ...]
        """

        # Getting enabled plugins
        enabled_plugins_dict = PluginHandler.get_enabled_plugins()

        # Creating the output dict
        output = list()

        # Going through each plugin and getting the command
        for key in enabled_plugins_dict:

            # Creating the list for this plugin.
            #  this will be added to output at the end of this for loop.
            item_list = list()

            # Getting the plugin info
            plugin_info = enabled_plugins_dict[key]

            # Getting the plugin nodes
            plugin_nodes = plugin_info["Plugin Nodes"]

            # Getting "PluginsDropdownOptionNode" node
            plugins_dropdown_node = plugin_nodes["PluginDropdownOptionNode"]

            # Appending the plugin's option name to the item list
            item_list.append(plugins_dropdown_node["OptionName"])

            # Getting the connected file node
            command_file = plugins_dropdown_node["CommandFile"]

            # Getting the items' command
            command_name = plugins_dropdown_node["CommandName"]
            file_path = os.path.join(
                PluginHandler.get_plugin_folder(),
                key, command_file
            )
            spec = importlib.util.spec_from_file_location(command_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Appending the command to the item list
            item_list.append(getattr(module, command_name))

            # Adding the item to the output list
            output.append(item_list)


        return output

