# App/FFLib/StandardArchive/__init__.py
# Contains Sarc class

# Importing dependencies
import App.AppLib.customtkinter as ctk
from tkinter import ttk
import subprocess
import os


# RESTBL class
class RESTBL:

    @staticmethod
    def generate_restbl_from_folder(folder_path: os.PathLike | str) -> None:
        """
        Generates a ResourceSizeTaBLe file for the given project path and shows progress with a toplevel window.
        :param folder_path: The input path for the folder that the function generates a rstb file from.
        """

        # Creating toplevel window
        window = ctk.CTkToplevel()
        window.title("Generating RESTBL Files...")
        window.geometry("400x100")
        window.attributes("-topmost", True)

        # Creating progress bar
        progress_bar = ttk.Progressbar(
            master=window,
            orient="horizontal",
            mode='determinate',
            length=400,
        )
        progress_bar.pack(side="top")

        # Creating progress label
        progress_label = ctk.CTkLabel(
            master=window,
            text="Generating 'ResourceSizeTable.Product.100.rsizetable.zs'...",
            anchor="w",
            width=300,
        )
        progress_label.pack(side="top")

        # Getting the path to restbl tool
        rstb_tool_path = os.path.join(os.getcwd(), "App", "Bin", "rstb_tool", "restbl.exe")

        # Getting the base command
        base_command = str(
            rstb_tool_path + ' --action single-mod --use-checksums --compress --mod-path "'
            + folder_path + '" --version '
        )

        # Running command with all game versions
        for version in ["100", "110", "111", "120", "121"]:
            window.update()
            progress_label.configure(text=f"Generating 'ResourceSizeTable.Product.{version}.rsizetable.zs'...")
            progress_bar["value"] += 20
            window.update()
            command = base_command + version
            subprocess.run(command)
            window.update()

        progress_bar.stop()

        # Destroying the window
        window.destroy()

        # Returning None
        return None
