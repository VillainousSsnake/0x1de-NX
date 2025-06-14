# /App/GUI/SubWin/main_menu/new_project.py

# Importing modules and/or libraries
from App.AppLib.project_handler import ProjectHandler
from tkinter import filedialog, messagebox
import App.AppLib.customtkinter as tk
from functools import partial
from PIL import Image
import shutil
import json
import os


# noinspection PyPep8Naming
class _func:
    @staticmethod
    def update_project_name_entry(project_name_entry, settings, event=None):
        text = project_name_entry.get()

        if text == "":
            return 1

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
            settings["Project Name"] = text + event.char
        else:
            settings["Project Name"] = text

    @staticmethod
    def update_create_romfs_checkbox(checkbox, settings):
        value = checkbox.get()
        if value == 1:
            value = True
        else:
            value = False
        settings["Create romfs folder"] = value

    @staticmethod
    def update_create_readme_checkbox(checkbox, settings):
        value = checkbox.get()
        if value == 1:
            value = True
        else:
            value = False
        settings["Create README.txt"] = value


class ButtonFunc:
    @staticmethod
    def cancel(window):
        window.destroy()

    @staticmethod
    def create(settings, window, app, segmented_button_menu_controller=None, root=None):
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
        image_file_name = None
        if settings["IconPath"] is not None:

            image_path = settings["IconPath"]
            image_file_name = os.path.basename(image_path)
            shutil.copyfile(image_path, os.path.join(new_project_dir, image_file_name))

        # Creating the info.json
        info_json_contents = {
            "Name": settings["Project Name"],
            "Version": "1.0.0",
            "Author": app.settings["author_name"],
            "Contributors": [],
            "Description": "Made with 0x1de-NX",
            "ThumbnailUri": image_file_name,
        }
        with open(os.path.join(new_project_dir, "info.json"), "w") as f_out:
            json.dump(info_json_contents, f_out)

        # Updating segmented_button_menu_controller
        if segmented_button_menu_controller is not None:
            segmented_button_menu_controller.hide_current_menu()
            segmented_button_menu_controller.update_projects_menu(segmented_button_menu_controller)

        # Opening project if segmented_button_menu_controller is None
        if segmented_button_menu_controller is None:
            app.variables["open_project_fp"] = new_project_dir

        # Destroying the window
        window.destroy()

        if root is not None:
            root.destroy()

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


def new_project(app, segmented_button_menu_controller=None, root=None):

    settings = {
        "Project Name": None,
        "IconPath": None,
        "Create romfs folder": True,
        "Create README.txt": True,
    }

    # Creating the window
    window = tk.CTkToplevel()
    window.title("0x1de-NX | New Project")
    window.geometry("600x300")
    window.resizable(False, False)

    window.focus_set()
    window.grab_set()

    # Configuring the menu widgets
    create_command = partial(ButtonFunc.create, settings, window, app, segmented_button_menu_controller, root)
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

    # Assigning the checkbox commands
    create_readme_checkbox_command = partial(
        _func.update_create_readme_checkbox,
        create_readme_checkbox,
        settings,
    )
    create_readme_checkbox.configure(command=create_readme_checkbox_command)

    create_romfs_folder_checkbox_command = partial(
        _func.update_create_romfs_checkbox,
        create_romfs_folder_checkbox,
        settings,
    )
    create_romfs_folder_checkbox.configure(command=create_romfs_folder_checkbox_command)
