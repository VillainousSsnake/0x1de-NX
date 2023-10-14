import turtle
import os


def game_path_select(self):

    # Initializing
    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    # Configuring the window
    window = turtle.Screen()
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

    # Configuring the buttons
    setTearsOfTheKingdomDump = turtle.Turtle()
    setTearsOfTheKingdomDump.pu()
    setTearsOfTheKingdomDump.speed(0)
    setTearsOfTheKingdomDump.goto(0, 0)

    # Configuring the textures
    setTearsOfTheKingdomDumpTex = os.path.join(
        os.getcwd(),
        "Project",
        "Screen",
        "Texture",
        "game_path_select",
        "setTotKDump.gif"
    )

    # Registering the textures
    window.register_shape(setTearsOfTheKingdomDumpTex)

    # Applying the textures
    setTearsOfTheKingdomDump.shape(setTearsOfTheKingdomDumpTex)

    window.mainloop()
