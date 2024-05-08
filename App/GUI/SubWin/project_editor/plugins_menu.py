# /App/GUI/plugins_menu.py

# Import statements
from App.AppLib.plugin_handler import PluginHandler
import customtkinter as ctk
from functools import partial


# _func class (Contains program methods)
class _func:
    @staticmethod
    def close_window(root: ctk.CTk, window: ctk.CTkToplevel, app):
        window.destroy()
        root.destroy()
        app.returnStatement = "project_editor"

    @staticmethod
    def open_plugins_folder_command():
        pass    # TODO: Stub


# Plugins menu function
def plugins_menu(root, app):

    # Creating the window
    window = ctk.CTkToplevel()
    window.geometry("525x300")
    window.title("0x1de-NX | Plugins")
    window.resizable(False, False)

    # Assigning the close button on the window top bar
    window.protocol("WM_DELETE_WINDOW", partial(_func.close_window, root, window, app))

    # Setting focus on the window
    window.focus_set()
    window.grab_set()

    # Navigation frame
    nav_frame = ctk.CTkFrame(
        master=window,
        fg_color='#242424',
        width=10000,
    )
    nav_frame.pack(fill='x', side='top')

    # Scroll frame
    scroll_frame = ctk.CTkScrollableFrame(
        master=window,
        width=10000,
        fg_color='#242424',
    )
    scroll_frame.pack(fill="both", side='left')

    # Navigation frame configuration
    open_plugins_folder_button = ctk.CTkButton(
        master=nav_frame,
        text="Open Plugins Folder",
        command=_func.open_plugins_folder_command,
    )
    open_plugins_folder_button.pack(side="left")

    # Scroll frame configuration
    plugins_dict = PluginHandler.get_plugins()

    for key in plugins_dict:

        plugin_frame = ctk.CTkFrame(
            master=scroll_frame,
            height=100,
            fg_color="#242424"
        )
        plugin_frame.pack(side='top')

        plugin_button = ctk.CTkButton(
            master=plugin_frame,
            width=100000,
            fg_color='#2B2B2B',
            height=100,
            font=('monospace', 25, 'bold'),
            anchor='w',
            text=key,
        )
        plugin_button.pack(side='top', fill='both')

        plugin_checkbox = ctk.CTkCheckBox(
            master=plugin_button, text="", width=-10, onvalue=True, offvalue=False
        )
        if plugins_dict[key]:
            plugin_checkbox.select()
        plugin_checkbox.grid(row=2, column=1)

        # Defining and assigning the checkbox command
        def on_click():
            PluginHandler.set_plugin(key, bool(plugin_checkbox.get()))

        plugin_checkbox.configure(command=on_click)

    if not plugins_dict:
        nothing_here_label = ctk.CTkLabel(
            master=scroll_frame,
            text="There is nothing here...",
            fg_color='#242424',
            font=("font", 20),
            height=400,
        )
        nothing_here_label.pack(fill='both')
