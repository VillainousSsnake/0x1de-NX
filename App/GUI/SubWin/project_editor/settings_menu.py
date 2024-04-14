# /App/GUI/settings_menu.py

# Import statements
import customtkinter as ctk
from functools import partial
from App.AppLib.config import Config
from tkinter import filedialog


# ButtonFunc class (Adapted from AINB-Toolbox)
class ButtonFunc:

    @staticmethod
    def emulator_path_browse_button_command(app, emulator_path_entry):
        emulator_path = filedialog.askopenfile(
            title="Select Emulator EXE",
            filetypes=(
                ("Windows Executable File", "*.exe"),
                ("All Files", "")
            ),
        )
        if emulator_path is None:
            return 0
        else:
            emulator_path = emulator_path.name
            app.settings["emulator_path"] = emulator_path
            Config.overwrite_setting("emulator_path", emulator_path)
            emulator_path_entry.delete(0, "end")
            emulator_path_entry.insert(0, emulator_path)

    @staticmethod
    def ainb_to_code_option_menu_button_command(app, event=None):

        match event:

            case "JSON":

                app.settings['ainb_code_format'] = 'JSON'
                Config.overwrite_setting('ainb_code_format', event)

            case "YAML":

                app.settings['ainb_code_format'] = 'YAML'
                Config.overwrite_setting('ainb_code_format', event)

    @staticmethod
    def romfs_path_browse_button_command(app, romfs_path_entry):
        romfs_path = filedialog.askdirectory(title="Select Tears of the Kingdom RomFS Folder")
        if romfs_path == "":
            return 0
        else:
            app.settings["romfs_path"] = romfs_path
            Config.overwrite_setting("romfs_path", romfs_path)
            romfs_path_entry.delete(0, "end")
            romfs_path_entry.insert(0, romfs_path)


class _func:

    @staticmethod
    def focus_in_emulator_entry(emulator_path_label, event=None):
        emulator_path_label.configure(
            text="Emulator Path*"
        )

    @staticmethod
    def update_emulator_entry(app, emulator_path_entry, emulator_path_label, event=None):
        emulator_path = emulator_path_entry.get()
        app.settings["emulator_path"] = emulator_path
        Config.overwrite_setting("emulator_path", emulator_path)
        emulator_path_label.configure(
            text="Emulator Path"
        )

    @staticmethod
    def focus_in_romfs_entry(romfs_path_label, event=None):
        romfs_path_label.configure(
            text="Game Dump Location*"
        )

    @staticmethod
    def update_romfs_entry(app, romfs_path_entry, romfs_path_label, event=None):
        romfs_path = romfs_path_entry.get()
        app.settings["romfs_path"] = romfs_path
        Config.overwrite_setting("romfs_path", romfs_path)
        romfs_path_label.configure(
            text="Game Dump Location"
        )

    @staticmethod
    def font_size_entry_return_command(app, font_size_label, font_size_entry, event=None):
        Text = "Font Size"
        font_size_label.configure(
            text=Text
        )
        app.settings["font_size"] = font_size_entry.get()
        Config.overwrite_setting("font_size", font_size_entry.get())

    @staticmethod
    def font_size_entry_keys_command(font_size_label, event=None):
        Text = "Font Size*"
        font_size_label.configure(
            text=Text
        )


