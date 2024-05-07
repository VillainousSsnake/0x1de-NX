# /App/AppLib/updater.py
# Contains Updater class

# Importing libraries and modules
from tkinter import messagebox
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
    def get_app_version() -> dict:
        """Returns the current app version"""

        return CurrentVersionGlobal

    @staticmethod
    def get_latest_version() -> dict:
        """Fetches the latest_version.json data from the 0x1de-NX repository"""

        url = f"https://raw.githubusercontent.com/VillainousSsnake/0x1de-NX/main/latest_version.json"
        response = requests.get(url)
        data = json.loads(response.text)
        return data["latest_app_version"]

    @staticmethod
    def check_for_updates() -> None:
        """Creates messagebox.showinfo object to notify the user of outdated client or up to date client"""

        # Creating the version output strings
        current_ver_out = str(CurrentVersionGlobal['type'] + " " + CurrentVersionGlobal['version'])
        latest_ver_out = str(Updater.get_latest_version()["type"] + " " + Updater.get_latest_version()["version"])

        # Creating the message variable
        message = f"0x1de-NX is up to date!\n Current Version: {current_ver_out}"

        # Modifying the message variable if 0x1de-NX is out of date
        if CurrentVersionGlobal["version"] != Updater.get_latest_version()["version"]:
            message = f"Update needed!\nCurrent Version: {current_ver_out}\nLatest Version: {latest_ver_out}"

        # Outputting the message
        messagebox.showinfo("0x1de-NX | Updater", message)

    @staticmethod
    def is_outdated_client() -> bool:
        """Returns bool for if the client is outdated or not."""

        # Returning True if out of date
        if CurrentVersionGlobal["version"] != Updater.get_latest_version()["version"]:
            return True

        # Returning False if up to date
        return False
