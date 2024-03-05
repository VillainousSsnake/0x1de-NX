# /App/GUI/SubWin/new_project.py

# Importing modules and/or libraries
from App.AppLib.project_handler import ProjectHandler
from tkinter import filedialog, messagebox
from App.AppLib.updater import Updater
from functools import partial
import customtkinter as tk
from PIL import Image
import shutil
import os


# noinspection PyPep8Naming
class _func:
    @staticmethod
    def update_project_name_entry(project_name_entry, settings, event=None):
        text = project_name_entry.get()
        if text == "":
            return 1
        settings["Project Name"] = text + event.char

    @staticmethod
    def update_image(self):
        pass  # TODO: Stub


class ButtonFunc:
    @staticmethod
    def cancel(window):
        window.destroy()

    @staticmethod
    def create(settings, window):
        """
            settings = {
                "Project Name": None,
                "IconPath": None,
                "Create romfs folder": True,
                "Create README.txt": True,
            }
        """

        if settings["Project Name"] is None:
            messagebox.showinfo("Invalid Project Name", "Please fill out the Project name!")
            return 1

        project_dir = ProjectHandler.get_project_directory()

        new_project_dir = str(os.path.join(project_dir, settings["Project Name"]))
        info_json_path = os.path.join(new_project_dir, 'info.json')

        # Detecting if the project dir exists
        if os.path.exists(new_project_dir):
            ask_yes_no_popup = messagebox.askyesno(
                 "Project already exists",
                 "Do you want to overwrite a pre-existing project?",
                )
            if not ask_yes_no_popup:
                return 0
            else:
                shutil.rmtree(path=new_project_dir)

        # Creating the project dir
        if new_project_dir != "":   # Safety feature
            os.mkdir(new_project_dir)

        # Creating the romfs dir
        if settings["Create romfs folder"]:
            os.mkdir(os.path.join(new_project_dir, 'romfs'))

        # Creating the README.txt file
        readme_contents = settings["Project Name"] + ":\n\n" + "PLACEHOLDER"
        if settings["Create README.txt"]:
            with open(os.path.join(new_project_dir, "README.txt"), "w") as f_out:
                f_out.write(readme_contents)

        # Copying the image to the folder
        if settings["IconPath"] is not None:

            image_path = settings["IconPath"]
            image_file_name = os.path.basename(image_path)
            shutil.copyfile(image_path, os.path.join(new_project_dir, image_file_name))

        # Creating the info.json
        # TODO: Stub

        # Destroying the window
        window.destroy()

    @staticmethod
    def select_icon(icon_image, settings, event=None):
        image_fp = filedialog.askopenfile(title="Select Project Image...")

        if image_fp is None:    # Safety
            return 0

        image_fp = image_fp.name

        if not os.path.exists(image_fp):
            messagebox.showinfo("Invalid path", "The image path does not exist!")
            return 0

        settings["IconPath"] = image_fp

        icon_image.configure(
            image=tk.CTkImage(
                light_image=Image.open(image_fp),
                dark_image=Image.open(image_fp),
                size=(96, 96),
            )
        )


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
    window.resizable(False, False)

    window.focus_set()
    window.grab_set()

    # Configuring the menu widgets
    create_command = partial(ButtonFunc.create, settings, window)
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
    update_method = partial(_func.update_project_name_entry, project_name_entry, settings)
    project_name_entry.bind("<Key>", update_method)

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
    icon_command = partial(ButtonFunc.select_icon, icon_image, settings)
    icon_image.bind("<Button-1>", icon_command)

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


