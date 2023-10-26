import turtle
import os


def mesh_codec_editor(self):

    # Initializing
    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    # Configuring the window
    window = turtle.Screen()
    window.delay(0)
    window.title("0x1de NX - VERSION: 0.0.1 - MeshCodec Editor")
    turtleCanvas = window.getcanvas()
    root = turtleCanvas.winfo_toplevel()
    root.iconbitmap(os.path.join(os.getcwd(), "Project", "Screen", "Texture", "main", "0x1de.ico"))

    def on_close():
        turtle.bye()
        self.returnStatement = "Closed"

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Window mainloop
    window.mainloop()
