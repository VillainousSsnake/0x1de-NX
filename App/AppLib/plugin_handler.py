# /App/AppLib/plugin_handler.py
# This is a plugin handler library

# Importing libraries and modules
import os


# PluginHandler class
class PluginHandler:
    @staticmethod
    def get_plugin_folder():
        # TODO: Replace os.getcwd() with os.getenv('LOCALAPPDATA')
        output = os.path.join(
            os.getcwd(), "0x1de-NX", "Plugins",
        )
        return output

    @staticmethod
    def get_plugins():
        pass  # TODO: Stub

