import turtle


def display_error_code(self, error_code, error_details): 

    turtle.TurtleScreen._RUNNING = True
    self.returnStatement = None

    error_code = str(error_code)
    error_details = str(error_details)

    output_error = 'ERROR_CODE: ' + error_code + "\nERROR_DETAILS: " + error_details

    window = turtle.Screen()
    window.setup(1000, 200)

    window.title("0x1de NX - ERROR CODE: ".join(error_code))
    turtleCanvas = window.getcanvas()
    root = turtleCanvas.winfo_toplevel()
    root.resizable(False, False)

    def on_close():
        turtle.bye()
        self.returnStatement = "Closed"

    root.protocol("WM_DELETE_WINDOW", on_close)

    pen = turtle.Turtle()
    pen.ht()
    pen.pu()
    pen.goto(-450,0)
    pen.write(output_error, font=("Courier", 25, "bold"))

    window.mainloop()
