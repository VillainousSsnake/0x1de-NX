import turtle
import os


def settings(self):

    # Initializing
    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    # Configuring the window
    window = turtle.Screen()
    window.title("0x1de NX - VERSION: 0.0.1 - Settings")
    turtleCanvas = window.getcanvas()
    root = turtleCanvas.winfo_toplevel()
    root.resizable(False, False)
    turtleCanvas.update()

    def on_close():
        turtle.bye()
        self.returnStatement = "Closed"

    root.protocol("WM_DELETE_WINDOW", on_close)
    window.bgcolor("#131642")

    # Configuring Buttons
    previousBtn = turtle.Turtle()
    previousBtn.pu()
    previousBtn.speed(0)
    previousBtn.goto(-window.canvwidth + 100, window.canvheight - 50)

    # Configuring textures
    previousBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "settings",
        "previousButton.gif"
    )

    # Registering the textures
    window.register_shape(previousBtnTex)

    # Applying the textures
    previousBtn.shape(previousBtnTex)

    # Configuring the button onclick methods
    def previous_button_conclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "MAIN_MENU"

    # Applying the onclick methods
    previousBtn.onclick(previous_button_conclick, 1)

    window.mainloop()
