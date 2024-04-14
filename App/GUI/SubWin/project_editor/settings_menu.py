# /App/GUI/settings_menu.py

# Import statements
import customtkinter as ctk
from functools import partial
from App.AppLib.config import Config
from tkinter import filedialog


# ButtonFunc class (Adapted from AINB-Toolbox)
class ButtonFunc:

    @staticmethod
    def mod_folder_path_browse_button_command(app, mod_folder_path_entry):
        mod_folder_path = filedialog.askdirectory(title="Select Tears of the Kingdom RomFS Folder")
        if mod_folder_path == "":
            return 0
        else:
            app.settings["mod_folder_path"] = mod_folder_path
            Config.overwrite_setting("mod_folder_path", mod_folder_path)
            mod_folder_path_entry.delete(0, "end")
            mod_folder_path_entry.insert(0, mod_folder_path)

    @staticmethod
    def rom_path_browse_button_command(app, rom_path_entry):
        rom_path = filedialog.askopenfile(
            title="Select Game ROM File",
            filetypes=(
                ("Nintendo Switch ROM File", ["*.xci", ".nsp"]),
            )
        )
        if rom_path == "":
            return 0
        else:
            rom_path = rom_path.name
            app.settings["rom_path"] = rom_path
            Config.overwrite_setting("rom_path", rom_path)
            rom_path_entry.delete(0, "end")
            rom_path_entry.insert(0, rom_path)

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
    def focus_in_mod_folder_entry(mod_folder_path_label, event=None):
        mod_folder_path_label.configure(
            text="TotK Mod Folder Path*"
        )

    @staticmethod
    def update_mod_folder_entry(app, mod_folder_path_entry, mod_folder_path_label, event=None):
        mod_folder_path = mod_folder_path_entry.get()
        app.settings["romfs_path"] = mod_folder_path
        Config.overwrite_setting("romfs_path", mod_folder_path)
        mod_folder_path_label.configure(
            text="TotK Mod Folder Path"
        )

    @staticmethod
    def focus_in_rom_entry(rom_path_label, event=None):
        rom_path_label.configure(
            text="TotK ROM Path*"
        )

    @staticmethod
    def update_rom_entry(app, rom_path_entry, rom_path_label, event=None):
        rom_path = rom_path_entry.get()
        app.settings["rom_path"] = rom_path
        Config.overwrite_setting("rom_path", rom_path)
        rom_path_label.configure(
            text="TotK ROM Path"
        )

    @staticmethod
    def focus_in_emulator_entry(emulator_path_label, event=None):
        emulator_path_label.configure(
            text="Emulator EXE Path*"
        )

    @staticmethod
    def update_emulator_entry(app, emulator_path_entry, emulator_path_label, event=None):
        emulator_path = emulator_path_entry.get()
        app.settings["emulator_path"] = emulator_path
        Config.overwrite_setting("emulator_path", emulator_path)
        emulator_path_label.configure(
            text="Emulator EXE Path"
        )

    @staticmethod
    def focus_in_romfs_entry(romfs_path_label, event=None):
        romfs_path_label.configure(
            text="RomFS Dump Path*"
        )

    @staticmethod
    def update_romfs_entry(app, romfs_path_entry, romfs_path_label, event=None):
        romfs_path = romfs_path_entry.get()
        app.settings["romfs_path"] = romfs_path
        Config.overwrite_setting("romfs_path", romfs_path)
        romfs_path_label.configure(
            text="RomFS Dump Path"
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

    # Creating the window
    window = ctk.CTkToplevel()
    window.geometry("525x300")
    window.title("0x1de-NX | Settings")
    window.resizable(False, False)

    # Setting focus on the window
    window.focus_set()
    window.grab_set()

    # Creating the scroll frame
    scroll_frame = ctk.CTkScrollableFrame(
        master=window,
        width=10000000,
        fg_color="#242424",
        height=250,
    )
    scroll_frame.pack(fill='both', side='top')

    # Creating close button
    close_button = ctk.CTkButton(
        master=window,
        text="Close Settings",
        command=window.destroy
    )
    close_button.pack(side="bottom", anchor="e")

    # Configuring settings
    #   # AINB-To-Code Setting
    #   ainb_to_code_format_label = ctk.CTkLabel(
    #       master=scroll_frame,
    #       text="AINB-To-Code Format", anchor='w', width=135,
    #       corner_radius=5, fg_color="#3B8ED0"
    #   )
    #   ainb_to_code_format_label.grid(row=2, column=0, padx=20, pady=10)
    #
    #   ainb_to_code_option_menu_command = partial(ButtonFunc.ainb_to_code_option_menu_button_command, app)
    #   ainb_to_code_format_option_menu = ctk.CTkOptionMenu(
    #       master=scroll_frame,
    #       values=["YAML", "JSON"],
    #       command=ainb_to_code_option_menu_command,
    #   )
    #   ainb_to_code_format_option_menu.set(app.settings["ainb_code_format"])
    #   ainb_to_code_format_option_menu.grid(row=2, column=1, padx=20, pady=10)

    # Font size setting
    font_size_label = ctk.CTkLabel(
        master=scroll_frame,
        text="Font Size", anchor='w', width=135,
        corner_radius=5, fg_color="#3B8ED0"
    )
    font_size_label.grid(row=0, column=0, padx=20, pady=10)

    font_size_entry = ctk.CTkEntry(master=scroll_frame)
    font_size_entry.insert("0", app.settings["font_size"])
    font_size_entry.grid(row=0, column=1, padx=20, pady=10)
    font_size_entry_keys_command = partial(_func.font_size_entry_keys_command, font_size_label)
    font_size_entry_return_command = partial(_func.font_size_entry_return_command, app, font_size_label,
                                             font_size_entry)
    font_size_entry.bind("<Key>", font_size_entry_keys_command)
    font_size_entry.bind("<Return>", font_size_entry_return_command)

    # RomFS path settings
    romfs_path_label = ctk.CTkLabel(
        master=scroll_frame,
        text="RomFS Dump Path", anchor='w', width=135,
        corner_radius=5, fg_color="#3B8ED0"
    )
    romfs_path_label.grid(row=1, column=0, padx=20, pady=10)

    romfs_path_entry = ctk.CTkEntry(master=scroll_frame)
    if app.settings["romfs_path"] is None:
        romfs_path_entry.configure(placeholder_text="Eg. (D:\\Tears of the Kingdom\\romfs)")
    else:
        romfs_path_entry.insert(0, app.settings["romfs_path"])
    romfs_path_entry.grid(row=1, column=1, padx=20, pady=10)
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
    romfs_path_browse.grid(row=1, column=3)

    # Emulator path setting
    emulator_path_label = ctk.CTkLabel(
        master=scroll_frame,
        text="Emulator EXE Path", anchor='w', width=135,
        corner_radius=5, fg_color="#3B8ED0"
    )
    emulator_path_label.grid(row=2, column=0, padx=20, pady=10)

    emulator_path_entry = ctk.CTkEntry(master=scroll_frame)
    if app.settings["emulator_path"] is None:
        emulator_path_entry.configure(placeholder_text="Eg. (D:\\EmulatorName\\emulator.exe)")
    else:
        emulator_path_entry.insert(0, app.settings["emulator_path"])
    emulator_path_entry.grid(row=2, column=1, padx=20, pady=10)
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
    emulator_path_browse.grid(row=2, column=3)
    
    # Rom Path Setting
    # rom path setting
    rom_path_label = ctk.CTkLabel(
        master=scroll_frame,
        text="TotK ROM Path", anchor='w', width=135,
        corner_radius=5, fg_color="#3B8ED0"
    )
    rom_path_label.grid(row=3, column=0, padx=20, pady=10)

    rom_path_entry = ctk.CTkEntry(master=scroll_frame)
    if app.settings["rom_path"] is None:
        rom_path_entry.configure(placeholder_text="Eg. (D:\\romName\\rom.nsp)")
    else:
        rom_path_entry.insert(0, app.settings["rom_path"])
    rom_path_entry.grid(row=3, column=1, padx=20, pady=10)
    rom_path_entry_command_partial = partial(
        _func.update_rom_entry,
        app,
        rom_path_entry,
        rom_path_label,
    )
    rom_path_entry_focus_partial = partial(_func.focus_in_rom_entry, rom_path_label)
    rom_path_entry.bind("<Return>", rom_path_entry_command_partial)
    rom_path_entry.bind("<Key>", rom_path_entry_focus_partial)

    rom_browse_command = partial(ButtonFunc.rom_path_browse_button_command, app, rom_path_entry)
    rom_path_browse = ctk.CTkButton(
        scroll_frame,
        text="Browse...", fg_color="grey",
        command=rom_browse_command,
    )
    rom_path_browse.grid(row=3, column=3)

    # mod_folder path setting
    mod_folder_path_label = ctk.CTkLabel(
        master=scroll_frame,
        text="TotK Mod Folder Path", anchor='w', width=135,
        corner_radius=5, fg_color="#3B8ED0"
    )
    mod_folder_path_label.grid(row=4, column=0, padx=20, pady=10)

    mod_folder_path_entry = ctk.CTkEntry(master=scroll_frame)
    if app.settings["mod_folder_path"] is None:
        mod_folder_path_entry.configure(placeholder_text="Eg. (D:\\mod_folderName\\mod_folder.exe)")
    else:
        mod_folder_path_entry.insert(0, app.settings["mod_folder_path"])
    mod_folder_path_entry.grid(row=4, column=1, padx=20, pady=10)
    mod_folder_path_entry_command_partial = partial(
        _func.update_mod_folder_entry,
        app,
        mod_folder_path_entry,
        mod_folder_path_label,
    )
    mod_folder_path_entry_focus_partial = partial(_func.focus_in_mod_folder_entry, mod_folder_path_label)
    mod_folder_path_entry.bind("<Return>", mod_folder_path_entry_command_partial)
    mod_folder_path_entry.bind("<Key>", mod_folder_path_entry_focus_partial)

    mod_folder_browse_command = partial(ButtonFunc.mod_folder_path_browse_button_command, app, mod_folder_path_entry)
    mod_folder_path_browse = ctk.CTkButton(
        scroll_frame,
        text="Browse...", fg_color="grey",
        command=mod_folder_browse_command,
    )
    mod_folder_path_browse.grid(row=4, column=3)
