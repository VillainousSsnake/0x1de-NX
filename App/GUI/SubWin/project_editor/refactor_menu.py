# /App/GUI/SubWin/project_editor/refactor_menu.py
# Contains code for refactor dialog

# Importing modules, packages and libraries
import App.AppLib.customtkinter as ctk
from tkinter import messagebox
from functools import partial
import pathlib
import os


# Creating ButtonFunc class
class ButtonFunc:
    @staticmethod
    def cancel(window):
        window.destroy()

    @staticmethod
    def rename_entry_onkey_command(filetype: list, entry: ctk.CTkEntry, event=None):

        # Check if the event does not have a character
        if not event.char:

            # Making text color red if the file extension(s) are edited
            if pathlib.Path(entry.get()).suffixes == filetype:
                entry.configure(text_color="#DCE4EE")
            else:
                entry.configure(text_color="red")

    @staticmethod
    def rename(cur_item, entry, event=None):

        popup_msg = messagebox.askyesno(
            title="0x1de-NX | Rename File...",
            message="Rename File'" + os.path.basename(cur_item['values'][0]) + "' to '" + entry.get() + "'?",
        )

        if popup_msg:
            pass    # TODO: Write code to rename the file and replace the treeview item


# Defining rename_project_dialog function
def refactor_menu(cur_item, project_treeview, app):

    # Setting up the toplevel window
    window = ctk.CTkToplevel()
    window.title("0x1de-NX | Rename Object")
    window.resizable(False, False)
    window.geometry("600x300")

    # Setting focus on the window
    window.focus_set()
    window.grab_set()

    print(cur_item)  # TODO: Remove

    object_type = cur_item['tags'][0]

    match object_type:

        # In the case where the object is a folder
        case "Directory":

            pass    # TODO: Stub

        # In the case where the object is a file
        case "File":

            filename = os.path.basename(cur_item['values'][0])
            filetype = pathlib.Path(cur_item['values'][0]).suffixes

            # Creating and packing Info frame
            frame = ctk.CTkFrame(
                master=window,
            )
            frame.pack(anchor="nw", fill=ctk.BOTH)

            # Configuring the menu widgets
            file_name_label = ctk.CTkLabel(
                master=frame,
                text=str("Rename File '" + filename + "' to:"),
                padx=10, pady=10,
            )
            file_name_label.pack(side="top", anchor='w')

            file_name_entry = ctk.CTkEntry(
                master=frame,
                placeholder_text=filename,
            )
            file_name_entry.pack(side="top", fill='x')
            file_name_entry.insert(0, filename)

            file_name_entry.bind("<Key>",
                                 partial(
                                     ButtonFunc.rename_entry_onkey_command,
                                     filetype, file_name_entry
                                    )
                                 )

            rename_button = ctk.CTkButton(
                master=window,
                text="Rename",
                command=partial(ButtonFunc.rename, cur_item, file_name_entry)
            )
            rename_button.pack(anchor="se", side="right")

            cancel_button = ctk.CTkButton(
                master=window,
                text="Cancel",
                command=partial(ButtonFunc.cancel, window),
            )
            cancel_button.pack(anchor="se", side="left")

        case _:     # Throwing type error
            TypeError("Object is not a Directory or File")
