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

    setGamePathBtn = turtle.Turtle()
    setGamePathBtn.pu()
    setGamePathBtn.speed(0)
    setGamePathBtn.goto(-175, 50)

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
    setGamePathBtnTex = os.path.join(
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
    window.register_shape(setGamePathBtnTex)

    # Applying the textures
    logo.shape(logoTex)
    previousBtn.shape(previousBtnTex)
    setGamePathBtn.shape(setGamePathBtnTex)

    # Configuring the button onclick methods
    def previous_button_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "MAIN_MENU"

    def game_paths_button_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "GAME_PATH_SELECT"

    # Applying the onclick methods
    previousBtn.onclick(previous_button_onclick, 1)
    setGamePathBtn.onclick(game_paths_button_onclick, 1)

    window.mainloop()
