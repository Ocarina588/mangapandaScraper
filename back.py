from bs4 import BeautifulSoup
import requests
import os
import sys

MANGA_PANDA_URL = 'http://www.mangapanda.com'
PATH_DIR = ''

def request_url(url):
    source = requests.get(url)
    if source.status_code != 200:
        return (None)
    return (source.text)

def request_manga(url):
    print(url)
    if url.find(MANGA_PANDA_URL + '/') != 0:
        return (None)
    if len(url.split(MANGA_PANDA_URL + '/')[1].split('/')) != 1:
        return (None)
    source = request_url(url)
    if source == None:
        return None
    return (BeautifulSoup(source, 'lxml'))

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
    return (name)

def get_manga_nb_chapters(soup):
    data = soup.find('div', id='chapterlist').find_all('a')
    return (len(data))

def check_error_chapter(source):
    if source == None:
        print('error: chapter not found')
        return (None)

    soup = BeautifulSoup(source, 'lxml')

    if soup.find('select', id='pageMenu') == None:
        print('error: chapter not found')
        return (None)
    return (soup)

def download_chapter(url, path):
    i = 0
    chapter = url.split('/')[-1]
    path = path + '\\' + chapter + '\\'
    source = request_url(url)

    print('=== Downloading chapter ' + chapter + '===' )

    soup = check_error_chapter(source)
    if soup == None:
        return

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

def get_begining_chapter(max):
    print('There\'s ' + str(max) + ' chapters')
    while (1):
        try:
            begining = int(input('Which chapter do you wanna start with?: '))
        except:
            print('The chapter need to be a integer')
            continue
        if begining <= max and begining > 0:
            return (begining)
        else:
            print('The chapter doesn\'t exist')
