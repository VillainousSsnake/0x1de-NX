# App/FFLib/StandardArchive/__init__.py
# Contains Sarc class

# Importing dependencies
import os
import subprocess


# RESTBL class
class RESTBL:

    @staticmethod
    def generate_restbl_from_folder(folder_path: os.PathLike | str):
        """
        Generates a ResourceSizeTaBLe file for the given project path.
        :param folder_path: The input path for the folder that the function generates a rstb file from.
        """

        # Getting the path to restbl tool
        rstb_tool_path = os.path.join(os.getcwd(), "App", "Bin", "rstb_tool", "restbl.exe")

        # Getting the base command
        base_command = str(
            rstb_tool_path + ' --action single-mod --use-checksums --compress --mod-path "'
            + folder_path + '" --version '
        )

        # Running command with all game versions
        for version in ["100", "110", "111", "120", "121"]:
            command = base_command + version
            subprocess.run(command)
            print(f"restbl {version} generated")

        # Output
        print("Done!")

        pass    # TODO: Stub
