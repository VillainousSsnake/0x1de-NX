# Importing custom libraries
from Project.FileFormatLibrary.ZStd.zstd import *

# Importing external libraries
import turtle
from tkinter import filedialog
import os

_Config = {
    "tempDir": os.path.join(os.getcwd(), "Project", "__Cache__", "_temp_"),
    "fileDropdown": False,
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
    window.title("0x1de NX - VERSION: 0.0.1 - File Editor")
    turtleCanvas = window.getcanvas()
    root = turtleCanvas.winfo_toplevel()
    root.iconbitmap(os.path.join(os.getcwd(), "Project", "Screen", "Texture", "main", "0x1de.ico"))

    def on_close():
        turtle.bye()
        self.returnStatement = "Closed"

    root.protocol("WM_DELETE_WINDOW", on_close)

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

    compressBtn = turtle.Turtle()
    compressBtn.pu()
    compressBtn.speed(0)

    decompressBtn = turtle.Turtle()
    decompressBtn.pu()
    decompressBtn.speed(0)

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
    compressBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "file_editor",
        "compressBtn.gif"
    )
    decompressBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "file_editor",
        "decompressBtn.gif"
    )

    # Registering the textures
    window.register_shape(fileBtnTex)
    window.register_shape(openBtnTex)
    window.register_shape(newBtnTex)
    window.register_shape(compressBtnTex)
    window.register_shape(decompressBtnTex)

    # Applying the texture
    fileBtn.shape(fileBtnTex)
    openBtn.shape(openBtnTex)
    newBtn.shape(newBtnTex)
    compressBtn.shape(compressBtnTex)
    decompressBtn.shape(decompressBtnTex)

    # Creating lists for the buttons
    fileDropdownButtons = (openBtn,
                           newBtn,
                           compressBtn,
                           decompressBtn)

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

    def compress_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        # TODO: write compress_onclick function

    def decompress_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        # TODO: write decompress_onclick function

    # Applying the button onclick methods
    fileBtn.onclick(file_onclick, 1)
    openBtn.onclick(open_onclick, 1)
    newBtn.onclick(new_onclick, 1)
    compressBtn.onclick(compress_onclick, 1)
    decompressBtn.onclick(decompress_onclick, 1)

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
        dictionary = ""

        if _FileConfig["decompressedFiletype"] == "pack":
            dictionary = os.path.join(os.getcwd(), "Project", "__Cache__", "_dict_", "pack.zsdic")

        elif _FileConfig["decompressedFiletype"] == "byml":
            dictionary = os.path.join(os.getcwd(), "Project", "__Cache__", "_dict_", "bcett.byml.zsdic")

        elif _FileConfig["decompressedFiletype"] == "bcett":
            dictionary = os.path.join(os.getcwd(), "Project", "__Cache__", "_dict_", "bcett.byml.zsdic")

        # If the file is a ZStandard file
        if 'zs' in _FileConfig["basename"]:

            fileContents = ZSTD.decompress(_Config["currentFilepath"], _Config["tempDir"], dictionary)
            _FileConfig["decompressedFileContents"] = fileContents

    def draw_file():

        # Importing global variables
        global _Config

        # Setting the 'displayingFile' to True so this function doesn't get called infinitely
        _Config["displayingFile"] = True

        # Drawing the file
        pen.clear()

        # Setting the display state
        _Config["displayingFileState"] = root.state()

        if root.state() != "zoomed":

            # Drawing the border
            pen.goto((-window.window_width() / 2) + (window.window_width() / 64),
                     (-window.window_height() / 2) + (window.window_height() / 32))
            pen.pd()
            pen.pensize(3)
            pen.color('black')
            pen.fillcolor('grey')
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
            pen.write(_FileConfig["basename"], font=("Courier", 15, "bold"))

            # Resetting the pen heading
            pen.seth(0)

            # TODO: Finish drawing file while state is not "zoomed"

        else:

            # Drawing the border
            pen.goto((-window.window_width() / 2) + (window.window_width() / 64),
                     (-window.window_height() / 2) + (window.window_height() / 32))
            pen.pd()
            pen.pensize(3)
            pen.color('black')
            pen.fillcolor('grey')
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
            pen.write(_FileConfig["basename"], font=("Courier", 15, "bold"))

            # Resetting the pen heading
            pen.seth(0)

            # TODO: Finish drawing file while state is "zoomed"

    # Configuring update function
    def update():

        if root.state() == "zoomed":
            fileBtn.goto(-turtleCanvas.winfo_width()/2 + 32, turtleCanvas.winfo_height()/2 - 12)
        else:
            fileBtn.goto(-window.canvwidth + 90, window.canvheight - 24)

        if _Config["fileDropdown"]:

            for btn in fileDropdownButtons:
                btn.ht()

        else:

            for btn in fileDropdownButtons:
                btn.st()

        # Updating turtle positions
        openBtn.goto(fileBtn.xcor() + 40, fileBtn.ycor() - 21)
        newBtn.goto(openBtn.xcor(), openBtn.ycor() - 21)
        compressBtn.goto(newBtn.xcor(), newBtn.ycor() - 21)
        decompressBtn.goto(newBtn.xcor(), newBtn.ycor() - 42)

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
