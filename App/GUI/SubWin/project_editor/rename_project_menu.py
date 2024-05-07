# /App/GUI/SubWin/project_editor/rename_project_menu.py
# Contains code for rename project dialog

# Importing modules, packages and libraries
from App.AppLib.file_handler import FileHandler
import App.AppLib.customtkinter as ctk
from tkinter import messagebox, ttk
from functools import partial
import os


# Creating _func class
class _func:
    def __init__(self):
        pass    # TODO: Stub


# Defining rename_project_dialog function
def rename_project_menu(current_item, project_treeview, app):

    # Setting up the toplevel window
    window = ctk.CTkToplevel()
    window.title("0x1de-NX | Rename Project")
    window.resizable(False, False)
    window.geometry("300x200")

    # Setting focus on the window
    window.focus_set()
    window.grab_set()

    # TODO: Finish


