# /App/GUI/main_menu.py
# Contains main menu code


# Importing modules and libraries:
from tkinter import messagebox, filedialog
from App.AppLib.updater import Updater
from App.AppLib.config import Config
import customtkinter as ctk
from PIL import Image
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

                messagebox.showinfo(
                    "0x1de-NX Pop-up",
                    "Please select your Zelda: Tears of the Kingdom RomFS dump folder.",
                )
                romfs_folder = filedialog.askdirectory(title="Select RomFS Folder Path")

                if romfs_folder == "":

                    message = """Do you want to continue without a romfs dump?
        This will most likely cause a lot of errors in the future."""

                    continue_prompt = messagebox.askyesno(
                        "0x1de-NX Pop-up", message
                    )

                else:

                    app.settings["romfs_path"] = romfs_folder
                    Config.overwrite_setting("romfs_path", romfs_folder)
                    continue_prompt = True


# ButtonCommand class (Contains functions for button commands)
class ButtonCommand:
    pass  # TODO: Stub


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

    #################################
    #  Configuring Navigation Menu  #
    #################################

    # Navigation frame
    navigation_frame = ctk.CTkFrame(master=root)
    navigation_frame.pack(fill="y", side="left")

    ####################################
    #  Configuring Logo and Info Menu  #
    ####################################

    # Logo and Info frame
    info_frame = ctk.CTkFrame(
        master=navigation_frame,
        fg_color="#2B2B2B"
    )
    info_frame.pack(fill="x", side="top")

    # Creating icon image
    info_icon_path = os.path.join(os.getcwd(), "App", "Image", "0x1de.ico")
    info_logo_image = ctk.CTkImage(
        light_image=Image.open(info_icon_path),
        dark_image=Image.open(info_icon_path),
        size=(48, 48)
    )

    # Creating button
    info_button = ctk.CTkButton(
        master=info_frame,
        image=info_logo_image,
        fg_color="#2B2B2B",
        font=("monospace", 17, "bold"),
        text="0x1de NX          \n",
        hover_color="#2B2B2B",
    )

    # Creating version label
    info_version_label = ctk.CTkLabel(
        master=info_button,
        fg_color="#2B2B2B",
        text=Updater.get_current_version(),
        font=ctk.CTkFont(size=10, family="monospace"),
        anchor="w",
    )
    info_version_label.place(x=65, y=25)
    info_button.pack(fill="x", side="top")

    # Root mainloop
    root.mainloop()
