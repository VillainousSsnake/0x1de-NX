import turtle


def zstandard_editor(self):

    # Initializing
    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    # Configuring the window
    window = turtle.Screen()
    window.title("0x1de NX - VERSION: 0.0.1 - ZStandard Editor")
    turtleCanvas = window.getcanvas()
    root = turtleCanvas.winfo_toplevel()

    def on_close():
        turtle.bye()
        self.returnStatement = "Closed"

    root.protocol("WM_DELETE_WINDOW", on_close)

    # Window mainloop
    window.mainloop()
