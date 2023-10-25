import turtle

def create_button(text="", size=[1,1], color="grey", shape="square", textPos=[0,0], textSize=15, textFont="Courier", textType="bold"):

    btn = turtle.Turtle()
    btn.pu()
    btn.shape(shape)
    btn.shapesize(size[0], size[1])
    btn.fillcolor(color)

    pen = turtle.Turtle()
    pen.ht()
    pen.pu()
    pen.speed(0)
    pen.goto(textPos[0], textPos[1])
    pen.write(text, font=(textFont, textSize, textType))

    turtle.mainloop()

create_button(
    "File Editor",
    [1,11],
    "grey",
    "square",
    [-107.5,-12.5],
    15,
    "Courier"
)