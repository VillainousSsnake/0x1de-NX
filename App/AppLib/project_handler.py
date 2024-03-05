# /App/AppLib/project_handler.py
# This is a plugin handler library

# Importing libraries
import json
import os


# ProjectHandler class
class ProjectHandler:
    @staticmethod
    def get_project_directory():
        # TODO: Replace os.getcwd() with os.getenv('LOCALAPPDATA')
        project_folder_path = os.path.join(
            os.getcwd(), "0x1de-NX", "Projects",
        )
        # Creating the directories if they don't exist
        if not os.path.exists(project_folder_path):
            os.makedirs(project_folder_path)
        return project_folder_path

    @staticmethod
    def get_projects():
        """Returns list of all projects and project information"""

        # Creating project_folder_path
        project_folder_path = ProjectHandler.get_project_directory()

        project_config_file_path = os.path.join(
            project_folder_path, "project.config"
        )

        # Creating the directories if they don't exist
        if not os.path.exists(project_folder_path):
            os.makedirs(project_folder_path)

        # creating the folder list
        folder_list = os.listdir(project_folder_path)

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
