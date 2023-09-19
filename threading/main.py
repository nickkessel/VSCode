import threading
import turtle as t
import time

def count(countTo):
    for x in range(countTo):
        print(x)
        time.sleep(.1)
        
ob = t.Turtle()
ob.pu()
ob.goto(-100,100)
ob.speed(0)

def drawShape(sides):
    for x in range(sides):
        ob.pd()
        ob.fd(50)
        ob.right(360/sides)
        ob.fd(50)

t1 = threading.Thread(target=count, args=(20,))
t2 = threading.Thread(target=drawShape, args=(40,))
t1.start()
t2.start()

#t1.join()

wn = t.Screen()
wn.mainloop()