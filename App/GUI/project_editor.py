# /App/GUI/project_editor.py
# Contains code for project editor

# Importing libraries and modules
from App.AppLib.project_handler import ProjectHandler
from App.AppLib.texture_handler import TextureHandler
from PIL import ImageTk, Image
from functools import partial
import customtkinter as ctk
from CTkMenuBar import *
import os


# ProgFunc class
class ProgFunc:
    @staticmethod
    def save_project():
        pass    # TODO: Stub

    class NavigationFrame:

        @staticmethod
        def project_tree_toggle_btn_command(
                self: ctk.CTkButton,
                project_tree_frame: ctk.CTkFrame
        ):
            button_color = self.cget("fg_color")

            if button_color == "#2B2B2B":   # The Project tree frame isn't expanded

                # Changing button color
                self.configure(fg_color="#4E5157", hover_color="#4E5157")

                # Expanding project tree frame
                project_tree_frame.configure(width=400)

            elif button_color == "#4E5157":     # The Project tree frame is expanded

                # Changing button color
                self.configure(fg_color="#2B2B2B", hover_color="#393B40")

                # Minimizing project tree frame
                project_tree_frame.configure(width=0)

    class FileButtonDropdown:
        """
        Holds commands for buttons in the file button dropdown
        (the "File" button as in the one on the title bar)
        """

        @staticmethod
        def new_project_command():
            pass    # TODO: Stub

        @staticmethod
        def new_command():
            pass    # TODO: Stub

        @staticmethod
        def open_command():
            pass    # TODO: Stub

        class export_project_as:
            @staticmethod
            def tkcl_package_command():
                pass    # TODO: Stub

            @staticmethod
            def nx_package_command():
                pass    # TODO: Stub

            @staticmethod
            def zip_file_command():
                pass    # TODO: Stub

        @staticmethod
        def close_project_command():
            pass    # TODO: Stub

        @staticmethod
        def rename_project_command():
            pass    # TODO: Stub

        @staticmethod
        def save_all_command():
            pass    # TODO: Stub

        @staticmethod
        def check_for_updates_command():
            pass    # TODO: Stub

        @staticmethod
        def exit_command():
            ProgFunc.save_project()
            exit()

    class ViewButtonDropdown:
        """
        Holds commands for buttons in the view button dropdown
        (the "View" button as in the one on the title bar)
        """

        @staticmethod
        def settings_command():
            pass    # TODO: Stub

        @staticmethod
        def toggle_console_command():
            pass    # TODO: Stub


