# /App/AppLib/texture_handler.py
# This is a texture handler module

# Importing modules and libraries
import os


# The texture handler class
class TextureHandle:

    @staticmethod
    def get_texture_directory() -> str:

        # TODO: Replace os.getcwd() with os.getenv('LOCALAPPDATA')
        texture_folder_path = os.path.join(
            os.getcwd(), "App", "Image", "Tex"
        )

        # Creating the directories if they don't exist
        if not os.path.exists(texture_folder_path):
            os.makedirs(texture_folder_path)

        return texture_folder_path
