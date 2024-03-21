# /App/GUI/project_editor.py
# Contains code for project editor

# Importing libraries and modules
from App.AppLib.texture_handler import TextureHandle
from PIL import ImageTk, Image
import customtkinter as ctk
from CTkMenuBar import *
import os


# ProgFunc class
class ProgFunc:
    class FileButtonDropdown:
        """
        Holds commands for buttons in the file button dropdown
        (the file button as in the one on the title bar)
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

        @staticmethod
        def save_as_command():
            pass    # TODO: Stub

        @staticmethod
        def recent_projects_command():
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
        def export_command():
            pass    # TODO: Stub

        @staticmethod
        def exit_command():
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

    for tex_name in os.listdir(TextureHandle.get_texture_directory()):
        tex_path = os.path.join(TextureHandle.get_texture_directory(), tex_name)
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
        ["New Project", "option"],
        ["New", "option"],
        ["Open", "option"],
        ["Save As", "submenu", ["TKCL Package", "0x1de NX Package", "Zip File"]],
        ["Recent Projects", "option"],
        ["Close Project", "option"],
        ["Rename Project", "option"],
        ["Save All", "option"],
        ["Check For Updates", "option"],
        ["Export", "option"],
        ["Exit", "option"],
    ]

    # Creating the title bars children's dropdowns
    file_btn_dropdown = CustomDropdownMenu(
        master=title_menu,
        widget=file_btn_title_bar,
    )

    # Creating options for each dropdown
    for item in file_dropdown_option_list:  # File btn dropdown

        if item[1] == "option": # Option
            file_btn_dropdown.add_option(
                item[0],
                getattr(
                    ProgFunc.FileButtonDropdown,
                    item[0].replace(" ", "_").lower() + "_command"
                )
            )

        elif item[1] == "submenu":  # Sub-Menu

            submenu = file_btn_dropdown.add_submenu(item[0])

            for option in item[2]:
                submenu.add_option(
                    option,
                    command=getattr(
                        getattr(ProgFunc.FileButtonDropdown, item[0].replace(" ", "_").lower()),    # The class
                        option.replace(" ", "_").lower() + "_command"                               # The command name
                    )
                )

        elif item[0] == "sep":
            file_btn_dropdown.add_separator()

        else:
            raise ValueError("The second option can only be 'option' or 'submenu' or 'sep', not " + item[1])

    # TODO: Configure and create children for each frame

    # Root mainloop (End of function)
    root.mainloop()
