# Importing custom libraries
from Project.FileFormatLibrary.ZStd.zstd import *
from Project.FileFormatLibrary.SArc.sarchive import *

# Importing external libraries
import turtle
from tkinter import filedialog
import os

_Config = {
    "tempDir": os.path.join(os.getcwd(), "Project", "__Cache__", "_temp_"),
    "fileDropdown": True,  # This is because it will be set to False when file_onclick()
                           # is set to the onclick function of fileBtn
    "fileOpen": False,
    "currentFilepath": "",
    "displayingFile": False,
    "displayingFileState": "",

}
# Configuring global variables
_FileConfig = {
    "basename": "",
    "filepath": "",
    "decompressedFiletype": "",
    "decompressedFileContents": "",
    "isExpanded": False,
}


# The Program method
def file_editor(self):

    # Initializing
    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    # Configuring the window
    window = turtle.Screen()
    window.delay(0)
    window.title("0x1de NX - VERSION: 0.0.1 - File Editor")
    turtleCanvas = window.getcanvas()
    root = turtleCanvas.winfo_toplevel()
    root.iconbitmap(os.path.join(os.getcwd(), "Project", "Screen", "Texture", "main", "0x1de.ico"))

    def on_close():
        turtle.bye()
        self.returnStatement = "Closed"

    root.protocol("WM_DELETE_WINDOW", on_close)
    window.bgcolor("#131642")

    # Creating the Screen pen
    pen = turtle.Turtle()
    pen.ht()
    pen.pu()
    pen.speed(0)

    # Configuring Buttons
    fileBtn = turtle.Turtle()
    fileBtn.pu()
    fileBtn.speed(0)

    openBtn = turtle.Turtle()
    openBtn.pu()
    openBtn.speed(0)

    newBtn = turtle.Turtle()
    newBtn.pu()
    newBtn.speed(0)

    exitToMainBtn = turtle.Turtle()
    exitToMainBtn.pu()
    exitToMainBtn.speed(0)

    closeFileBtn = turtle.Turtle()
    closeFileBtn.pu()
    closeFileBtn.speed(0)
    closeFileBtn.ht()

    # Configuring textures
    fileBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "file_editor",
        "fileBtn.gif"
    )
    openBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "file_editor",
        "openBtn.gif"
    )
    newBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "file_editor",
        "newBtn.gif"
    )
    exitToMainBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "file_editor",
        "exitToMainMenu.gif"
    )
    closeFileBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "file_editor",
        "closeBtn.gif"
    )

    # Registering the textures
    window.register_shape(fileBtnTex)
    window.register_shape(openBtnTex)
    window.register_shape(newBtnTex)
    window.register_shape(exitToMainBtnTex)
    window.register_shape(closeFileBtnTex)

    # Applying the texture
    fileBtn.shape(fileBtnTex)
    openBtn.shape(openBtnTex)
    newBtn.shape(newBtnTex)
    exitToMainBtn.shape(exitToMainBtnTex)
    closeFileBtn.shape(closeFileBtnTex)

    # Creating lists for the buttons
    fileDropdownButtons = (openBtn,
                           newBtn)

    # Configuring the button onclick methods
    def file_onclick(x, y):

        global _Config

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        if _Config["fileDropdown"] is False:
            _Config["fileDropdown"] = True
        else:
            _Config["fileDropdown"] = False

    def open_onclick(x, y):

        global _Config

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        filetypes = (
            ('ZStandard File', '*.zs'),
            ('All Files', '*.*'),
        )

        filepath = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select a File",
            filetypes=filetypes,
        )

        if filepath != "":
            _Config["fileOpen"] = True

        else:
            _Config["fileOpen"] = False
            return -1

        _Config["currentFilepath"] = filepath

    def new_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        # TODO: write new_onclick function

    def exit_to_main_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        turtle.bye()
        self.returnStatement = "MAIN_MENU"

    def close_file_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        # TODO: write new_onclick function

    # Applying the button onclick methods
    fileBtn.onclick(file_onclick, 1)
    openBtn.onclick(open_onclick, 1)
    newBtn.onclick(new_onclick, 1)
    exitToMainBtn.onclick(exit_to_main_onclick, 1)
    closeFileBtn.onclick(close_file_onclick, 1)

    # Program Functions:
    def configure_file():

        # Importing global variables
        global _FileConfig

        # Configuring the filepath to the file
        _FileConfig["filepath"] = _Config["currentFilepath"]

        # Configuring the name of the file
        basename = str(os.path.basename(_Config["currentFilepath"]))
        _FileConfig["basename"] = os.path.basename(_Config["currentFilepath"])

        # Configuring the decompressed filetype of the ZStandard file
        decompressedFiletype = basename.split(".")[1]
        _FileConfig["decompressedFiletype"] = decompressedFiletype

        # Configuring the decompressed contents of the file

        # If the file is a ZStandard file
        if 'zs' in _FileConfig["basename"]:
            # Setting the dictionary based on what format the decompressed file will be
            dictionary = ""

            if _FileConfig["decompressedFiletype"] == "pack":
                dictionary = os.path.join(os.getcwd(), "Project", "__Cache__", "_dict_", "pack.zsdic")

            elif _FileConfig["decompressedFiletype"] == "byml":
                dictionary = os.path.join(os.getcwd(), "Project", "__Cache__", "_dict_", "bcett.byml.zsdic")

            elif _FileConfig["decompressedFiletype"] == "bcett":
                dictionary = os.path.join(os.getcwd(), "Project", "__Cache__", "_dict_", "bcett.byml.zsdic")

            # Getting the decompressed contents of the file
            fileContents = ZSTD.read(_Config["currentFilepath"], dictionary)
            _FileConfig["decompressedFileContents"] = fileContents

    def get_contents_to_draw(mode='root'):

        if mode == "root":

            if ".zs" in _FileConfig["basename"]:

                if _FileConfig["decompressedFiletype"] == "pack":

                    # Grabbing the list of files in the SArc
                    sarcContents = SARC.read_data(_FileConfig["decompressedFileContents"], 'l')

                    # formatting sarcContents to sarcKeys
                    sarcKeys = []

                    for key in sarcContents.mapping.keys():
                        sarcKeys.append(key)

                    # formatting sarcKeys into sarcRootFolders
                    sarcRootFolders = []
                    sarcSplitKeys = []

                    for key in sarcKeys:
                        splitKey = key.split("/")
                        sarcSplitKeys.append(splitKey)

                    for key in sarcSplitKeys:
                        if key[0] not in sarcRootFolders:
                            sarcRootFolders.append(key[0])

                    # formatting sarcRootFolders into output
                    output = ""

                    for rootFolder in sarcRootFolders:
                        output += '\n' + rootFolder

                    # Returning output
                    return output

                    # TODO: Finish get_contents_to_draw when decompressed format is pack

    def draw_file():

        # Importing global variables
        global _Config

        # Setting the 'displayingFile' to True so this function doesn't get called infinitely
        _Config["displayingFile"] = True

        # Clearing the screen of the ink that belongs to pen
        pen.clear()

        # Setting the display state
        _Config["displayingFileState"] = root.state()

        if root.state() != "zoomed":

            # Drawing the border
            pen.goto((-window.window_width() / 2) + (window.window_width() / 64),
                     (-window.window_height() / 2) + (window.window_height() / 32))
            pen.pd()
            pen.pensize(3)
            pen.color('#ba75eb')
            pen.fillcolor('#8b41bf')
            pen.begin_fill()
            for loop in range(2):
                pen.fd(window.window_width() - (window.window_width() / 16))
                pen.lt(90)
                pen.fd(window.window_height() - (window.window_height() / 4))
                pen.lt(90)
            pen.end_fill()
            pen.pu()
            pen.pensize(1)

            # drawing the file name
            pen.lt(90)
            pen.fd(window.window_height() - (window.window_height() / 4) - 25)
            pen.setx(pen.xcor() + 25)
            pen.color('black')
            pen.write(_FileConfig["basename"], font=("Courier", 17, "bold"))

            # Moving the closeBtn turtle next to the file name and showing the turtle
            closeFileBtn.goto(pen.xcor(), pen.ycor())
            closeFileBtn.st()

            # Moving the pen near the bottom-left of the border
            pen.goto((-window.window_width() / 2) + (window.window_width() / 64) + 15,
                     (-window.window_height() / 2) + (window.window_height() / 32) + 15)

            # Writing the file contents depending on the decompressed file format

            contentOutput = get_contents_to_draw()

            # TODO: Looking at each item in sarcKeys and determining the directories on the root

            # Writing the formatted list of files in the SArc
            pen.write(contentOutput, font=("Courier", 14, "bold"))

            # Resetting the pen heading
            pen.seth(0)

            # TODO: Finish drawing file while state is not "zoomed"

        else:

            # Drawing the border
            pen.goto((-window.window_width() / 2) + (window.window_width() / 64),
                     (-window.window_height() / 2) + (window.window_height() / 32))
            pen.pd()
            pen.pensize(3)
            pen.color('#ba75eb')
            pen.fillcolor('#8b41bf')
            pen.begin_fill()
            for loop in range(2):
                pen.fd(window.window_width() - (window.window_width() / 25))
                pen.lt(90)
                pen.fd(window.window_height() - (window.window_height() / 5))
                pen.lt(90)
            pen.end_fill()
            pen.pu()
            pen.pensize(1)

            # drawing the file name
            pen.lt(90)
            pen.fd(window.window_height() - (window.window_height() / 5) - 25)
            pen.setx(pen.xcor() + 25)
            pen.color('black')
            pen.write(_FileConfig["basename"], font=("Courier", 15, "bold"))

            # Resetting the pen heading
            pen.seth(0)

            # TODO: Finish drawing file while state is "zoomed"

    # Configuring update function
    def update():

        if root.state() == "zoomed":
            exitToMainBtn.goto(turtleCanvas.winfo_width()/2 - 120, turtleCanvas.winfo_height()/2 - 15)
            fileBtn.goto(-turtleCanvas.winfo_width()/2 + 43, turtleCanvas.winfo_height()/2 - 15)
        else:
            exitToMainBtn.goto(window.canvwidth - 179, window.canvheight - 27)
            fileBtn.goto(-window.canvwidth + 101, window.canvheight - 27)

        if _Config["fileDropdown"]:

            for btn in fileDropdownButtons:
                btn.ht()

        else:

            for btn in fileDropdownButtons:
                btn.st()

        # Updating turtle positions
        openBtn.goto(fileBtn.xcor() + 33, fileBtn.ycor() - 28)
        newBtn.goto(openBtn.xcor(), openBtn.ycor() - 27)

        # Detecting if the Screen pen drew the file (if a file is opened)
        if _Config["fileOpen"]:
            if not _Config["displayingFile"]:

                # Configure and draw file
                configure_file()
                draw_file()

            else:

                # Detecting if the file needs to be re-drawn
                if root.state() != _Config["displayingFileState"]:

                    # Draw file
                    draw_file()

        # Looping the update() function forever
        turtle.ontimer(update, 100)

    # Running the update() function
    update()

    # window mainloop
    window.mainloop()
