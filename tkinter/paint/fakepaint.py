# Draws shapes by dragging on a canvas.
import tkinter
import pyautogui
import time
from PIL import Image

#TODO s without the highlight are COMPLETE
#TODO rebuild grid so that i can have 2 tool change buttons in the width of 1 other element like status text or clear/save buttons
#TODO make buttons for changing active tool
#TODO make icons for said new buttons !DONE
#FIXME: redo icon for pen tool
#TODO: change instuctions (maybe hover???)
#TODO delete the old keypress thing and update that in instructions
#TODO add frame system for tool change buttons
#TODO: rewrite save code so that the filename is the time of the save
#TODO: mMAYBE rewrite save code so you can choose filepath
#TODO: add pen tool for drawing (could be hard, but could then add width and all that kinda cool stuff (mouse scroll width???)) with cursor to reflect it (Change cursor size???)
#TODO: fix colors so there is more variety / usefullness
#TODO: mouse scroll wheel for color change?

root = tkinter.Tk()
root.wm_title('Color-Shape Art Creation')
root.configure(bg="lightgray")

# Create a canvas and place it
canvas = tkinter.Canvas(root, height=600, width=900, background='#FFFFFF')
canvas.grid(row=0, column=2, rowspan=3)

#create color frame
color_frame = tkinter.Canvas(root, background='#333333', width=500, height=60)
color_frame.grid(row=4, column=2, rowspan=2)

#frame for clear save and future menu type buttons
menu_button_frame = tkinter.Frame(root, background='lightgray')
menu_button_frame.grid(row = 1, column= 0, columnspan=2)

#frame for buttons that change the current tool
tool_button_frame = tkinter.Frame(root, background='#bbbbbb')
tool_button_frame.grid(row=0, column= 0, columnspan=2, padx= 5)

# Create a list of objects on the canvas
shapes = []

resized_img_button = (40,40) #resize icons

#list of colors
colorsList = ['red', 'yellow', 'blue', 'green', 'brown', 'cyan', 'violet', 'magenta', 
        'orange', 'darkgray']

#set default cursor to circle
canvas.config(cursor="circle")
#set default shape to oval
color_int = 0
shape_type = 0
border_width = 1
borderOn = True

#Instructions for the user
# message = tkinter.Label(root, text='Drag mouse to create \n shape!\n r = rectangle \n c = circle \n right-click = recolor \n b = border \n middle-click = cycle colors', padx=20)
# message.grid(column=0, row=0, columnspan=2)

#text with shape
current_shape = tkinter.Label(root, text='Oval ', font=('Impact', 20 ))
current_shape.grid(column=0, row=2, columnspan=2)

current_border = tkinter.Label(root, text= "Border On", font=('Impact', 20))
current_border.grid(column=0, row=2, sticky= tkinter.S, columnspan=2)

highlight_square = color_frame.create_rectangle(5 + (color_int*50) ,5,45 + (color_int * 50),55, fill= '#aaaaaa')

for x in range(10):
    color_square = color_frame.create_rectangle( 10+ (x * 50) ,10, 40 + (x*50),50, fill=colorsList[x])

#button functions
def clear():
    print("clear")
    shapes.clear()
    canvas.delete('all')


def save():
    print("\n start save")
    x, y = canvas.winfo_rootx(), canvas.winfo_rooty()
    w, h = canvas.winfo_width(), canvas.winfo_height()
    
    print(x , y, w, h)
    
    current_time = time.time()
    final_time = round(current_time)
    print(final_time)
    
    
    image = pyautogui.screenshot('canvas' + str(final_time) + '.png', region= (x,y,w,h)) 
    time.sleep(1)
    image.save("canvas.png")
    print("saved")

def shape(type): # add 'event' param if turning on keyboard shortcuts
    #print("hello")
    global shape_type 
    shape_type = type
    print(shape_type)
    
    if shape_type == 0:
        canvas.config(cursor="circle")
        current_shape.config(text="Oval")
    elif shape_type == 1:
        canvas.config(cursor="dotbox")
        current_shape.config(text="Rectangle")
    elif shape_type == 2:
        canvas.config(cursor= "pencil")
        current_shape.config(text= "Pen Tool")
    elif shape_type == 3:
        canvas.config(cursor="circle")
        current_shape.config(text="Circle")
        
clear_img = tkinter.PhotoImage(file='C:/Users/nickk/Documents/VSCode/tkinter/paint/clear.png')
clear_button = tkinter.Button(menu_button_frame, image= clear_img, command=clear, width=100,
                              fg= "red", background="white", activebackground= "red",
                              activeforeground="white")
clear_button.pack(pady = 10, padx =15)

