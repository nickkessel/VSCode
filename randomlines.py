#-----------import libraries
import turtle as t
import time 
import random as r

#----------variables
font_setup = ["Impact", 35, "normal"]
screen_size = 350
colors = ['white',
    'black',
    'red',
    'green',
    'blue',
    'cyan',
    'magenta',  # You can also use 'purple'
    'yellow',
    'orange',
    'brown']
values = [20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160]

#---------turtle setup

#main drawing turtle
ob = t.Turtle()
ob.ht()
ob.speed(0)
ob.color("white")

#start button
start = t.Turtle()
start.shape("square")
start.pu()
start.speed(0)
start.goto(0,-300)
start.shapesize(4,12,1)
start.color("green")

#clear button
clear = t.Turtle()
clear.shape("triangle")
clear.pu()
clear.speed(0)
clear.seth(-90)
clear.goto(-250,-287)
clear.shapesize(4,4,1)
clear.color("grey")

#label buttons
label = t.Turtle()
label.ht()
label.pu()
label.color("salmon")
label.speed(0)
label.goto(-295,-250)
label.write("clear", font = font_setup)
label.goto(-85,-260)
label.write("generate", font = font_setup)

#screen border
border = t.Turtle()
border.ht()
border.speed(0)
border.pu()
border.color("yellow")
border.pensize(2)
border.goto(-screen_size,screen_size + 20)
border.pd()
border.goto(-screen_size,-screen_size + 20)
border.goto(screen_size,-screen_size + 20)
border.goto(screen_size,screen_size + 20)
border.goto(-screen_size,screen_size + 20)

#------------ functions

#main generate function
def design(x,y):
    start.color("red")
    ob.color(r.choice(colors))
    for i in range(200):
        clear.color("blue")
        if abs(ob.xcor()) > screen_size or abs(ob.ycor()) > screen_size:
            ob.pu()
            ob.goto(0,0)
            ob.pd()
        else:  
            ob.fd(r.randint(25,55))
            #ob.right(r.randint(40,140))
            ob.right(r.choice(values))
    start.color("green")
        
#clears screen       
def clear_screen(x,y):
    ob.clear()
    clear.color("grey")    
    
#------------events
   
start.onclick(design)
clear.onclick(clear_screen)

wn = t.Screen()
wn.bgcolor("black")
wn.mainloop()