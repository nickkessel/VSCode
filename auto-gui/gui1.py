import pyautogui as gui
import time

width, height = gui.size()
print("w: " + str(width), "h: " + str(height)) #print screen width and height

mouseX, mouseY = gui.position()
print(mouseX, mouseY)

for x in range(50): #for 12.5 seconds, print mouse x and y
    time.sleep(.25)
    mouseX, mouseY = gui.position()
    print(mouseX, mouseY)