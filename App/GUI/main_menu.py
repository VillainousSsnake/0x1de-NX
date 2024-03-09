# /App/GUI/main_menu.py
# Contains main menu code

# Importing SubWin modules
from App.GUI.SubWin.main_menu.open_project import open_project as subwin_open_project
from App.GUI.SubWin.main_menu.new_project import new_project as subwin_new_project
from App.GUI.SubWin.main_menu.import_tkcl import import_tkcl as subwin_import_tkcl

# Importing modules and libraries:
from App.AppLib.project_handler import ProjectHandler
from App.AppLib.plugin_handler import PluginHandler
from tkinter import messagebox, filedialog
from App.AppLib.updater import Updater
from App.AppLib.config import Config
from functools import partial
import customtkinter as ctk
from PIL import Image, ImageTk
import os


# _func class (Contains functions that the menu function uses)
# noinspection PyPep8Naming, PyUnusedLocal
class _func:
    @staticmethod
    def update_search_bar_projects_menu(self, segmented_button_controller, event=None):
        # Updating segmented_button_menu_controller
        segmented_button_controller.hide_current_menu()

        added_char = ""
        is_str = True

        match event.keycode:
            case 8:
                is_str = False

            case 9:
                is_str = False
            case 13:
                is_str = False
            case 16:
                is_str = False
            case 17:
                is_str = False

        if is_str:
            added_char = event.char

        search_query = self.get() + added_char

        if event.keycode == 8:
            search_query = self.get()[:len(self.get())-1]

        segmented_button_controller.update_projects_menu(
            segmented_button_controller,
            search_query=search_query
        )

    @staticmethod
    def highlight_labels_on_button_enter(info_label1=None, info_label2=None, button=None, event=None):
        fgc = "#144870"
        info_label1.configure(fg_color=fgc)
        info_label2.configure(fg_color=fgc)
        button.configure(fg_color=fgc)

    @staticmethod
    def highlight_labels_on_button_leave(info_label1=None, info_label2=None, button=None, event=None):
        fgc = "#242424"
        info_label1.configure(fg_color=fgc)
        info_label2.configure(fg_color=fgc)
        button.configure(fg_color=fgc)

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
    def __init__(self, master, root, app):
        self.segmented_buttons_controller = self
        self.object_list = list()
        self.variables = dict()
        self.master = master
        self.root = root
        self.app = app

    def create_projects_menu(self, segmented_button_controller):

        # Creating variables
        app = self.app
        root = self.root

        # Creating segmented_button_menu_controller.variables
        self.variables = {
            "Projects": ProjectHandler.get_projects(),
            "Enabled Mods": [],
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
        search_entry_command = partial(
            _func.update_search_bar_projects_menu,
            search_entry,
            segmented_button_controller
        )
        search_entry.bind("<Key>", search_entry_command)

        # Creating the new_project button
        new_project_command = partial(
            ButtonCommand.ProjectsMenu.new_project,
            root, app, self,
        )
        new_project_button = ctk.CTkButton(
            master=nav_frame,
            text="New Project",
            command=new_project_command,
        )
        new_project_button.grid(row=0, column=1)

        # Creating open_project button
        open_project_command = partial(ButtonCommand.ProjectsMenu.open_project, root, app)
        open_project_button = ctk.CTkButton(
            master=nav_frame,
            text="Open Project",
            command=open_project_command,
        )
        open_project_button.grid(row=0, column=2)

        # Creating install project from tkcl button
        import_tkcl_command = partial(ButtonCommand.ProjectsMenu.import_tkcl, root, app)
        import_tkcl = ctk.CTkButton(
            master=nav_frame,
            text="Import .TKCL",
            command=import_tkcl_command,
        )
        import_tkcl.grid(row=0, column=3)

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

            # Creating the image for the project
            if item["ThumbnailUri"] is not None:

                image_path = os.path.join(
                    item["ProjectFolder"],
                    os.path.basename(item["Filepath"]),
                    item["ThumbnailUri"],
                )

                if not os.path.exists(image_path):
                    image_path = os.path.join(os.getcwd(), "App", "Image", "img_not_found.jpg")

            else:

                image_path = os.path.join(os.getcwd(), "App", "Image", "img_not_found.jpg")

            # Creating the project image
            project_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(128, 128)
            )

            # Assigning the image to the project button
            project_button.configure(image=project_image)

            # Creating info_label_text
            info_label1_text = str(item["Author"]) + ", v" + str(item["Version"])
            info_label2_text = str(item["Filepath"])

            # Creating info label for author and version
            info_label1 = ctk.CTkLabel(
                master=project_button,
                text=info_label1_text,
                font=("monospace", 17),
                anchor="w"
            )
            info_label1.place(x=175, y=45)

            info_label2 = ctk.CTkLabel(
                master=project_button,
                text=info_label2_text,
                font=("monospace", 12, 'italic'),
                anchor="w",
            )
            info_label2.place(x=190, y=70)

            # The label highlight fix
            command_enter = partial(
                _func.highlight_labels_on_button_enter,
                info_label1,
                info_label2,
                project_button
            )
            command_leave = partial(
                _func.highlight_labels_on_button_leave,
                info_label1,
                info_label2,
                project_button
            )
            info_label1.bind("<Enter>", command_enter)
            info_label2.bind("<Enter>", command_enter)
            project_button.bind("<Enter>", command_enter)
            project_button.bind("<Leave>", command_leave)

        # If there was nothing in the projects list
        if len(self.variables["Projects"]) == 0:
            nothing_label = ctk.CTkLabel(
                master=scrollable_frame,
                text="There is nothing here...",
                height=400,
                font=("font", 20),
            )
            nothing_label.pack(fill="both")

    def update_projects_menu(self, segmented_button_controller, search_query=None):

        # Creating variables
        app = self.app
        root = self.root

        # Creating segmented_button_menu_controller.variables
        self.variables = {
            "Projects": ProjectHandler.get_projects(),
            "Enabled Mods": [],
        }

        # Changing the 'Projects' entry based on the search query variable
        new_projects_list = []

        if search_query is not None:

            for item in self.variables["Projects"]:
                if search_query in item["Name"]:
                    new_projects_list.append(item)

            self.variables["Projects"] = new_projects_list



        # Creating the navigation frame
        nav_frame = ctk.CTkFrame(
            master=self.master,
            fg_color="#242424"
        )
        nav_frame.pack(side="top", fill="x")
        self.object_list[0] = nav_frame

        # Creating a scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(
            master=self.master,
            fg_color="#242424",
            width=10000
        )
        scrollable_frame.pack(fill="both", side="right")
        self.object_list[1] = scrollable_frame

        # Creating the search_entry entry
        search_entry = ctk.CTkEntry(
            master=nav_frame,
            placeholder_text="Search Projects",
            width=155,
        )
        search_entry.grid(row=0, column=0)

        search_entry_command = partial(
            _func.update_search_bar_projects_menu,
            search_entry,
            segmented_button_controller
        )
        search_entry.bind("<Key>", search_entry_command)

        if search_query is not None:
            search_entry.insert('0', search_query)

        # Creating the new_project button
        new_project_command = partial(
            ButtonCommand.ProjectsMenu.new_project,
            root, app, self,
        )
        new_project_button = ctk.CTkButton(
            master=nav_frame,
            text="New Project",
            command=new_project_command,
        )
        new_project_button.grid(row=0, column=1)

        # Creating open_project button
        open_project_command = partial(ButtonCommand.ProjectsMenu.open_project, root, app)
        open_project_button = ctk.CTkButton(
            master=nav_frame,
            text="Open Project",
            command=open_project_command,
        )
        open_project_button.grid(row=0, column=2)

        # Creating install project from tkcl button
        import_tkcl_command = partial(ButtonCommand.ProjectsMenu.import_tkcl, root, app)
        import_tkcl = ctk.CTkButton(
            master=nav_frame,
            text="Import .TKCL",
            command=import_tkcl_command,
        )
        import_tkcl.grid(row=0, column=3)

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

            # Creating the image for the project
            if item["ThumbnailUri"] is not None:

                image_path = os.path.join(
                    item["ProjectFolder"],
                    os.path.basename(item["Filepath"]),
                    item["ThumbnailUri"],
                )

                if not os.path.exists(image_path):
                    image_path = os.path.join(os.getcwd(), "App", "Image", "img_not_found.jpg")

            else:

                image_path = os.path.join(os.getcwd(), "App", "Image", "img_not_found.jpg")

            # Creating the project image
            project_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(128, 128)
            )

            # Assigning the image to the project button
            project_button.configure(image=project_image)

            # Creating info_label_text
            info_label1_text = str(item["Author"]) + ", v" + str(item["Version"])
            info_label2_text = str(item["Filepath"])

            # Creating info label for author and version
            info_label1 = ctk.CTkLabel(
                master=project_button,
                text=info_label1_text,
                font=("monospace", 17),
                anchor="w"
            )
            info_label1.place(x=175, y=45)

            info_label2 = ctk.CTkLabel(
                master=project_button,
                text=info_label2_text,
                font=("monospace", 12, 'italic'),
                anchor="w",
            )
            info_label2.place(x=190, y=70)

            # The label highlight fix
            command_enter = partial(
                _func.highlight_labels_on_button_enter,
                info_label1,
                info_label2,
                project_button
            )
            command_leave = partial(
                _func.highlight_labels_on_button_leave,
                info_label1,
                info_label2,
                project_button
            )
            info_label1.bind("<Enter>", command_enter)
            info_label2.bind("<Enter>", command_enter)
            project_button.bind("<Enter>", command_enter)
            project_button.bind("<Leave>", command_leave)

        # If there was nothing in the projects list
        if len(self.variables["Projects"]) == 0:
            nothing_label = ctk.CTkLabel(
                master=scrollable_frame,
                text="There is nothing here...",
                height=400,
                font=("font", 20),
            )
            nothing_label.pack(fill="both")

    def create_plugins_menu(self):

        # Navigation frame
        nav_frame = ctk.CTkFrame(
            master=self.master,
            fg_color='#242424',
            width=10000,
        )
        nav_frame.pack(fill='x', side='top')
        self.object_list.append(nav_frame)

        # Scroll frame
        scroll_frame = ctk.CTkScrollableFrame(
            master=self.master,
            width=10000,
            fg_color='#242424',
        )
        scroll_frame.pack(fill="both", side='left')
        self.object_list.append(scroll_frame)

        # Navigation frame configuration
        import_plugin = ctk.CTkButton(
            master=nav_frame,
            text="Import Plugin",
        )
        import_plugin.pack(side="left")

        apply_plugins = ctk.CTkButton(
            master=nav_frame,
            text="Apply Plugins"
        )
        apply_plugins.pack(side='left')

        # Scroll frame configuration
        plugins_dict = PluginHandler.get_plugins()

        for key in plugins_dict:

            plugin_frame = ctk.CTkFrame(
                master=scroll_frame,
                height=100,
                fg_color="#242424"
            )
            plugin_frame.pack(side='top')

            plugin_button = ctk.CTkButton(
                master=plugin_frame,
                width=100000,
                fg_color='#2B2B2B',
                height=100,
                font=('monospace', 25, 'bold'),
                anchor='w',
                text=key,
            )
            plugin_button.pack(side='top', fill='both')

            plugin_checkbox = ctk.CTkCheckBox(
                master=plugin_button, text="", width=-10
            )
            if plugins_dict[key]:
                plugin_checkbox.select()
            plugin_checkbox.grid(row=2, column=1)

        if not plugins_dict:
            nothing_here_label = ctk.CTkLabel(
                master=scroll_frame,
                text="There is nothing here...",
                fg_color='#242424',
                font=("font", 20),
                height=400,
            )
            nothing_here_label.pack(fill='both')

    def create_settings_menu(self):
        pass  # TODO: Stub

    def create_community_menu(self):
        pass  # TODO: Stub

    def show_projects_menu(self):
        self.object_list[0].pack(side="top", fill="x")
        self.object_list[1].pack(side="left", fill="both")

    def show_plugins_menu(self):
        self.object_list[2].pack(fill='x', side='top')
        self.object_list[3].pack(fill='both', side='left')

    def show_settings_menu(self):
        pass  # TODO: Stub

    def show_community_menu(self):
        pass  # TODO: Stub

    def hide_current_menu(self):
        for obj in self.object_list:
            obj.pack_forget()

    def destroy_current_menu(self):
        for obj in self.object_list:
            obj.destroy()


