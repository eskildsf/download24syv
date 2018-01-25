#!/data/tools/download24syv/env/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from slugify import slugify
from os.path import isfile
from datetime import datetime
import requests

# API Information
# http://api.radio24syv.dk/Podcasts.html
# http://api.radio24syv.dk/Programs.html

# Find programs at
# http://api.radio24syv.dk/programs
# and put the videoProgramId into the list below
programs = (
'13976201', # Q & A
'6555368', # Huxi og det Gode Gamle Folketing
'10839671', # Den Korte Weekendavis
'3843419', # Cordua & Steno
'12144388', # Politiradio
#'13973671', # 24 spm til prof
)

storage = '/data/usb/podcasts/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def podcasts(videoProgramId):
    p = []
    url = 'http://api.radio24syv.dk/podcasts/program/%s' % videoProgramId
    json = requests.get(url, params={'size': 2}, headers=headers).json()
    for e in json:
        url = 'http://arkiv.radio24syv.dk%s' % e['audioInfo']['url']
        date = datetime.strptime(e['publishInfo']['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
        p.append({'title': e['programInfo']['title'], 'url': url, 'date': date, 'part': e['part'],})
    print(p)
    return p

def download(podcast):
    if podcast['part'] is None:
        part = ''
    else:
        part = '-'+podcast['part'][1:2]
    file_name = storage+slugify(podcast['title']+'-'+podcast['date'].strftime('%Y-%m-%d'))+part+'.mp3'
    if isfile(file_name):
        return file_name
    r = requests.get(podcast['url'], stream=True, headers=headers)
    with open(file_name, 'wb') as f:
        print('Downloading %s' % file_name, end='')
        for chunk in r.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)
                print('.', end='')
    print('')
    return file_name

if __name__ == '__main__':
    for program in programs:
        for podcast in podcasts(program):
            download(podcast)
