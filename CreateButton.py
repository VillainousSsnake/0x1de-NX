import turtle

window = turtle.Screen()
window.bgcolor("#131642")

def create_button(text="", size=[1,1], color="grey", outline_color="black", shape="square", textPos=[0,0], textSize=15, textFont="Courier", textType="bold"):

    btn = turtle.Turtle()
    btn.pu()
    btn.shape(shape)
    btn.shapesize(size[0], size[1], 1.5)
    btn.color(outline_color)
    btn.fillcolor(color)

    pen = turtle.Turtle()
    pen.ht()
    pen.pu()
    pen.speed(0)
    pen.goto(textPos[0], textPos[1])
    pen.write(text, font=(textFont, textSize, textType))

    turtle.mainloop()

create_button(
    "New",
    [1.25,7],
    "#8b41bf",
    "#ba75eb",
    "square",
    [-60,-12.5],
    15,
    "Courier"
)