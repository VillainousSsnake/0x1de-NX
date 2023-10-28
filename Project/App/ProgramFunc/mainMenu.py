import turtle
import os


def main_menu(self):

    # Initializing
    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    # Configuring the window
    window = turtle.Screen()
    window.delay(0)
    window.title("0x1de NX - VERSION: 0.0.1")
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

    # Configuring the turtles

    settingsBtn = turtle.Turtle()
    settingsBtn.pu()
    settingsBtn.speed(0)
    settingsBtn.goto(-100, -125)

    editorBtn = turtle.Turtle()
    editorBtn.pu()
    editorBtn.speed(0)
    editorBtn.goto(-200, -50)

    mergeBtn = turtle.Turtle()
    mergeBtn.pu()
    mergeBtn.speed(0)
    mergeBtn.goto(200, -50)

    pluginsBtn = turtle.Turtle()
    pluginsBtn.pu()
    pluginsBtn.speed(0)
    pluginsBtn.goto(100, -125)

    playBtn = turtle.Turtle()
    playBtn.pu()
    playBtn.speed(0)
    playBtn.goto(0,-50)

    creditsBtn = turtle.Turtle()
    creditsBtn.pu()
    creditsBtn.speed(0)
    creditsBtn.goto(0,-200)

    logo = turtle.Turtle()
    logo.pu()
    logo.speed(0)
    logo.goto(-2.5, 175)

    # Configuring the textures
    settingsBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "main",
        "settingsBtn.gif"
    )
    editorBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "main",
        "editorBtn.gif"
    )
    mergeBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "main",
        "mergeBtn.gif"
    )
    pluginsBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "main",
        "pluginsBtn.gif"
    )
    playBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "main",
        "playBtn.gif"
    )
    creditsBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "main",
        "creditsBtn.gif"
    )
    logoTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "main",
        "logo.gif"
    )

    # Registering the textures
    window.register_shape(settingsBtnTex)
    window.register_shape(editorBtnTex)
    window.register_shape(mergeBtnTex)
    window.register_shape(pluginsBtnTex)
    window.register_shape(playBtnTex)
    window.register_shape(creditsBtnTex)
    window.register_shape(logoTex)

    # Applying the textures
    settingsBtn.shape(settingsBtnTex)
    editorBtn.shape(editorBtnTex)
    mergeBtn.shape(mergeBtnTex)
    pluginsBtn.shape(pluginsBtnTex)
    playBtn.shape(playBtnTex)
    creditsBtn.shape(creditsBtnTex)
    logo.shape(logoTex)

    # Configuring the button turtle's onclick method
    def settings_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "SETTINGS"

    def editor_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "SELECT_EDITOR"

    def merge_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "MERGE_MODS"

    def plugins_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "PLUGINS_MENU"

    def play_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "PLAY_MENU"

    def credits_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "CREDITS_MENU"

    # Applying the onclick methods
    settingsBtn.onclick(settings_onclick, 1)
    editorBtn.onclick(editor_onclick, 1)
    mergeBtn.onclick(merge_onclick, 1)
    pluginsBtn.onclick(plugins_onclick, 1)
    playBtn.onclick(play_onclick, 1)
    creditsBtn.onclick(credits_onclick, 1)

    # Turtle mainloop
    window.mainloop()

    while self.returnStatement is None:
        pass

    return self.returnStatement
