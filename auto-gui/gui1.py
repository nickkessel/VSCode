import pyautogui as gui
import time

width, height = gui.size()
print("w: " + str(width), "h: " + str(height))

mouseX, mouseY = gui.position()
print(mouseX, mouseY)

for x in range(50):
    time.sleep(.25)
    mouseX, mouseY = gui.position()
    print(mouseX, mouseY)