# /App/GUI/main_menu.py
# Contains main menu code


# Importing modules and libraries:
from tkinter import messagebox, filedialog
from App.AppLib.updater import Updater
from App.AppLib.config import Config
from functools import partial
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
    @staticmethod
    def segmented_button_menu(buttons_list, value):

        # ['#36719F', '#144870']

        # Setting all buttons to the bg color
        for button in buttons_list:
            button.configure(fg_color="#2B2B2B")
            button.configure(hover_color='#144870')

        # Setting the correct button to the "selected" color and showing the menu
        match value:

            case "Projects":    # Projects button
                buttons_list[0].configure(fg_color="#1F6AA5")
                buttons_list[0].configure(hover_color="#1F6AA5")

            case "Plugins":     # Plugins button
                buttons_list[1].configure(fg_color="#1F6AA5")
                buttons_list[1].configure(hover_color="#1F6AA5")

            case "Settings":
                buttons_list[2].configure(fg_color="#1F6AA5")
                buttons_list[2].configure(hover_color="#1F6AA5")

            case "Community":   # Community button
                buttons_list[3].configure(fg_color="#1F6AA5")
                buttons_list[3].configure(hover_color="#1F6AA5")


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

    # Navigation frame
    navigation_frame = ctk.CTkFrame(master=root)
    navigation_frame.pack(fill="y", side="left")

    # Logo and Info frame
    info_frame = ctk.CTkFrame(
        master=navigation_frame,
        fg_color="#2B2B2B"
    )
    info_frame.pack(fill="x", side="top")

    ####################################
    #  Configuring Logo and Info Menu  #
    ####################################

    # Creating icon image
    info_icon_path = os.path.join(os.getcwd(), "App", "Image", "0x1de.ico")
    info_logo_image = ctk.CTkImage(
        light_image=Image.open(info_icon_path),
        dark_image=Image.open(info_icon_path),
        size=(64, 64)
    )

    # Creating button
    info_button = ctk.CTkButton(
        master=info_frame,
        image=info_logo_image,
        fg_color="#2B2B2B",
        font=("monospace", 25, "bold"),
        text="0x1de NX          \n",
        hover_color="#2B2B2B",
    )

    # Creating version label
    info_version_label = ctk.CTkLabel(
        master=info_button,
        fg_color="#2B2B2B",
        text=Updater.get_current_version(),
        font=ctk.CTkFont(size=14),
        anchor="w",
    )
    info_version_label.place(x=82, y=37)
    info_button.pack(fill="x", side="top")

    #################################
    #  Configuring Navigation Menu  #
    #################################

    # Creating segmented_button variables
    segmented_button_font = ctk.CTkFont(size=16)
    segmented_button_height = 40

    # Configuring Projects button
    nav_projects_button = ctk.CTkButton(
        master=navigation_frame,
        text="Projects",
        font=segmented_button_font,
        height=segmented_button_height,
        anchor="w",
        hover_color="#1F6AA5",
    )
    nav_projects_button.pack(side=ctk.TOP, fill="x", pady=1)

    # Configuring Plugins button
    nav_plugins_button = ctk.CTkButton(
        master=navigation_frame,
        text="Plugins",
        font=segmented_button_font,
        height=segmented_button_height,
        fg_color="#2B2B2B",
        anchor="w",
    )
    nav_plugins_button.pack(side=ctk.TOP, fill="x", pady=1)

    # Configuring Settings button
    nav_settings_button = ctk.CTkButton(
        master=navigation_frame,
        text="Settings",
        font=segmented_button_font,
        height=segmented_button_height,
        fg_color="#2B2B2B",
        anchor="w",
    )
    nav_settings_button.pack(side=ctk.TOP, fill="x", pady=1)

    # Configuring Community button
    nav_community_button = ctk.CTkButton(
        master=navigation_frame,
        text="Community",
        font=segmented_button_font,
        height=segmented_button_height,
        fg_color="#2B2B2B",
        anchor="w",
    )
    nav_community_button.pack(side=ctk.TOP, fill="x", pady=1)

    # Creating segmented_buttons_list
    segmented_buttons_list = [
        nav_projects_button,
        nav_plugins_button,
        nav_settings_button,
        nav_community_button,
    ]

    segmented_buttons_values = [
        "Projects",
        "Plugins",
        "Settings",
        "Community",
    ]

    # Assigning commands to each button in segmented_buttons_list
    for button in segmented_buttons_list:

        # Creating the command
        command = partial(
            ButtonCommand.segmented_button_menu,
            segmented_buttons_list,
            segmented_buttons_values[segmented_buttons_list.index(button)]
        )

        # Assigning the command
        button.configure(
            command=command
        )

    # Root mainloop
    root.mainloop()
