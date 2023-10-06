"""
0x1de NX is a tool for modding file formats from The Legend of Zelda: Tears of the Kingdom

"""

from tkinter import filedialog
from tkinter import *
import turtle
import os
from __Cache__.data import *
from FileFormatLibrary.ZStd.zstd import ZSTD


# program
class Program:
    @staticmethod
    def main():

        # Configuring the window
        window = turtle.Screen()
        window.title("0x1de NX - VERSION: Dev1.0.0")
        turtleCanvas = window.getcanvas()
        root = turtleCanvas.winfo_toplevel()
        root.resizable(False, False)
        def on_close():
            turtle.bye()
        root.protocol("WM_DELETE_WINDOW", on_close)

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
        def file_btn_func():
            pass
        def open_btn_func():
            pass
        def open_folder_func():
            pass

        # Setting the button's onclick functions
        fileBtn.onclick(file_btn_func, 1)
        openBtn.onclick(open_btn_func, 1)
        openFolderBtn.onclick(open_folder_func, 1)



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
Program.main()
