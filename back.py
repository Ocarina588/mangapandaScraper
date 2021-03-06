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