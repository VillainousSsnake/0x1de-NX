# /App/GUI/project_editor.py
# Contains code for project editor

# Importing SubWin modules
from App.GUI.SubWin.project_editor.new_dialog import new_dialog as subwin_new_dialog

# Importing libraries and modules
from App.AppLib.texture_handler import TextureHandler
from App.AppLib.file_handler import FileHandler
import App.AppLib.customtkinter as ctk
from tkinter import ttk, messagebox
from tkinterdnd2 import DND_FILES
from PIL import ImageTk, Image
from functools import partial
from CTkMenuBar import *
import subprocess
import hashlib
import shutil
import os


# ProgFunc class
class ProgFunc:
    @staticmethod
    def save_project():
        pass    # TODO: Stub

    class FileEditor:
        def __init__(self,
                     master,
                     app,
                     tabs: list = None
                     ):
            self.tabview = ctk.CTkTabview(
                master,
                fg_color="#242424",
                height=99999999,
                width=99999999,
                anchor="w",
            )
            self.master = master
            self.app = app

            if tabs is not None:    # Creating the tabs
                for value in tabs:
                    self.tabview.insert("end", value)

            else:   # Creating the "nothing here" label
                self.nothing_opened_label = ctk.CTkLabel(
                    master=self.master,
                    text="Double click a file in the Project Tree to edit!",
                    anchor="center",
                    width=999999999,
                    height=999999999,
                    font=("monospace", 25, 'italic'),
                    text_color="grey",
                )
                self.nothing_opened_label.pack(anchor="center")

        def open_file(self, app, item_info) -> None:

            # Detecting the type of given input, and if it is a Directory then it exits the func
            if item_info['tags'][0] == "Directory":
                return None

            # Destroying nothing opened indicator label
            if self.nothing_opened_label.winfo_exists():
                self.nothing_opened_label.pack_forget()
                self.tabview.pack(side="top", anchor="w")

            # If statement for if the tab exists or not
            if item_info["text"] not in self.tabview._tab_dict:  # Creating tab because tab doesn't exist

                # Creating the close tab function
                def close_tab_command():
                    self.tabview.delete(item_info["text"])

                    # If the tabview doesn't have any tabs left
                    if self.tabview.get() == "":

                        # Resetting the tabview
                        self.tabview.destroy()
                        self.tabview = ctk.CTkTabview(
                            self.master,
                            fg_color="#242424",
                            height=99999999,
                            width=99999999,
                            anchor="w",
                        )

                        # Showing the nothing opened label
                        self.nothing_opened_label.pack(anchor="center")

                # Creating the tab
                tab = self.tabview.add(item_info["text"])

                # TODO: Create the close button for the tab

                # Displaying the file
                FileHandler.display_file_to_tabview_from_info(app, self.tabview, item_info, self)

            else:    # Switching tab to existing one because tab exists
                self.tabview.set(item_info["text"])

    class ProjectTreeView:
        @staticmethod
        def on_double_click(self, file_editor, app, event=None):
            curItem = self.focus()
            item_info = self.item(curItem)
            file_editor.open_file(app, item_info=item_info)

        @staticmethod
        def on_key(self: ttk.Treeview, file_editor, project_treeview, app, event=None):

            curItem = self.item(self.focus())

            # Detecting the key symbol
            if event.keysym == "Delete":    # If the key is "delete"

                # Asking for confirmation
                ok_cancel_prompt = messagebox.askokcancel(
                    "0x1de-NX | Delete File from Project (UNSAFE)",
                    "Are you sure you want to delete this file from the project?\nWARNING: THIS CANNOT BE UNDONE YET!!!"
                )

                # If confirmed
                if ok_cancel_prompt:

                    # Removing the item from the tabview
                    item_name = self.focus()
                    self.delete(item_name)
                    if curItem["text"] in file_editor.tabview._tab_dict:
                        file_editor.tabview.delete(curItem["text"])

                    if file_editor.tabview.get() == "":
                        file_editor.tabview.pack_forget()
                        file_editor.nothing_opened_label.pack(anchor="center")

                    # Getting the recently deleted directory
                    recently_deleted_dir = os.path.join(
                        os.getenv("LOCALAPPDATA"), "0x1de-NX", "_temp_", "_0_RECENTLY_0_DELETED_0_"
                    )

                    # Creating the recently deleted directory if it doesn't exist
                    if not os.path.exists(recently_deleted_dir):
                        os.makedirs(recently_deleted_dir)

                    # Creating the destination directory variables
                    folders_list = os.listdir(recently_deleted_dir)
                    dest_dir = os.path.join(recently_deleted_dir, str(len(folders_list)))

                    # Creating the destination directory
                    os.makedirs(dest_dir)

                    # Moving the file to the destination
                    shutil.move(src=curItem["values"][0], dst=dest_dir)

            elif event.keysym == "F2":
                pass    # TODO: Stub (Renaming files)

            elif event.keysym == "n" and event.state == 44:
                subwin_new_dialog(curItem, project_treeview, app)

        @staticmethod
        def on_right_click(self, event=None):

            # Setting selection to the item being hovered over
            treeview_item = self.identify("item", event.x, event.y)
            if treeview_item == "":
                return 0
            self.focus(treeview_item)
            self.selection_set(treeview_item)

            # Creating right click menu
            rc_menu = CustomDropdownMenu
            rc_menu.add_option(self=CustomDropdownMenu(widget=self), option="a")

            # Printing event
            print(event)    # TODO: Finish

    class TopNavFrame:
        @staticmethod
        def launch_totk_command(app):

            # Getting the project folder name
            sha1 = hashlib.sha1()
            sha1.update(os.path.basename(app.variables["open_project_fp"]).encode())
            project_folder_name = sha1.hexdigest()
            del sha1

            # Creating the folder path variables
            src_folder = os.path.join(app.variables["open_project_fp"])
            dest_folder = os.path.join(
                app.settings["mod_folder_path"],
                project_folder_name,
            )

            # Checking if the destination folder exists
            if os.path.exists(dest_folder):

                # Asking to delete the folder
                delete_dir_confirm = messagebox.askokcancel(
                    "0x1de-NX Folder already exists",
                    "0x1de-NX Folder already exists, do you want to over write it?"
                )

                if delete_dir_confirm:  # Deleting the folder
                    shutil.rmtree(dest_folder)

                else:   # Exiting function
                    return 0

            # Copying the folder into the mod folder location
            shutil.copytree(src=str(src_folder), dst=str(dest_folder))

            # Running the emulator
            emulator_path = str(app.settings["emulator_path"])
            rom_path = str(app.settings["rom_path"])
            command = emulator_path + ' "' + rom_path + '"'
            subprocess.call(command)

            # Deleting the mod folder after the emulator ran
            shutil.rmtree(dest_folder)

    class NavigationFrame:

        @staticmethod
        def project_tree_toggle_btn_command(
                self: ctk.CTkButton,
                project_tree_frame: ctk.CTkFrame
        ):
            button_color = self.cget("fg_color")

            if button_color == "#2B2B2B":   # The Project tree frame isn't expanded

                # Changing button color
                self.configure(fg_color="#4E5157", hover_color="#4E5157")

                # Expanding project tree frame
                project_tree_frame.configure(width=400)

                # Showing the widgets
                project_tree_frame.winfo_children()[0].pack(fill="x", side="top")
                project_tree_frame.winfo_children()[1].pack(fill="both", side="top")

            elif button_color == "#4E5157":     # The Project tree frame is expanded

                # Changing button color
                self.configure(fg_color="#2B2B2B", hover_color="#393B40")

                # Minimizing project tree frame
                project_tree_frame.configure(width=0)
                for widget in project_tree_frame.winfo_children():
                    widget.pack_forget()

    class FileButtonDropdown:
        """
        Holds commands for buttons in the file button dropdown
        (the "File" button as in the one on the title bar)
        """

        @staticmethod
        def new_project_command():
            pass    # TODO: Stub

        @staticmethod
        def new_command():
            pass    # TODO: Stub

        @staticmethod
        def open_command():
            pass    # TODO: Stub

        class export_project_as:
            @staticmethod
            def tkcl_package_command():
                pass    # TODO: Stub

            @staticmethod
            def nx_package_command():
                pass    # TODO: Stub

            @staticmethod
            def zip_file_command():
                pass    # TODO: Stub

        @staticmethod
        def close_project_command():
            pass    # TODO: Stub

        @staticmethod
        def rename_project_command():
            pass    # TODO: Stub

        @staticmethod
        def save_all_command():
            pass    # TODO: Stub

        @staticmethod
        def check_for_updates_command():
            pass    # TODO: Stub

        @staticmethod
        def exit_command():
            ProgFunc.save_project()
            exit()

    class ViewButtonDropdown:
        """
        Holds commands for buttons in the view button dropdown
        (the "View" button as in the one on the title bar)
        """

        @staticmethod
        def settings_command():
            pass    # TODO: Stub

        @staticmethod
        def toggle_console_command():
            pass    # TODO: Stub


