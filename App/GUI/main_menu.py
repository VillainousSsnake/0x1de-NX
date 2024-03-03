# /App/GUI/main_menu.py
# Contains main menu code


# Importing modules and libraries:
from App.AppLib.project_handler import ProjectHandler
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


# SegmentedButtonMenu class
class SegmentedButtonMenu:
    def __init__(self, master):
        self.object_list = list()
        self.variables = dict()
        self.master = master

    def projects_menu_show(self):

        self.variables = {
            "Projects": ProjectHandler.get_projects(),
        }

        # Creating the navigation frame
        nav_frame = ctk.CTkFrame(
            master=self.master,
            fg_color="#242424"
        )
        nav_frame.pack(side="top", fill="x")
        self.object_list.append(nav_frame)

        # Creating a scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(
            master=self.master,
            fg_color="#242424",
            width=10000
        )
        scrollable_frame.pack(fill="both", side="right")
        self.object_list.append(scrollable_frame)

        # Creating the search_entry entry
        search_entry = ctk.CTkEntry(
            master=nav_frame,
            placeholder_text="Search Projects",
            width=155,
        )
        search_entry.grid(row=0, column=0)
        self.object_list.append(search_entry)

        # Creating the new_project button
        new_project_button = ctk.CTkButton(
            master=nav_frame,
            text="New Project"
        )
        new_project_button.grid(row=0, column=1)
        self.object_list.append(new_project_button)

        # Creating open_project button
        open_project_button = ctk.CTkButton(
            master=nav_frame,
            text="Open Project"
        )
        open_project_button.grid(row=0, column=2)
        self.object_list.append(open_project_button)

        # Creating install project from tkcl button
        install_tkcl = ctk.CTkButton(
            master=nav_frame,
            text="Install .TKCL"
        )
        install_tkcl.grid(row=0, column=3)
        self.object_list.append(install_tkcl)

        # Drawing the projects
        # Loop for every dictionary in Projects list
        for item in self.variables["Projects"]:

            # Creating the frame for the mod
            project_frame = ctk.CTkFrame(
                master=scrollable_frame,
                height=150,
                fg_color="#242424",
            )
            project_frame.pack(side="top", fill="x")
            self.object_list.append(project_frame)

            # Creating the overall project button
            project_button = ctk.CTkButton(
                master=project_frame,
                height=project_frame.cget("height"),
                text=str(item["Name"]) + "\n\n\n",
                anchor="w",
                font=("monospace", 25, "bold"),
                fg_color="#242424"
            )
            project_button.pack(fill="both")
            self.object_list.append(project_button)

            # Creating info_label_text
            info_label1_text = item["Author"] + ", v" + item["Version"]
            info_label2_text = item["Description"]

            # Creating info label for author and version
            info_label1 = ctk.CTkLabel(
                master=project_button,
                text=info_label1_text,
                font=("monospace", 15),
                anchor="w"
            )
            info_label1.place(x=30, y=45)
            self.object_list.append(info_label1)

            info_label2 = ctk.CTkLabel(
                master=project_button,
                text=info_label2_text,
                font=("monospace", 13),
                anchor="w",
                wraplength=300,
            )
            info_label2.place(x=35, y=70)

        # If there was nothing in the projects list
        if len(self.variables["Projects"]) == 0:

            nothing_label = ctk.CTkLabel(
                master=scrollable_frame,
                text="There is nothing here...\n Select New Project to get started!",
                height=400,
                font=("font", 20),
            )
            nothing_label.pack(fill="both")
            self.object_list.append(nothing_label)

    def destroy_current_menu(self):

        for obj in self.object_list:
            obj.destroy()

        self.variables = dict()


# ButtonCommand class (Contains functions for button commands)
class ButtonCommand:
    @staticmethod
    def segmented_button_menu(segmented_menu_controller, buttons_list, value):

        # Setting all buttons to the bg color
        for button in buttons_list:
            button.configure(fg_color="#2B2B2B")
            button.configure(hover_color='#144870')

        # Destroying the menu
        segmented_menu_controller.destroy_current_menu()

        # Setting the correct button to the "selected" color and showing the menu
        match value:

            case "Projects":    # Projects button
                buttons_list[0].configure(fg_color="#1F6AA5")
                buttons_list[0].configure(hover_color="#1F6AA5")
                segmented_menu_controller.projects_menu_show()

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

    # Segmented Button Menu frame
    menu_frame = ctk.CTkFrame(
        master=root,
        fg_color="#242424"
    )
    menu_frame.pack(fill="both", side="right")

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

    # Creating segmented_buttons_values
    segmented_buttons_values = [
        "Projects",
        "Plugins",
        "Settings",
        "Community",
    ]

    # Showing projects menu (Since that is the default open menu)
    segmented_button_controller = SegmentedButtonMenu(menu_frame)
    segmented_button_controller.projects_menu_show()

    # Assigning commands to each button in segmented_buttons_list
    for button in segmented_buttons_list:

        # Creating the command
        command = partial(
            ButtonCommand.segmented_button_menu,
            segmented_button_controller,
            segmented_buttons_list,
            segmented_buttons_values[segmented_buttons_list.index(button)]
        )

        # Assigning the command
        button.configure(command=command)

    # Root mainloop
    root.mainloop()