# Defining project_editor
def project_editor(app):

    # Setting theme
    ctk.set_appearance_mode(app.settings["current_theme"])

    # Creating root window
    root = ctk.CTk()
    root.title("")
    root.geometry("1250x700")
    root.wm_iconbitmap()
    root.iconphoto(
        False,
        ImageTk.PhotoImage(file=os.path.join(os.getcwd(), "App", "Image", "0x1de.png"))
    )

    # Defining on_close function
    def on_close():
        root.destroy()
        app.returnStatement = "exit"

    # Assigning the buttons on the tkinter window top bar
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Creating navigation frame
    navigation_frame = ctk.CTkFrame(
        master=root,
        width=40,
    )
    navigation_frame.pack(
        side="left",
        fill='y',
    )

    # Creating project tree frame
    project_tree_frame = ctk.CTkFrame(
        master=root,
        width=400,
        height=9999999,
    )
    project_tree_frame.pack(
        side='left',
        anchor="nw",
        fill='y',
        padx=1,
    )

    # Creating top navigation frame
    top_nav_frame = ctk.CTkFrame(
        master=root,
        height=40,
    )
    top_nav_frame.pack(
        side="top",
        anchor="e",
        fill='x'
    )

    # Creating editor view frame
    editor_frame = ctk.CTkFrame(
        master=root,
        fg_color="#242424",
        width=9999999,
    )
    editor_frame.pack(fill='both', side='right')

    # Getting the textures and loading them into a list
    button_texture_dict = {}

    for tex_name in os.listdir(TextureHandler.get_texture_directory()):
        tex_path = os.path.join(TextureHandler.get_texture_directory(), tex_name)
        button_texture_dict[tex_name.replace(".png", "")] = Image.open(tex_path)

    # Creating title menu
    title_menu = CTkTitleMenu(
        master=root,
        title_bar_color="#1B2125",
    )

    # Creating and configuring the title menu's children
    file_btn_title_bar = title_menu.add_cascade("File")
    file_btn_title_bar.configure(
        text="File",
        width=0,
        fg_color="#1B2125",
        corner_radius=5,
        hover_color="#4E5157",
    )
    file_btn_title_bar.grid_configure(padx=10)

    view_btn_title_bar = title_menu.add_cascade("View")
    view_btn_title_bar.configure(
        text="View",
        width=0,
        fg_color="#1B2125",
        corner_radius=5,
        hover_color="#4E5157",
    )

    projects_btn_title_bar = title_menu.add_cascade("Projects")
    projects_btn_title_bar.configure(
        text="Projects",
        width=0,
        fg_color="#1B2125",
        corner_radius=5,
        hover_color="#4E5157",
    )

    plugins_btn_title_bar = title_menu.add_cascade("Plugins")
    plugins_btn_title_bar.configure(
        text="Plugins",
        width=0,
        fg_color="#1B2125",
        corner_radius=5,
        hover_color="#4E5157",
    )

    # Creating the menu's option lists
    file_dropdown_option_list = [
        ["New", "option"],
        ["Open", "option"],
        ["Save All", "option"],
        ["sep"],    # Seperator
        ["New Project", "option"],
        ["Close Project", "option"],
        ["Rename Project", "option"],
        ["Export Project As", "submenu", ["TKCL Package", "NX Package", "Zip File"], 'arrow'],
        ["sep"],    # Seperator
        ["Check For Updates", "option"],
        ["sep"],    # Seperator
        ["Exit", "option"],
    ]
    view_dropdown_option_list = [
        ["Settings", "option"],
        ["sep"],    # Seperator
        ["Toggle Console", "option"]
    ]

    # Creating the file button dropdown
    file_btn_dropdown = CustomDropdownMenu(
        master=title_menu,
        widget=file_btn_title_bar,
        pady=0
    )
    file_btn_dropdown.corner_radius = -5

    # Creating the view button dropdown
    view_btn_dropdown = CustomDropdownMenu(
        master=title_menu,
        widget=view_btn_title_bar,
        pady=0
    )
    view_btn_dropdown.corner_radius = -5

    # Creating options for each dropdown
    for item in file_dropdown_option_list:  # File btn dropdown

        if item[0] == "sep":  # Seperator
            file_btn_dropdown.add_separator()

        elif item[1] == "option":  # Option
            # Creating the text var
            btn_text = item[0]

            # Button Cosmetics
            if "arrow" in item:
                btn_text += "           >"

            # Creating the option
            file_btn_dropdown.add_option(
                btn_text,
                getattr(
                    ProgFunc.FileButtonDropdown,
                    item[0].replace(" ", "_").lower() + "_command"
                ),
            )

        elif item[1] == "submenu":  # Sub-Menu
            # Creating the text var
            btn_text = item[0]

            # Button Cosmetics
            if "arrow" in item:
                btn_text += "           >"

            # Creating the submenu
            submenu = file_btn_dropdown.add_submenu(btn_text)
            submenu.configure(corner_radius=10)

            for option in item[2]:
                submenu.add_option(
                    option,
                    command=getattr(
                        getattr(ProgFunc.FileButtonDropdown, item[0].replace(" ", "_").lower()),  # The class
                        option.replace(" ", "_").lower() + "_command"  # The command name
                    )
                )

        else:
            raise ValueError("The second option can only be 'option' or 'submenu' or 'sep', not " + item[1])

    # Creating options for each dropdown
    for item in view_dropdown_option_list:  # File btn dropdown

        if item[0] == "sep":  # Seperator
            view_btn_dropdown.add_separator()

        elif item[1] == "option":  # Option
            # Creating the text var
            btn_text = item[0]

            # Button Cosmetics
            if "arrow" in item:
                btn_text += "           >"

            # Creating the option
            view_btn_dropdown.add_option(
                btn_text,
                getattr(
                    ProgFunc.ViewButtonDropdown,
                    item[0].replace(" ", "_").lower() + "_command"
                ),
            )

        elif item[1] == "submenu":  # Sub-Menu
            # Creating the text var
            btn_text = item[0]

            # Button Cosmetics
            if "arrow" in item:
                btn_text += "           >"

            # Creating the submenu
            submenu = view_btn_dropdown.add_submenu(btn_text)
            submenu.configure(corner_radius=10)

            for option in item[2]:
                submenu.add_option(
                    option,
                    command=getattr(
                        getattr(ProgFunc.ViewButtonDropdown, item[0].replace(" ", "_").lower()),  # The class
                        option.replace(" ", "_").lower() + "_command"  # The command name
                    )
                )

        else:
            raise ValueError("The second option can only be 'option' or 'submenu' or 'sep', not " + item[1])

    # Creating children for navigation_frame
    project_tree_toggle_nav_btn = ctk.CTkButton(
        master=navigation_frame,
        text="",
        width=0,
        image=ctk.CTkImage(
            light_image=button_texture_dict["btn_003"],
            dark_image=button_texture_dict["btn_003"],
            size=(22, 19),
        ),
        fg_color="#2B2B2B",
        hover_color="#393B40",
    )
    project_tree_toggle_nav_btn.configure(
        command=partial(
            ProgFunc.NavigationFrame.project_tree_toggle_btn_command,
            project_tree_toggle_nav_btn, project_tree_frame
        )
    )
    project_tree_toggle_nav_btn.pack()

    # TODO: Configure and create children for each frame

    # Root mainloop (End of function)
    root.mainloop()
