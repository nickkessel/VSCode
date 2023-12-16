import pyautogui as gui

logo = 'C:/Users/nickk/Documents/VSCode/auto-gui/spotify.png'
gui.alert("Start Program")

spotify_location = gui.locateOnScreen(logo)
print(spotify_location)