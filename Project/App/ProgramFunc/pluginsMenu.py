import turtle
import os


def plugins_menu(self):

    # Initializing
    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    # Configuring the window
    window = turtle.Screen()
    window.delay(0)
    window.title("0x1de NX - VERSION: 0.0.1 - Plugins Menu")
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

    # Configuring the Turtles
    logo = turtle.Turtle()
    logo.pu()
    logo.speed(0)
    logo.goto(-2.5, 175)

    previousBtn = turtle.Turtle()
    previousBtn.pu()
    previousBtn.speed(0)
    previousBtn.goto(-window.canvwidth + 100, window.canvheight - 50)

    # Configuring the textures
    logoTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "plugins_menu",
        "logo.gif"
    )
    previousBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "plugins_menu",
        "previousButton.gif"
    )

    # Registering the textures
    window.register_shape(logoTex)
    window.register_shape(previousBtnTex)

    # Applying the textures
    logo.shape(logoTex)
    previousBtn.shape(previousBtnTex)

    # Configuring button onclick method's
    def previous_button_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "MAIN_MENU"

    # Applying the button onclick method's
    previousBtn.onclick(previous_button_onclick, 1)

    # Turtle mainloop
    window.mainloop()
