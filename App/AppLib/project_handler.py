# /App/AppLib/project_handler.py
# This is a plugin handler module

# Importing libraries
from tkinter import filedialog
from functools import partial
import json
import os


# ProjectHandler class
class ProjectHandler:
    @staticmethod
    def get_project_directory() -> str:
        """Returns the project directory path"""

        # Creating the project folder path
        project_folder_path = os.path.join(
            os.getenv('LOCALAPPDATA'), "0x1de-NX", "Projects",
        )

        # Creating the directories if they don't exist
        if not os.path.exists(project_folder_path):
            os.makedirs(project_folder_path)

        # Returning the project folder path
        return project_folder_path

    @staticmethod
    def get_projects() -> list:
        """Returns list of all projects and project information"""

        # Creating project_folder_path
        project_folder_path = ProjectHandler.get_project_directory()

        project_config_file_path = os.path.join(
            project_folder_path, "project.config"
        )

        # Creating the directories if they don't exist
        if not os.path.exists(project_folder_path):
            os.makedirs(project_folder_path)

        # Creating the project config file if it doesn't exist
        if not os.path.exists(project_config_file_path):

            folder_list = os.listdir(project_folder_path)

            output_list = []

            # For every folder in folder_list
            for item in folder_list:

                # Detecting if the mod has info.json
                if os.path.exists(os.path.join(project_folder_path, item, "info.json")):

                    with open(os.path.join(project_folder_path, item, "info.json")) as f_in:
                        mod_info = json.load(f_in)

                    mod_info["Filepath"] = os.path.join("~0x1de-NX", "Projects", item)
                    mod_info["ProjectFolder"] = project_folder_path

                else:

                    mod_info = {
                        "Name": item,
                        "ProjectFolder": project_folder_path,
                        "Filepath": os.path.join("~0x1de-NX", "Projects", item),
                        "Version": "Unknown",
                        "Author": "Unknown",
                        "Contributors": None,
                        "Description": None,
                        "ThumbnailUri": None,
                    }

                output_list.append(mod_info)

            return output_list

    @staticmethod
    def get_projects_menu_dropdown(root, app) -> list:
        """
        Returns list of options for the projects menu dropdown, and the command for the option.
        This makes it possible to calculate existing projects in real time, without having to restart.
        :return: [["Option Name", OpenProjectWithOptionName], ...]
        """

        # Creating the open project function
        def open_command(root_, app_, project_path):

            if project_path is None:

                # Asking user for the project folder
                folder_select = filedialog.askdirectory(
                    initialdir=ProjectHandler.get_project_directory(),
                    title="Open Folder...",
                    mustexist=True,
                )

                # Detecting if the user canceled
                if folder_select == "":
                    return 0

                # Setting project_path to the given directory path
                project_path = folder_select

            # Setting the open project variable to the project path
            app_.variables["open_project_fp"] = project_path

            # Exiting the current menu and summoning the next one
            root_.destroy()
            app_.returnStatement = "project_editor"

        # Getting all projects
        projects_info_list = ProjectHandler.get_projects()
        projects_list = list()

        # Loop for every info dict in the list of info dicts
        for project_info in projects_info_list:

            # Getting the command
            project_open_command = partial(
                open_command,
                root, app, os.path.join(project_info["ProjectFolder"], project_info["Name"])
            )

            # Creating the list item
            project_list_item = [project_info["Name"], project_open_command]

            # Appending the list item
            projects_list.append(project_list_item)

        return projects_list
