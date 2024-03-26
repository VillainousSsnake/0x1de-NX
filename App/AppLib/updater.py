# /App/AppLib/updater.py
# Contains Updater class

# Importing libraries and modules
import requests
import json


# Global Variables
CurrentVersionGlobal = "Alpha 0.0.1"


# Updater class
class Updater:
    @staticmethod
    def get_app_version():

        return CurrentVersionGlobal

    @staticmethod
    def get_latest_version():

        url = f"https://api.github.com/repos/VillainousSsnake/0x1de-NX/tags"
        response = requests.get(url)
        data = json.loads(response.text)
        return data[0]['name'] if data else None