# Settings menu function
def settings_menu(app):

    window = ctk.CTkToplevel()
    window.geometry("525x300")

    scroll_frame = ctk.CTkScrollableFrame(master=window, width=10000000, fg_color="#242424")
    scroll_frame.pack(fill='both', side='left')

    romfs_path_label = ctk.CTkLabel(
        master=scroll_frame,
        text="Game Dump Location", anchor='w', width=135,
        corner_radius=5, fg_color="#3B8ED0"
    )
    romfs_path_label.grid(row=0, column=0, padx=20, pady=10)

    romfs_path_entry = ctk.CTkEntry(master=scroll_frame)
    if app.settings["romfs_path"] is None:
        romfs_path_entry.configure(placeholder_text="Eg. (D:\\Tears of the Kingdom\\romfs)")
    else:
        romfs_path_entry.insert(0, app.settings["romfs_path"])
    romfs_path_entry.grid(row=0, column=1, padx=20, pady=10)
    romfs_path_entry_command_partial = partial(_func.update_romfs_entry, app, romfs_path_entry, romfs_path_label)
    romfs_path_entry_focus_partial = partial(_func.focus_in_romfs_entry, romfs_path_label)
    romfs_path_entry.bind("<Return>", romfs_path_entry_command_partial)
    romfs_path_entry.bind("<Key>", romfs_path_entry_focus_partial)

    romfs_browse_command = partial(ButtonFunc.romfs_path_browse_button_command, app, romfs_path_entry)
    romfs_path_browse = ctk.CTkButton(
        scroll_frame,
        text="Browse...", fg_color="grey",
        command=romfs_browse_command,
    )
    romfs_path_browse.grid(row=0, column=3)

    # AINB-To-Code Setting
    ainb_to_code_format_label = ctk.CTkLabel(
        master=scroll_frame,
        text="AINB-To-Code Format", anchor='w', width=135,
        corner_radius=5, fg_color="#3B8ED0"
    )
    ainb_to_code_format_label.grid(row=2, column=0, padx=20, pady=10)

    ainb_to_code_option_menu_command = partial(ButtonFunc.ainb_to_code_option_menu_button_command, app)
    ainb_to_code_format_option_menu = ctk.CTkOptionMenu(
        master=scroll_frame,
        values=["YAML", "JSON"],
        command=ainb_to_code_option_menu_command,
    )
    ainb_to_code_format_option_menu.set(app.settings["ainb_code_format"])
    ainb_to_code_format_option_menu.grid(row=2, column=1, padx=20, pady=10)

    # Font size setting
    font_size_label = ctk.CTkLabel(
        master=scroll_frame,
        text="Font Size", anchor='w', width=135,
        corner_radius=5, fg_color="#3B8ED0"
    )
    font_size_label.grid(row=3, column=0, padx=20, pady=10)

    font_size_entry = ctk.CTkEntry(master=scroll_frame)
    font_size_entry.insert("0", app.settings["font_size"])
    font_size_entry.grid(row=3, column=1, padx=20, pady=10)
    font_size_entry_keys_command = partial(_func.font_size_entry_keys_command, font_size_label)
    font_size_entry_return_command = partial(_func.font_size_entry_return_command, app, font_size_label,
                                             font_size_entry)
    font_size_entry.bind("<Key>", font_size_entry_keys_command)
    font_size_entry.bind("<Return>", font_size_entry_return_command)

    # Emulator path setting
    emulator_path_label = ctk.CTkLabel(
        master=scroll_frame,
        text="Emulator EXE Path", anchor='w', width=135,
        corner_radius=5, fg_color="#3B8ED0"
    )
    emulator_path_label.grid(row=4, column=0, padx=20, pady=10)

    emulator_path_entry = ctk.CTkEntry(master=scroll_frame)
    if app.settings["emulator_path"] is None:
        emulator_path_entry.configure(placeholder_text="Eg. (D:\\EmulatorName\\emulator.exe)")
    else:
        emulator_path_entry.insert(0, app.settings["emulator_path"])
    emulator_path_entry.grid(row=4, column=1, padx=20, pady=10)
    emulator_path_entry_command_partial = partial(
        _func.update_emulator_entry,
        app,
        emulator_path_entry,
        emulator_path_label,
    )
    emulator_path_entry_focus_partial = partial(_func.focus_in_emulator_entry, emulator_path_label)
    emulator_path_entry.bind("<Return>", emulator_path_entry_command_partial)
    emulator_path_entry.bind("<Key>", emulator_path_entry_focus_partial)

    emulator_browse_command = partial(ButtonFunc.emulator_path_browse_button_command, app, emulator_path_entry)
    emulator_path_browse = ctk.CTkButton(
        scroll_frame,
        text="Browse...", fg_color="grey",
        command=emulator_browse_command,
    )
    emulator_path_browse.grid(row=4, column=3)