# Defining project_editor
def project_editor(app):

    # Setting theme
    ctk.set_appearance_mode(app.settings["current_theme"])

    # Creating root window
    root = ctk.CTk()
    root.title("")
    root.geometry("1250x700")
    root.wm_iconbitmap()
    root.iconphoto(
        False,
        ImageTk.PhotoImage(file=os.path.join(os.getcwd(), "App", "Image", "0x1de.png"))
    )

    # Defining on_close function
    def on_close():
        root.destroy()
        app.returnStatement = "exit"

    # Assigning the buttons on the tkinter window top bar
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Creating navigation frame
    navigation_frame = ctk.CTkFrame(
        master=root,
        width=40,
    )
    navigation_frame.pack(
        side="left",
        fill='y',
    )

    # Creating project tree frame
    project_tree_frame = ctk.CTkFrame(
        master=root,
        width=400,
        height=9999999,
    )
    project_tree_frame.pack(
        side='left',
        anchor="nw",
        fill='y',
        padx=1,
    )

    # Creating top navigation frame
    top_nav_frame = ctk.CTkFrame(
        master=root,
        height=40,
    )
    top_nav_frame.pack(
        side="top",
        anchor="e",
        fill='x'
    )

    # Creating editor view frame
    editor_frame = ctk.CTkFrame(
        master=root,
        fg_color="#242424",
        width=9999999,
    )
    editor_frame.pack(fill='both', side='right')

    # Getting the textures and loading them into a list
    button_texture_dict = {}

    for tex_name in os.listdir(TextureHandler.get_texture_directory()):
        tex_path = os.path.join(TextureHandler.get_texture_directory(), tex_name)
        button_texture_dict[tex_name.replace(".png", "")] = Image.open(tex_path)

    ############################
    #    title_menu  config    #
    ############################

    # Creating title menu
    title_menu = CTkTitleMenu(
        master=root,
        title_bar_color="#1B2125",
    )

    # Creating and configuring the title menu's children
    file_btn_title_bar = title_menu.add_cascade("File")
    file_btn_title_bar.configure(
        text="File",
        width=0,
        fg_color="#1B2125",
        corner_radius=5,
        hover_color="#4E5157",
    )
    file_btn_title_bar.grid_configure(padx=10)

    view_btn_title_bar = title_menu.add_cascade("View")
    view_btn_title_bar.configure(
        text="View",
        width=0,
        fg_color="#1B2125",
        corner_radius=5,
        hover_color="#4E5157",
    )

    projects_btn_title_bar = title_menu.add_cascade("Projects")
    projects_btn_title_bar.configure(
        text="Projects",
        width=0,
        fg_color="#1B2125",
        corner_radius=5,
        hover_color="#4E5157",
    )

    plugins_btn_title_bar = title_menu.add_cascade("Plugins")
    plugins_btn_title_bar.configure(
        text="Plugins",
        width=0,
        fg_color="#1B2125",
        corner_radius=5,
        hover_color="#4E5157",
    )

    # Creating the menu's option lists
    file_dropdown_option_list = [
        ["New", "option"],
        ["Open", "option"],
        ["Save All", "option"],
        ["sep"],    # Seperator
        ["New Project", "option"],
        ["Rename Project", "option"],
        ["Export Project As", "submenu", ["TKCL Package", "NX Package", "Zip File"], 'arrow'],
        ["Close Project", "option"],
        ["sep"],    # Seperator
        ["Check For Updates", "option"],
        ["sep"],    # Seperator
        ["Exit", "option"],
    ]
    view_dropdown_option_list = [
        ["Settings", "option"],
        ["sep"],    # Seperator
        ["Toggle Console", "option"]
    ]

    # Creating the file button dropdown
    file_btn_dropdown = CustomDropdownMenu(
        master=title_menu,
        widget=file_btn_title_bar,
        pady=0
    )
    file_btn_dropdown.corner_radius = -5

    # Creating the view button dropdown
    view_btn_dropdown = CustomDropdownMenu(
        master=title_menu,
        widget=view_btn_title_bar,
        pady=0
    )
    view_btn_dropdown.corner_radius = -5

    # Creating options for each dropdown
    for item in file_dropdown_option_list:  # File btn dropdown

        if item[0] == "sep":  # Seperator
            file_btn_dropdown.add_separator()

        elif item[1] == "option":  # Option
            # Creating the text var
            btn_text = item[0]

            # Button Cosmetics
            if "arrow" in item:
                btn_text += "           >"

            # Creating the option
            file_btn_dropdown.add_option(
                btn_text,
                getattr(
                    ProgFunc.FileButtonDropdown,
                    item[0].replace(" ", "_").lower() + "_command"
                ),
            )

        elif item[1] == "submenu":  # Sub-Menu
            # Creating the text var
            btn_text = item[0]

            # Button Cosmetics
            if "arrow" in item:
                btn_text += "           >"

            # Creating the submenu
            submenu = file_btn_dropdown.add_submenu(btn_text)
            submenu.configure(corner_radius=10)

            for option in item[2]:
                submenu.add_option(
                    option,
                    command=getattr(
                        getattr(ProgFunc.FileButtonDropdown, item[0].replace(" ", "_").lower()),  # The class
                        option.replace(" ", "_").lower() + "_command"  # The command name
                    )
                )

        else:
            raise ValueError("The second option can only be 'option' or 'submenu' or 'sep', not " + item[1])

    # Creating options for each dropdown
    for item in view_dropdown_option_list:  # File btn dropdown

        if item[0] == "sep":  # Seperator
            view_btn_dropdown.add_separator()

        elif item[1] == "option":  # Option
            # Creating the text var
            btn_text = item[0]

            # Button Cosmetics
            if "arrow" in item:
                btn_text += "           >"

            # Creating the option
            view_btn_dropdown.add_option(
                btn_text,
                getattr(
                    ProgFunc.ViewButtonDropdown,
                    item[0].replace(" ", "_").lower() + "_command"
                ),
            )

        elif item[1] == "submenu":  # Sub-Menu
            # Creating the text var
            btn_text = item[0]

            # Button Cosmetics
            if "arrow" in item:
                btn_text += "           >"

            # Creating the submenu
            submenu = view_btn_dropdown.add_submenu(btn_text)
            submenu.configure(corner_radius=10)

            for option in item[2]:
                submenu.add_option(
                    option,
                    command=getattr(
                        getattr(ProgFunc.ViewButtonDropdown, item[0].replace(" ", "_").lower()),  # The class
                        option.replace(" ", "_").lower() + "_command"  # The command name
                    )
                )

        else:
            raise ValueError("The second option can only be 'option' or 'submenu' or 'sep', not " + item[1])

    ############################
    #   editor_frame  config   #
    ############################

    file_editor = ProgFunc.FileEditor(master=editor_frame, app=app)

    ################################
    #   navigation_frame  config   #
    ################################

    project_tree_toggle_nav_btn = ctk.CTkButton(    # Creating the project tree frame toggle button
        master=navigation_frame,
        text="",
        width=0,
        image=ctk.CTkImage(
            light_image=button_texture_dict["btn_003"],
            dark_image=button_texture_dict["btn_003"],
            size=(22, 19),
        ),
        fg_color="#4E5157",
        hover_color="#4E5157",
    )
    project_tree_toggle_nav_btn.configure(
        command=partial(
            ProgFunc.NavigationFrame.project_tree_toggle_btn_command,
            project_tree_toggle_nav_btn, project_tree_frame
        )
    )
    project_tree_toggle_nav_btn.pack()

    ##################################
    #   project_tree_frame  config   #
    ##################################

    project_tree_top_bar_frame = ctk.CTkFrame(
        project_tree_frame,
        height=75,
        width=400,
        fg_color="#2B2B2B"
    )
    project_tree_top_bar_frame.pack(fill="x", side="top")

    project_tree_treeview_frame = ctk.CTkFrame(
        project_tree_frame,
        width=400,
        fg_color="#2B2B2B",
    )
    project_tree_treeview_frame.pack(fill="both", side="top")

    # Configuring children of project_tree_top_bar_frame
    project_tree_title_label = ctk.CTkLabel(
        master=project_tree_top_bar_frame,
        text="Project Tree",
        font=("monospace", int(app.settings["font_size"]) + 5),
        anchor="w",
        width=400,
    )
    project_tree_title_label.pack(anchor="w")

    # Configuring children of project_tree_treeview_frame

    FONT = ("monospace", int(app.settings["font_size"]))
    ROW_HEIGHT = int(int(app.settings["font_size"]) * 2.5)

    # Minimum and maximum for font size for project Treeview widget
    if int(app.settings["font_size"]) > 25:
        FONT = ("monospace", 25)
        ROW_HEIGHT = 50
    if int(app.settings["font_size"]) < 18:
        FONT = None

    # Creating tree-view style
    tree_style = ttk.Style()
    tree_style.theme_use('default')
    tree_style.configure(
        "Treeview",
        background="#2B2B2B",
        foreground="white",
        fieldbackground="#2B2B2B",
        borderwidth=0,
    )

    # Applying fonts
    if FONT is not None:
        tree_style.configure(
            "Treeview",
            font=FONT,
            rowheight=ROW_HEIGHT
        )

    project_treeview = ttk.Treeview(    # Project treeview
        project_tree_treeview_frame,
        show="tree",
        height=99999999,
    )
    project_treeview.pack(fill="both", side="top")
    project_treeview.bind(
        "<Double-Button-1>",
        partial(ProgFunc.ProjectTreeView.on_double_click, project_treeview, file_editor, app)
    )
    project_treeview.bind("<Key>", partial(ProgFunc.ProjectTreeView.on_key,
                                           project_treeview,
                                           file_editor,
                                           project_treeview,
                                           app,
                                           )
                          )
    project_treeview.bind("<Button-3>", partial(ProgFunc.ProjectTreeView.on_right_click, project_treeview))

    # Inserting all the files and folders into tree view
    sub_directories = [x[0] for x in os.walk(app.variables["open_project_fp"])]
    counter = 0
    for folder_path in sub_directories:

        # Creating the item parameter variables
        folder_parent = folder_path.replace(
            os.path.basename(folder_path), ""
        )[:len(
            folder_path.replace(os.path.basename(folder_path), "")
        )-1]
        folder_iid = folder_path
        folder_text = chr(0x0001F4C1) + " " + os.path.basename(folder_path)

        if os.path.basename(folder_path) == "romfs":
            folder_text = chr(0x0001F4C1) + " 𝐫𝐨𝐦𝐟𝐬"

        # Making the parent an empty string if it is the first folder
        if counter == 0:
            folder_parent = ""

        # Creating the folder
        project_treeview.insert(
            parent=folder_parent,
            index=0,
            iid=folder_iid,
            text=folder_text,
            tags=["Directory"],
            values=[folder_path],
        )

        # Creating all the files in the folder and inserting them into the tree
        for file_name in os.listdir(folder_path):
            file_path = folder_path + "\\" + file_name
            if os.path.isfile(file_path):

                # Creating the item parameter variables
                file_parent = folder_path
                file_iid = file_path
                file_format = FileHandler.get_file_info_from_name(file_name)["format"]
                file_icon = FileHandler.get_file_info_from_name(file_name)["icon"]
                file_text = file_icon + " " + os.path.basename(file_path)

                # Making the parent an empty string if it is the first folder
                if counter == 0:
                    file_parent = ""

                # Creating the file
                project_treeview.insert(
                    parent=file_parent,
                    index="end",
                    iid=file_iid,
                    text=file_text,
                    tags=["File", file_format],
                    values=[file_path],
                )

        counter += 1

    # Defining the drop file command for the project treeview
    def drop_file_command(event=None):
        path = event.data
        if event.data[0] == "{":
            path = event.data[1:len(event.data) - 1]
        current_treeview_item = project_treeview.focus()

        if "." in current_treeview_item:
            current_treeview_item = os.path.split(current_treeview_item)[0]

        if current_treeview_item != "":

            if os.path.isfile(path):
                shutil.copy(
                    path,
                    os.path.join(app.variables["open_project_fp"], current_treeview_item)
                )
            elif os.path.isdir(path):
                yesnopopup = messagebox.askokcancel(
                    "0x1de-NX | Moving Folder",
                    "Are you sure you want to move this folder into the project?",
                )
                if not yesnopopup:
                    return 0
                shutil.move(
                    path,
                    os.path.join(app.variables["open_project_fp"], current_treeview_item)
                )
            else:
                raise TypeError("Unknown object")

        else:

            if os.path.isfile(path):
                shutil.copy(path, app.variables["open_project_fp"])
            elif os.path.isdir(path):
                yesnopopup = messagebox.askokcancel(
                    "0x1de-NX | Moving Folder",
                    "Are you sure you want to move this folder into the project?",
                )
                if not yesnopopup:
                    return 0
                shutil.move(path, app.variables["open_project_fp"])
            else:
                raise TypeError("Unknown object")

        # Deleting all the treeview items
        project_treeview.delete(*project_treeview.get_children())

        # Re-inserting all the items into the treeview
        sub_directories_ = [x[0] for x in os.walk(app.variables["open_project_fp"])]
        counter_ = 0
        for folder_path_ in sub_directories_:

            # Creating the item parameter variables
            folder_parent_ = folder_path_.replace(
                os.path.basename(folder_path_), ""
            )[:len(
                folder_path_.replace(os.path.basename(folder_path_), "")
            ) - 1]
            folder_iid_ = folder_path_
            folder_text_ = chr(0x0001F4C1) + " " + os.path.basename(folder_path_)

            if os.path.basename(folder_path_) == "romfs":
                folder_text_ = chr(0x0001F4C1) + " 𝐫𝐨𝐦𝐟𝐬"

            # Making the parent an empty string if it is the first folder
            if counter_ == 0:
                folder_parent_ = ""

            # Creating the folder
            project_treeview.insert(
                parent=folder_parent_,
                index=0,
                iid=folder_iid_,
                text=folder_text_,
                tags=["Directory"],
                values=[folder_path_],
            )

            # Creating all the files in the folder and inserting them into the tree
            for file_name_ in os.listdir(folder_path_):
                file_path_ = folder_path_ + "\\" + file_name_
                if os.path.isfile(file_path_):

                    # Creating the item parameter variables
                    file_parent_ = folder_path_
                    file_iid_ = file_path_
                    file_format_ = FileHandler.get_file_info_from_name(file_name_)["format"]
                    file_icon_ = FileHandler.get_file_info_from_name(file_name_)["icon"]
                    file_text_ = file_icon_ + " " + os.path.basename(file_path_)

                    # Making the parent an empty string if it is the first folder
                    if counter_ == 0:
                        file_parent_ = ""

                    # Creating the file
                    project_treeview.insert(
                        parent=file_parent_,
                        index="end",
                        iid=file_iid_,
                        text=file_text_,
                        tags=["File", file_format_],
                        values=[file_path_],
                    )

            counter_ += 1

    # Assigning the drag-and-drop commands for the project treeview
    project_tree_frame.drop_target_register(DND_FILES)
    project_tree_frame.dnd_bind('<<Drop>>', drop_file_command)

    ############################
    #   top_nav_frame config   #
    ############################

    launch_totk_button = ctk.CTkButton(
        master=top_nav_frame,
        text="",
        width=0,
        image=ctk.CTkImage(
            dark_image=button_texture_dict["btn_006"],
            light_image=button_texture_dict["btn_006"],
            size=(45, 45)
        ),
        fg_color="#2B2B2B",
        hover_color="#4E5157",
        command=partial(ProgFunc.TopNavFrame.launch_totk_command, app)
    )
    launch_totk_button.pack(side="right")

    # TODO: Configure and create children for each frame.
    #  top_nav_frame needs work. navigation_frame could use some work.

    # Root mainloop (End of function)
    root.mainloop()
