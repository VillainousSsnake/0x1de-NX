# /App/GUI/main_menu.py
# Contains main menu code


# Importing modules and libraries:
from tkinter import messagebox, filedialog
from App.AppLib.config import Config
import customtkinter as ctk
import os


# _func class (Contains functions that the menu function uses)
# noinspection PyPep8Naming
class _func:

    @staticmethod
    def verify_romfs_path(app):

        # Detecting if the romfs_path is None
        if app.settings["romfs_path"] is None:

            # Asking user to provide romfs path
            continue_prompt = False

            # While continue prompt is no loop
            while continue_prompt is False:

                messagebox.showinfo("0x1de-NX Pop-up", "Please select your romfs folder.")
                romfs_folder = filedialog.askdirectory(title="Select RomFS Folder Path")

                if romfs_folder == "":

                    message = """Do you want to continue without a romfs dump?
        This will most likely cause a lot of errors in the future."""

                    continue_prompt = messagebox.askyesno(
                        "AINB-Toolbox Pop-up", message
                    )

                else:

                    app.settings["romfs_path"] = romfs_folder
                    Config.overwrite_setting("romfs_path", romfs_folder)
                    continue_prompt = True


# main_menu function
def main_menu(app):

    # Verifying if the romfs path is real
    _func.verify_romfs_path(app)

    # Setting theme
    ctk.set_appearance_mode(app.settings["current_theme"])

    # Creating root window
    root = ctk.CTk()
    root.title("AINB-Toolbox - VillainousSsnake - Alpha v0.0.1")
    root.geometry("850x525+200+200")

    # Defining on_close function
    def on_close():
        root.destroy()
        app.returnStatement = "exit"

    # Assigning the buttons on the tkinter window top bar
    root.protocol("WM_DELETE_WINDOW", on_close)

    # TODO: Code goes here

    # Root mainloop
    root.mainloop()
