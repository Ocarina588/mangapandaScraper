from bs4 import BeautifulSoup
import requests
import os
import sys

MANGA_PANDA_URL = 'http://www.mangapanda.com' 

def request_url(url):
    try:
        source = requests.get(url).text
    except:
        return (None)
    return (source)

def request_manga():
    source = request_url(input('manga url: '))
    if (source == None):
        print('error: manga not found')
        sys.exit(1)
    return (source)

def request_img(url):
    source = request_url(url)
    if (source == None):
        print('error: Didn\'t find the img page')
        return (None)
    soup = BeautifulSoup(source, 'lxml')
    src = soup.find('div', id='imgholder').find('img', id='img')['src']
    img =  requests.get(src)
    if img == None:
        print('error: couldn\'t find the image n' + img_href.split('/')[-1])
    return (img)

def download_img(img_href, path, i):
    img = request_img(MANGA_PANDA_URL + img_href)
    if (img == None):
        return
    name = str(i) + '.jpg'
    try:
        if img.status_code == 200:
            with open(path + name, 'wb') as f:
                f.write(img.content)
                print(name + ' created')
        else:
            print('error: status code ' + str(img.status_code))
    except OSError as error:
        print(error)
        return
    
def get_manga_dir():
    while (1):
        path = input('where do you want to download the manga? (need full path): ')
        if os.path.isdir(path) == True:
            path = path + '\\'
            return (path)
        else:
            print('the path given isn\'t a directory')

def check_good_name(name):
    for x in [':', '\\', '/', '<', '>', '?', '!', '*', '|']:
            if x in name:
                return (False)
    return (True)

def get_manga_name(soup):
    name = soup.find('div', id='mangaproperties').find('h1').text
    status = check_good_name(name)
    while (status == False):
        name = input('Manga name contains forbidden characters, pleas rename the folder: ')
        status = check_good_name(name)
    return (name)

def download_chapter(url, path):
    i = 0
    chapter = url.split('/')[-1]
    path = path + '\\' + chapter + '\\'
    source = request_url(url)

    print('=== Downloading chapter ' + chapter + '===' )
    if (source == None):
        print('error: chapter not found')
        return
    
    soup = BeautifulSoup(source, 'lxml')
    my_mkdir(path)

    for img_href in soup.find('select', id='pageMenu').find_all('option'):
        i = i + 1
        download_img(img_href['value'], path, i)
    print('')

def my_mkdir(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)
        sys.exit(1)

def download_manga():
    source = request_manga()
    soup = BeautifulSoup(source, 'lxml')
    name = get_manga_name(soup)
    path = get_manga_dir() + name
    data = soup.find('div', id='chapterlist')

    my_mkdir(path)
    
    for chapter in data.find_all('a'):
        download_chapter(MANGA_PANDA_URL + chapter['href'], path)

download_manga()