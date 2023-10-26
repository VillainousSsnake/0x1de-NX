import turtle
import os


def settings(self):

    # Initializing
    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    # Configuring the window
    window = turtle.Screen()
    window.delay(0)
    window.title("0x1de NX - VERSION: 0.0.1 - Settings")
    turtleCanvas = window.getcanvas()
    root = turtleCanvas.winfo_toplevel()
    root.resizable(False, False)
    root.iconbitmap(os.path.join(os.getcwd(), "Project", "Screen", "Texture", "main", "0x1de.ico"))
    turtleCanvas.update()

    def on_close():
        turtle.bye()
        self.returnStatement = "Closed"

    root.protocol("WM_DELETE_WINDOW", on_close)
    window.bgcolor("#131642")

    # Configuring Logo
    logo = turtle.Turtle()
    logo.pu()
    logo.speed(0)
    logo.goto(-2.5, 175)

    # Configuring Buttons
    previousBtn = turtle.Turtle()
    previousBtn.pu()
    previousBtn.speed(0)
    previousBtn.goto(-window.canvwidth + 100, window.canvheight - 50)

    setTotKPathBtn = turtle.Turtle()
    setTotKPathBtn.pu()
    setTotKPathBtn.speed(0)
    setTotKPathBtn.goto(-175, 50)

    # Configuring textures
    logoTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "settings",
        "logo.gif"
    )
    previousBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "settings",
        "previousButton.gif"
    )
    setTotKPathBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "settings",
        "setTotKDump.gif"
    )

    # Registering the textures
    window.register_shape(logoTex)
    window.register_shape(previousBtnTex)
    window.register_shape(setTotKPathBtnTex)

    # Applying the textures
    logo.shape(logoTex)
    previousBtn.shape(previousBtnTex)
    setTotKPathBtn.shape(setTotKPathBtnTex)

    # Configuring the button onclick methods
    def previous_button_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "MAIN_MENU"

    def set_totk_path_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "GAME_PATH_SELECT"

    # Applying the onclick methods
    previousBtn.onclick(previous_button_onclick, 1)
    setTotKPathBtn.onclick(set_totk_path_onclick, 1)

    window.mainloop()
