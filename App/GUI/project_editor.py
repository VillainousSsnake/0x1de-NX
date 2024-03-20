# /App/GUI/project_editor.py
# Contains code for project editor

# Importing libraries and modules
from App.AppLib.texture_handler import TextureHandle
from PIL import ImageTk, Image
import customtkinter as ctk
from CTkMenuBar import *
import os


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

    # TODO: Configure and create children for each frame

    # Root mainloop (End of function)
    root.mainloop()
