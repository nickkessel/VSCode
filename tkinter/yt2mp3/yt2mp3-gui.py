from pytube import YouTube
from pytube import Playlist

import os
import moviepy.editor as mp
import re
import tkinter
from tkinter import font
import threading
import time
import music_tag

counter = 0
root = tkinter.Tk()
root.wm_title('yt2mp3')
root.configure(bg="lightpink", height= 150, width= 300)
root.resizable(width= False, height = False)
text_font = font.Font(family = 'OCR-A BT', size = 15)

title = tkinter.Label(root, text= "youtube playlist downloader", font= text_font, bg= 'lightpink')
title.grid(row=0, column=0, pady= 10)

input_frame = tkinter.LabelFrame(root, labelanchor= 'nw', text= 'Paste playlist link', font= ('Roboto', 12), bg= 'lightpink')
input_frame.grid(row=1, column=0, pady= 10, padx= 5)

text_input = tkinter.Text(input_frame, height= 1.5, width = 50, insertofftime= 200, insertontime= 200)
text_input.grid(row= 0, column= 0)

info_box = tkinter.LabelFrame(root, labelanchor= 'nw', text= 'Download Info', font= ('Roboto', 12), bg= 'lightpink')
info_box.grid(row=2, column=0, pady= 10, padx= 5)

playlist_title_text = tkinter.Label(info_box,font= ('Courier New', 12), text= 'playlist-name' , bg= 'lightpink')
playlist_title_text.grid(row=0, column= 0)

amount_text = tkinter.Label(info_box,font= ('Courier New', 12), text= 'dl info', bg= 'lightpink' )
amount_text.grid(row=1, column= 0)


def dl_playlist():
    ytlink = text_input.get("1.0",'end-1c')
    playlist = Playlist(ytlink)
    # #print vid url
    # for url in playlist:
    #     print(url)
    # #print address of yt object in playlist
    # for vid in playlist.videos:
    #     print(vid)
    global counter

    folder = "/Users/nickk/Desktop/music"
    
    for url in playlist:
        #amount_text.config(text= 'downloading ' + str(counter) + ' of ' + str(playlist.length))
        YouTube(url).streams.filter(only_audio=True).first().download('/Users/nickk/Desktop/music')
        counter = counter + 1

    counter2 = 1
    for file in os.listdir(folder):
        if re.search('mp4', file):
            #amount_text.config(text= 'converting ' + str(counter2) + ' of ' + str(playlist.length))
            mp4_path = os.path.join(folder,file)
            mp3_path = os.path.join(folder,os.path.splitext(file)[0]+'.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)
            file_to_edit = music_tag.load_file(mp3_path)
            file_to_edit['artist'] = 'test'
            

def get_playlist_data():
    ytlink = text_input.get("1.0",'end-1c')
    playlist = Playlist(ytlink)
    playlist_title_text.config(text= "Downloading: " + playlist.title + " by " + playlist.owner + ' [' + str(playlist.length) + ' songs]')
    amount_text.config(text= 'downloading ' + str(playlist.length) + ' songs')
    global counter
    while True:
        time.sleep(1)
        global counter
        amount_text.config(text= 'processing ' + str(counter) + ' of ' + str(playlist.length))
        
        if counter == playlist.length:
            amount_text.config(text= 'processing complete, please see console')

    
    
def thread_starter():
    ui_thread = threading.Thread(target=get_playlist_data).start()
    dl_thread = threading.Thread(target= dl_playlist).start()


submit_button = tkinter.Button(input_frame, text= 'Go', command= thread_starter, font= ('Roboto', 12), bg= 'lightblue')
submit_button.grid(row= 0, column= 1, padx= 5)


root.mainloop()