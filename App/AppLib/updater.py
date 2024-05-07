# /App/AppLib/updater.py
# Contains Updater class

# Importing libraries and modules
import requests
import json


# Global Variables
CurrentVersionGlobal = {
  "type": "Early Access",
  "version": "1.0.1"
}


# Updater class
class Updater:
    @staticmethod
    def get_app_version():

        return CurrentVersionGlobal

    @staticmethod
    def get_latest_version():

        url = f"https://raw.githubusercontent.com/VillainousSsnake/0x1de-NX/main/latest_version.json"
        response = requests.get(url)
        data = json.loads(response.text)
        return data["latest_app_version"]
