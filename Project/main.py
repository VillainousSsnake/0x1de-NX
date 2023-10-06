"""
0x1de NX is a tool for modding file formats from The Legend of Zelda: Tears of the Kingdom

"""

from tkinter import filedialog
from tkinter import *
import turtle
from __Cache__.data import *
from FileFormatLibrary.ZStd.zstd import ZSTD


# program
class Program:
    @staticmethod
    def main():

        window = turtle.Screen()
        window.title("0x1de NX - VERSION: Dev1.0.0")
        turtleCanvas = window.getcanvas()
        root = turtleCanvas._rootwindow
        root.resizable(False, False)
        def on_close():
            turtle.bye()
        root.protocol("WM_DELETE_WINDOW", on_close)

        # the window mainloop
        window.mainloop()


# running the program
Program.main()
