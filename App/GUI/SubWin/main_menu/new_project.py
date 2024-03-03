# /App/GUI/SubWin/new_project.py

# Importing modules and/or libraries
from App.AppLib.updater import Updater
from tkinter import filedialog
from functools import partial
import customtkinter as tk
from PIL import Image
import os


class _func:
    def update_image(self):
        pass  # TODO: Stub


class ButtonFunc:
    @staticmethod
    def cancel(window):
        window.destroy()

    @staticmethod
    def create():
        pass  # TODO: Stub


def new_project(root, app):

    settings = {
        "Project Name": None,
        "IconPath": None,
        "Create romfs folder": True,
        "Create README.txt": True,
    }

    # Creating the window
    window = tk.CTkToplevel()
    window.title("0x1de NX | " + Updater.get_current_version() + " | New Project")
    window.geometry("600x300")
    window.attributes("-topmost", True)
    window.resizable(False, False)

    window.focus_set()
    window.grab_set()

    # Configuring the menu widgets
    create_command = partial(ButtonFunc.create)
    create_button = tk.CTkButton(
        master=window,
        text="Create",
        command=create_command
    )
    create_button.pack(anchor="se", side="right")

    cancel_command = partial(ButtonFunc.cancel, window)
    cancel_button = tk.CTkButton(
        master=window,
        text="Cancel",
        command=cancel_command,
    )
    cancel_button.pack(anchor="se", side="left")

    project_name_label = tk.CTkLabel(
        master=window,
        text="Project Name: ",
    )
    project_name_label.pack(side="top", anchor='w')

    project_name_entry = tk.CTkEntry(
        master=window,
        placeholder_text="Enter project name here..."
    )
    project_name_entry.pack(side="top", fill='x')

    frame_1 = tk.CTkFrame(master=window, fg_color="#242424", width=10000)
    frame_1.pack(side="top", pady=30)

    icon_path_label = tk.CTkLabel(
        master=frame_1,
        text="Icon:"
    )
    icon_path_label.pack(side="top", anchor="w")

    icon_image = tk.CTkLabel(
        master=frame_1,
        text="",
        image=tk.CTkImage(
            light_image=Image.open(os.path.join(os.getcwd(), "App", "Image", "img_not_found.jpg")),
            dark_image=Image.open(os.path.join(os.getcwd(), "App", "Image", "img_not_found.jpg")),
            size=(96, 96),
        ),
    )
    icon_image.pack(side="left", anchor="n")

    create_readme_checkbox = tk.CTkCheckBox(
        master=frame_1,
        text="Create README.txt?",
    )
    create_readme_checkbox.pack(side="right", padx=35, pady=30)
    create_readme_checkbox.toggle()

    create_romfs_folder_checkbox = tk.CTkCheckBox(
        master=window,
        text="Create romfs folder?",
    )
    create_romfs_folder_checkbox.place(x=276, y=125)
    create_romfs_folder_checkbox.toggle()


