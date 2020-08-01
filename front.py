from tkinter import *
import back as B

def enable_scene_1(a):
    set_photo_mangapanda_label()
    set_input_url()
    set_button_find()
    error.place_forget()
    manga_name.place_forget()

def disable_scene_1():
    photo_mangapanda_label.place_forget()
    input_url.place_forget()
    button_find.place_forget()

def set_photo_mangapanda_label():
    photo_mangapanda_label.config(bg='#1BF186')
    x = WIDTH/2 - photo_mangapanda.width()/2
    y = HEIGHT/2 - photo_mangapanda.height()
    photo_mangapanda_label.place(x=x, y=y)

def set_input_url():
    x = WIDTH/2 - 140
    y = HEIGHT/2
    input_url.place(x=x, y=y)

def set_error_message():
    x = WIDTH/2 - 65
    y = HEIGHT/2 + 60
    error.place(x=x, y=y)

def set_button_find():
    x = WIDTH/2 - 10
    y = HEIGHT/2 + 30
    button_find.place(x=x, y=y)

def set_manga_name(name):
    x = WIDTH/2
    y = HEIGHT/2
    manga_name.config(text=name)
    manga_name.place(x=x, y=y)

def main():
    enable_scene_1(None)
    window.mainloop()

def find_manga():
    source = B.request_manga(input_url.get())
    if source == None:
        set_error_message()
    else:
        disable_scene_1()
        set_manga_name(B.get_manga_name(source))

WIDTH = 540
HEIGHT = 360

# creating window
window = Tk()
window.title("Mangapanda Scraper")
window.geometry(str(WIDTH) + 'x' + str(HEIGHT))
window.minsize(WIDTH, HEIGHT)
window.maxsize(WIDTH, HEIGHT)
window.config(background='#1BF186')

# creating photos
photo_mangapanda = PhotoImage(file='mangapanda.png')

# creating labels
photo_mangapanda_label = Label(window, image=photo_mangapanda)
error = Label(window, text='NOT FOUND', bg='#1BF186', fg='red', font='Arial 18 bold')
manga_name = Label(window, text='')

# creating inputs
input_url = Entry(window, width=50)

# creating buttons
button_find = Button(window, text="Find", command=find_manga)

window.bind('<KeyPress>', enable_scene_1)

main()