# ButtonCommand class (Contains functions for button commands)
class ButtonCommand:
    class ProjectsMenu:
        @staticmethod
        def new_project(root, app, self):
            subwin_new_project(root, app, self)

        @staticmethod
        def open_project(root, app):
            subwin_open_project(root, app)

        @staticmethod
        def import_tkcl(root, app):
            subwin_import_tkcl(root, app)

    @staticmethod
    def segmented_button_menu(segmented_menu_controller, buttons_list, value):

        # Setting all buttons to the bg color
        for button in buttons_list:
            button.configure(fg_color="#2B2B2B")
            button.configure(hover_color='#144870')

        # Destroying the menu
        segmented_menu_controller.hide_current_menu()

        # Setting the correct button to the "selected" color and showing the menu
        match value:

            case "Projects":    # Projects button
                buttons_list[0].configure(fg_color="#1F6AA5")
                buttons_list[0].configure(hover_color="#1F6AA5")
                segmented_menu_controller.show_projects_menu()

            case "Plugins":     # Plugins button
                buttons_list[1].configure(fg_color="#1F6AA5")
                buttons_list[1].configure(hover_color="#1F6AA5")
                segmented_menu_controller.show_plugins_menu()

            case "Settings":
                buttons_list[2].configure(fg_color="#1F6AA5")
                buttons_list[2].configure(hover_color="#1F6AA5")
                segmented_menu_controller.show_settings_menu()

            case "Community":   # Community button
                buttons_list[3].configure(fg_color="#1F6AA5")
                buttons_list[3].configure(hover_color="#1F6AA5")
                segmented_menu_controller.show_community_menu()


# main_menu function
def main_menu(app):

    # Verifying if the romfs path is real
    _func.verify_romfs_path(app)

    # Setting theme
    ctk.set_appearance_mode(app.settings["current_theme"])

    # Creating root window
    root = ctk.CTk()
    root.title("0x1de-NX | Alpha v0.0.1")
    root.geometry("850x525+200+200")
    root.wm_iconbitmap()
    root.iconphoto(
        False,
        ImageTk.PhotoImage(file=r'C:\Users\ecrje\PycharmProjects\0x1de-NX\App\Image\0x1de.ico')
    )

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

    # Creating the segmented
    segmented_button_controller = SegmentedButtonMenu(menu_frame, root, app)

    # Creating all the menus
    segmented_button_controller.create_projects_menu(segmented_button_controller)
    segmented_button_controller.create_plugins_menu()
    segmented_button_controller.create_settings_menu()
    segmented_button_controller.create_community_menu()

    # Showing the project menu (Since it's the default)
    segmented_button_controller.show_projects_menu()

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
