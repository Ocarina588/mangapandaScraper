from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import tempfile
import requests
import sys
import back as B
import os

def start_dowload():
    B.PATH_DIR = filedialog.askdirectory()
    button_download.place_forget()
    set_progress_bar()
    thread.start()

def enable_scene_1():
    disable_scene_2()
    set_photo_mangapanda_label()
    set_input_url()
    set_button_find()
    error.place_forget()
    manga_name.pack_forget()
    button_download.pack_forget()

def disable_scene_1():
    photo_mangapanda_label.place_forget()
    input_url.place_forget()
    button_find.place_forget()

def disable_scene_2():
    button_download.pack_forget()
    manga_name.pack_forget()
    photo_manga_label.pack_forget()

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

def set_button_download():
    x = WIDTH/2 - 30
    y = 325
    button_download.place(x=x, y=y)

def set_manga_name(name):
    manga_name.config(text=name)
    manga_name.pack()

def set_photo_manga(source):
    temp.seek(0)
    temp.truncate()
    img_url = source.find('div', id='mangaimg').find('img')['src']
    img_data = requests.get(img_url)
    temp.write(img_data.content)
    img = Image.open(temp.name)
    img = img.resize((200, 270))
    x = WIDTH/2 - 200/2 - 100
    y = HEIGHT/2 - 270/2
    photo_manga = ImageTk.PhotoImage(image=img)
    photo_manga_label.config(image=photo_manga, anchor=E)
    photo_manga_label.image=photo_manga
    photo_manga_label.place(x=x, y=y)

def set_manga_chapter():
    x = WIDTH/2 + 70
    y = HEIGHT/2 - 50
    manga_chapter.place(x=x, y=y)

def set_progress_bar():
    x = 70
    y = 325
    progress_bar['value'] = 0
    progress_bar.place(x=x, y=y)

def set_manga_chapter_nb(source):
    x = WIDTH/2 + 100
    y = HEIGHT/2
    manga_chapter_nb.config(text=str(B.get_manga_nb_chapters(source)))
    manga_chapter_nb.place(x=x, y=y)

def find_manga():
    source = B.request_manga(input_url.get())
    if source == None:
        set_error_message()
    else:
        disable_scene_1()
        set_manga_name(B.get_manga_name(source))
        set_photo_manga(source)
        set_button_download()
        set_manga_chapter()
        set_manga_chapter_nb(source)

def download_chapter(url, path, len_tab):
    global STOP_THREAD
    global STEP
    i = 0
    chapter = url.split('/')[-1]
    path = path + '\\' + chapter + '\\'
    source = B.request_url(url)
    print('=== Downloading chapter ' + chapter + '===' )

    soup = B.check_error_chapter(source)
    if soup == None:
        return

    B.my_mkdir(path)
    data = soup.find('select', id='pageMenu').find_all('option')

    for img_href in data:
        if STOP_THREAD == True:
            STOP_THREAD = False
            sys.exit(0)
        i = i + 1
        B.download_img(img_href['value'], path, i)
        STEP = STEP + 1/len(data)
        progress_bar['value'] = STEP * 100 / len_tab
        window.update_idletasks()
    print('')

def download_manga():
    global STEP
    soup = B.request_manga(input_url.get())
    name = B.get_manga_name(soup)
    path = B.PATH_DIR + '//' + name
    data = soup.find('div', id='chapterlist')
    STEP = 0

    if data == None:
        print('No chapter found')
        return

    B.my_mkdir(path)
    tab = data.find_all('a')
    len_tab = len(tab)
    for chapter in tab:
        download_chapter(B.MANGA_PANDA_URL + chapter['href'], path, len_tab)

def on_closing():
    window.destroy()
    temp.close()
    os.unlink(temp.name)
    sys.exit(0)

def main():
    enable_scene_1()
    window.mainloop()

WIDTH = 540
HEIGHT = 360
STOP_THREAD = False
STEP = 0

# creating window
window = Tk()
window.title("Mangapanda Scraper")
window.geometry(str(WIDTH) + 'x' + str(HEIGHT))
window.minsize(WIDTH, HEIGHT)
window.maxsize(WIDTH, HEIGHT)
window.config(background='#1BF186')
window.protocol("WM_DELETE_WINDOW", on_closing)
thread = threading.Thread(target=download_manga)
thread.daemon = True

# creating temp file
temp = tempfile.NamedTemporaryFile(delete=False)

# creating photos
photo_mangapanda = PhotoImage(file='mangapanda.png')
photo_manga = PhotoImage()

# creating labels
photo_mangapanda_label = Label(window, image=photo_mangapanda)
photo_manga_label = Label(window, imgage=None)
error = Label(window, text='NOT FOUND', bg='#1BF186', fg='red', font='Arial 18 bold')
manga_name = Label(window, bg='#1BF186', text='', font='Arial 20 bold')
manga_chapter = Label(window, bg='#1BF186', text='Chapters', font='Arial 18 bold')
manga_chapter_nb = Label(window, bg='#1BF186', text='', font='Arial 18')

# creating progress bar
progress_bar = ttk.Progressbar(window, length=400, mode='determinate')

# creating inputs
input_url = Entry(window, width=50)
input_url.insert(0, B.MANGA_PANDA_URL)

# creating buttons
button_find = Button(window, text="Find", command=find_manga)
button_download = Button(window, text="Download", command=start_dowload)

main()