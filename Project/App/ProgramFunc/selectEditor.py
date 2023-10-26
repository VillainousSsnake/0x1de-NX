import turtle
import os


def select_editor(self):

    # Initializing
    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    # Configuring the window
    window = turtle.Screen()
    window.delay(0)
    window.title("0x1de NX - VERSION: 0.0.1 - Select Editor")
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

    pen = turtle.Turtle()
    pen.ht()
    pen.speed(0)
    pen.pu()

    logo = turtle.Turtle()
    logo.pu()
    logo.speed(0)
    logo.goto(-2.5, 175)

    # Configuring the buttons
    meshCodecEditorBtn = turtle.Turtle()
    meshCodecEditorBtn.pu()
    meshCodecEditorBtn.speed(0)
    meshCodecEditorBtn.goto(150, -100)

    fileEditorBtn = turtle.Turtle()
    fileEditorBtn.pu()
    fileEditorBtn.speed(0)
    fileEditorBtn.goto(-150, -100)

    previousBtn = turtle.Turtle()
    previousBtn.pu()
    previousBtn.speed(0)
    previousBtn.goto(-window.canvwidth + 100, window.canvheight - 50)

    # Configuring the textures
    meshCodecEditorBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "select_editor",
        "MeshCodecEditorButton.gif"
    )
    fileEditorBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "select_editor",
        "fileEditorButton.gif"
    )
    logoTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "select_editor",
        "logo.gif"
    )
    previousBtnTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "select_editor",
        "previousButton.gif"
    )

    # Registering the textures
    window.register_shape(meshCodecEditorBtnTex)
    window.register_shape(fileEditorBtnTex)
    window.register_shape(logoTex)
    window.register_shape(previousBtnTex)

    # Applying the textures
    logo.shape(logoTex)
    meshCodecEditorBtn.shape(meshCodecEditorBtnTex)
    fileEditorBtn.shape(fileEditorBtnTex)
    previousBtn.shape(previousBtnTex)

    # Configuring the button onclick methods
    def previous_button_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "MAIN_MENU"

    def mesh_codec_editor_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "MESH_CODEC_EDITOR"

    def file_editor_onclick(x, y):

        if x is None or y is None:
            on_close()
            raise TypeError("Onclick Coordinates cannot be NoneType")

        on_close()
        self.returnStatement = "FILE_EDITOR"

    # Applying the onclick methods
    previousBtn.onclick(previous_button_onclick, 1)
    meshCodecEditorBtn.onclick(mesh_codec_editor_onclick, 1)
    fileEditorBtn.onclick(file_editor_onclick, 1)

    # The window mainloop
    window.mainloop()
