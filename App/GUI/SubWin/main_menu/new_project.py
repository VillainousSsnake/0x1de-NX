# /App/GUI/SubWin/new_project.py

# Importing modules and/or libraries
from App.AppLib.updater import Updater
from tkinter import filedialog
import customtkinter as ctk
import os


def new_project(root, app):

    # Creating the window
    window = ctk.CTkToplevel()
    window.title("0x1de NX | " + Updater.get_current_version() + " | New Project")
    window.geometry("600x400")
    window.attributes("-topmost", True)
    window.resizable(False, False)
