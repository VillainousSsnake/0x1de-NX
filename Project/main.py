"""
0x1de NX is a tool for modding file formats from The Legend of Zelda: Tears of the Kingdom

"""

from tkinter import filedialog
from tkinter import *
import turtle
import os
from __Cache__.data import *
from FileFormatLibrary.ZStd.zstd import ZSTD


# Program
class Program:
    def main(self):
        # Configuring the app variables
        self._Config = {
            "isFileOpen": False,
            "isFolderOpen": False,
            "isFileBtnDropdownShowing": False,
            "CurrentFilepath": None,
            "displayingObject": False,
        }

        # Configuring the window
        window = turtle.Screen()
        window.title("0x1de NX - VERSION: Dev1.0.0")
        turtleCanvas = window.getcanvas()
        root = turtleCanvas.winfo_toplevel()
        root.resizable(False, False)
        def on_close():
            turtle.bye()
        root.protocol("WM_DELETE_WINDOW", on_close)

        # Configuring the App Pen
        pen = turtle.Turtle()
        pen.pu()
        pen.ht()
        pen.speed(0)

        # Configure buttons
        fileBtn = turtle.Turtle()
        fileBtn.pu()
        fileBtn.speed(0)
        fileBtn.goto(-window.canvwidth + 91, window.canvheight - 25)

        openBtn = turtle.Turtle()
        openBtn.pu()
        openBtn.speed(0)
        openBtn.goto(fileBtn.xcor() + 40, fileBtn.ycor() - 21)

        openFolderBtn = turtle.Turtle()
        openFolderBtn.pu()
        openFolderBtn.speed(0)
        openFolderBtn.goto(openBtn.xcor(), openBtn.ycor() - 21)

        # Creating a list of mutable buttons
        self.mutableButtonsList = [openBtn, openFolderBtn]
        self.fileDropdownButtons = [openBtn, openFolderBtn]

        # Configure button texture
        fileBtnTex = os.path.join(
            os.getcwd(),
            "Project",
            "Screen",
            "Texture",
            "filebtn.gif"
        )
        openBtnTex = os.path.join(
            os.getcwd(),
            "Project",
            "Screen",
            "Texture",
            "openbtn.gif"
        )
        openFolderBtnTex = os.path.join(
            os.getcwd(),
            "Project",
            "Screen",
            "Texture",
            "openfolderbtn.gif"
        )

        # Adding the shape to the turtle canvas
        window.register_shape(fileBtnTex)
        window.register_shape(openBtnTex)
        window.register_shape(openFolderBtnTex)

        # Setting the button's textures
        fileBtn.shape(fileBtnTex)
        openBtn.shape(openBtnTex)
        openFolderBtn.shape(openFolderBtnTex)

        # Configuring the button's onclick functions
        def file_btn_func(x, y):
            if self._Config["isFileBtnDropdownShowing"]:
                # Hiding the dropdown
                self._Config["isFileBtnDropdownShowing"] = False
                for button in self.mutableButtonsList:
                    button.ht()
            else:
                self._Config["isFileBtnDropdownShowing"] = True
                for button in self.fileDropdownButtons:
                    button.st()

        def open_btn_func(x, y):
            filetypes = (
                ('ZStandard', '*.zs'),
            )
            filepath = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                  title="Select a File",
                                                  filetypes=filetypes)
            if filepath == "":
                return -1

            self._Config["isFileOpen"] = True
            self._Config["currentFilepath"] = filepath

            update()

        def open_folder_func(x, y):
            filepath = filedialog.askdirectory(initialdir=os.getcwd(), title="Select a Folder")

            if filepath == "":
                return -1

            self._Config["isFolderOpen"] = True
            self._Config["currentFilepath"] = filepath

            update()

        # Setting the button's onclick functions
        fileBtn.onclick(file_btn_func, 1)
        openBtn.onclick(open_btn_func, 1)
        openFolderBtn.onclick(open_folder_func, 1)

        # Program Functions
        def update():

            if not self._Config["displayingObject"]:
                if self._Config["isFileOpen"]:
                    configure_current_file()

                if self._Config["isFolderOpen"]:
                    configure_current_folder()

        def configure_current_file():

            currentFile = str(self._Config["currentFilepath"])
            tempDir = os.path.join(
                os.getcwd(),
                "Project",
                "__Cache__",
                "_temp_"
            )
            dictDir = os.path.join(
                os.getcwd(),
                "Project",
                "__Cache__",
                "_dict_"
            )

            if currentFile.endswith("pack.zs"):
                pass

            # TODO: Stub

        def configure_current_folder():
            # TODO: Stub
            pass


        # Turtle mainloop
        window.mainloop()


    @staticmethod
    def createButton(
            shapesize: list = ...,
            shape: str = ...,
            fillcolor="grey",
            text: str = ...,
            text_pos=[0,0],
            text_size=15,
            text_font="Courier",
            text_format="bold"
    ):
        btn = turtle.Turtle()
        btn.shape(shape)
        btn.fillcolor(fillcolor)
        btn.shapesize(shapesize[0], shapesize[1])

        pen = turtle.Turtle()
        pen.pu()
        pen.ht()
        pen.speed(0)
        pen.goto(text_pos[0], text_pos[1])
        pen.write(text, font=(text_font, text_size, text_format))

        turtle.mainloop()


# running the program
app = Program()
app.main()
