import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


root = tk.Tk()
root.minsize(height=500, width = 400)
root.title("textedit")

font_intvar = tk.IntVar()
font_intvar.set(14)

# canvas = Canvas(root, width = 600, height = 600, background='lightblue')
# canvas.grid()
title = tk.Label(activebackground= "gray", height = 3, text= "Text Editor!!!", cursor = "pirate", font= ('Impact' , 30))
title.grid(row=0, column=0)


status = tk.Label(root, text='')
status.grid(row=3, column=0)

font_int = font_intvar.get()
edit = tk.Text(width=50, height=20, bg="lightblue", font=("Times New Roman", font_int))
edit.grid(row=1, column=0)


def save_func():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                text_content = edit.get("1.0", "end-1c")
                file.write(text_content)
            status.config(text=f"File Saved! Last Saved at " )
        except Exception as e:
            status.config(text=f"Error")
       
def font_size(amt):
    global font_int
    font_int = font_int + amt
    edit.config(font=('Times New Roman', font_int))

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

filemenu = tk.Menu(menu_bar, tearoff=0)
filemenu.add_command(label='Save', command= save_func)

textmenu = tk.Menu(menu_bar, tearoff=0)
textmenu.add_command(label='Text Size +', command= font_size(1))

menu_bar.add_cascade(label = 'File', menu= filemenu)
menu_bar.add_cascade(label = 'Text', menu= textmenu)


root.mainloop()

