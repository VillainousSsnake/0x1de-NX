# /App/AppLib/config.py
# Contains Config class

# Importing Modules
import os

# Creating default_settings
default_settings = '''current_theme: Dark
romfs_path: None
ainb_code_format: JSON
font_size: 15
author_name: None'''  # Default settings variable


class Config:

    @staticmethod
    def get_all_settings(mode="dict"):

        # Creating the variables that hold the paths
        cache_path = os.path.join(os.getcwd(), "0x1de-NX", "_Cache_")
        settings_file_path = os.path.join(cache_path, "settings.config")

        # Detecting if the _Cache_ path exists
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        # Detecting if the settings_file_path exists
        if not os.path.exists(settings_file_path):
            with open(settings_file_path, "w") as f_out:
                f_out.write(default_settings)

        # Getting the yaml contents (list)
        with open(settings_file_path, "r") as f_in:
            data = f_in.read().split("\n")

        new_data = {}

        for item in data:
            new_data[item.split(": ")[0]] = item.split(": ")[1]

        if mode == "dict":

            output = {}

            for key in new_data:
                if new_data[key].lower() == 'true':
                    output[key] = True
                elif new_data[key].lower() == 'false':
                    output[key] = False
                elif new_data[key].lower() == 'none':
                    output[key] = False
                else:
                    output[key] = new_data[key]

        elif mode == "list":

            output = []

            for key in new_data:
                output.append(key)

        else:

            raise ValueError("mode '" + str(mode) + "' is not a valid mode")

        return output

    @staticmethod
    def get_setting(entry):

        # Creating the variables that hold the paths
        cache_path = os.path.join(os.getcwd(), "0x1de-NX", "_Cache_")
        settings_file_path = os.path.join(cache_path, "settings.config")

        # Detecting if the _Cache_ path exists
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        # Detecting if the settings_file_path exists
        if not os.path.exists(settings_file_path):
            with open(settings_file_path, "w") as f_out:
                f_out.write(default_settings)

        # Getting the yaml contents (list)
        with open(settings_file_path, "r") as f_in:
            data = f_in.read().split("\n")

        new_data = {}

        for item in data:
            new_data[item.split(": ")[0]] = item.split(": ")[1]

        output = new_data[entry]
        if output.lower() == 'true':
            output = True
        if output.lower() == 'false':
            output = False
        if output.lower() == 'none':
            output = None

        return output

    @staticmethod
    def overwrite_setting(key, value):
        # Creating the variables that hold the paths
        cache_path = os.path.join(os.getcwd(), "0x1de-NX", "_Cache_")
        settings_file_path = os.path.join(cache_path, "settings.config")

        # Detecting if the _Cache_ path exists
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        # Detecting if the settings_file_path exists
        if not os.path.exists(settings_file_path):
            with open(settings_file_path, "w") as f_out:
                f_out.write(default_settings)

        # Getting the contents (list)
        with open(settings_file_path, "r") as f_in:
            data = f_in.read().split("\n")

        new_data = {}

        for item in data:
            new_data[item.split(": ")[0]] = item.split(": ")[1]

        # Detecting booleans in the value and converting them to strings
        if value is True:
            value = 'true'
        elif value is False:
            value = 'false'
        elif value is None:
            value = 'none'
        else:
            value = str(value)

        # Overwriting the value to the key
        new_data[key] = value

        compiled_data = ""

        # Compiling the dictionary
        for _key in new_data:
            compiled_data += str(_key) + ": " + str(new_data[_key]) + "\n"

        # Overwriting the config file
        with open(settings_file_path, "w") as f_out:
            f_out.write(compiled_data[:len(compiled_data)-1])

        return 0