save_img = tkinter.PhotoImage(file='C:/Users/nickk/Documents/VSCode/tkinter/paint/save.png')
save_button = tkinter.Button(menu_button_frame, image=save_img, command= save,
                             width = 100, activebackground= "cyan")
save_button.pack()

oval_img = tkinter.PhotoImage(file='C:/Users/nickk/Documents/VSCode/tkinter/paint/oval_icon.png')
oval_button = tkinter.Button(tool_button_frame, image = oval_img, text="oval", command= lambda: shape(0))
oval_button.grid(row = 0, column=0, padx = 5, pady= 5)

rect_img = tkinter.PhotoImage(file='C:/Users/nickk/Documents/VSCode/tkinter/paint/rect_icon2.png')
rect_button = tkinter.Button(tool_button_frame, image= rect_img,text="rect", command= lambda: shape(1))
rect_button.grid(row = 0, column = 1)

pen_img = tkinter.PhotoImage(file='C:/Users/nickk/Documents/VSCode/tkinter/paint/pen_icon2.png')
pen_button = tkinter.Button(tool_button_frame, image= pen_img, text="pen", command= lambda: shape(2))
pen_button.grid(row=1, column=0, padx= 5, pady=5)

circle_img = tkinter.PhotoImage(file='C:/Users/nickk/Documents/VSCode/tkinter/paint/circle_icon2.png')
circle_button = tkinter.Button(tool_button_frame, image= circle_img, text="Circle", command= lambda: shape(3))
circle_button.grid(row=1, column=1, padx = 5, pady = 5)

########## Event handler for mouse clicks and recolor

startx, starty = 300, 300 #initial values for mouse coordinates

def recolor(event):
    global mouse_x, mouse_y
    mouse_x = event.x
    mouse_y = event.y
    print("Mouse coords: " + str(mouse_x) + ", " + str(mouse_y))
    
    for x in shapes:
        print(str(x )+ ". " + str(canvas.coords(x)))
        if mouse_x > canvas.coords(x)[0] and mouse_y > canvas.coords(x)[1] and mouse_x < canvas.coords(x)[2] and mouse_y < canvas.coords(x)[3]:
            canvas.itemconfig(x, fill=colorsList[color_int])

def color_select(event):
    global color_int
    color_int = color_int + 1
    if color_int > 9:
        color_int = 0
    print("color: " + str(color_int))
    color_frame.coords(highlight_square, 5 + (color_int*50) ,5,45 + (color_int * 50),55 )

def border(event):
    global border_width, borderOn
    if borderOn == True:
        borderOn = False
    elif borderOn == False:
        borderOn = True
        
    if borderOn == True:
        border_width = 1
        current_border.config(text= "Border On")
    elif borderOn == False:
        border_width = 0
        current_border.config(text = "Border Off")
    

def down(event):
    global startx, starty # Use global variables for assignment
    startx = event.x # Store the mouse down coordinates in the global variables
    starty = event.y
    
def up(event): # thing that do the drawing
    global color_int
    global shape_type
    global border_width
    #tk_color_string = color(red_intvar, green_intvar, blue_intvar)
    r = (startx-event.x)**2 + (starty-event.y)**2 # Pythagorean theorem
    r = int(r**.5)  # square root to get distance
    
    endx = event.x
    endy = event.y
    
    if shape_type == 0:
        print("oval") 
        #new_shape = canvas.create_oval(startx-r, starty-r, startx+r, starty+r,
        #outline='#000000', fill=colorsList[color_int])
        shapes.append(canvas.create_oval(startx, starty, endx, endy,
        outline='#000000', fill=colorsList[color_int], width = border_width ))
    elif shape_type == 1:
        print("rect") 
        shapes.append(canvas.create_rectangle(startx, starty, endx, endy,
        outline='#000000', fill= colorsList[color_int], width= border_width))
    elif shape_type == 2:
        print("pen tool")
    elif shape_type == 3:
        print("circle")
        shapes.append(canvas.create_oval(startx, starty, startx + r, starty + r,
            outline='#000000', fill=colorsList[color_int], width= border_width))
 # aggregate the canvas' item
    #print(shapes)
    
# Button press and release event

canvas.bind('<Button-1>', down)
canvas.bind('<ButtonRelease-1>', up)
# canvas.bind('<c>', lambda event: shape(event, 0))
# canvas.bind('<r>', lambda event: shape(event, 1))
canvas.bind('<Button-2>', color_select)
canvas.bind('<Button-3>', recolor)
canvas.bind('<b>', border)

canvas.focus_set()

# Only the one widget with 'focus' gets keyboard events.

print (startx, starty)
root.mainloop()
