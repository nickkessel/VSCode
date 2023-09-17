#-----------import libraries
import turtle as t
import time 
import random as r

#----------variables
font_setup = ["Impact", 35, "normal"]
screen_size = 350


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
    for i in range(200):
        clear.color("blue")
        if abs(ob.xcor()) > screen_size or abs(ob.ycor()) > screen_size:
            ob.pu()
            ob.goto(0,0)
            ob.pd()
        else:  
            ob.fd(r.randint(20,60))
            ob.right(r.randint(45,135))
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