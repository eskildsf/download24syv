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
# and put in the videoProgramId below
programs = (
'13976201', # Q & A
'6555368', # Huxi og det Gode Gamle Folketing
'13792677', # Huxi og det Gode Gamle Folketing Sammendrag
'10839671', # Den Korte Radioavis
'13973704', # Se Europa og Do
)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def podcasts(videoProgramId):
    p = []
    url = 'http://api.radio24syv.dk/podcasts/program/%s' % videoProgramId
    json = requests.get(url, params={'size': 5}, headers=headers).json()
    for e in json:
        url = 'http://arkiv.radio24syv.dk%s' % e['audioInfo']['url']
        date = datetime.strptime(e['publishInfo']['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
        p.append({'title': e['programInfo']['title'], 'url': url, 'date': date})
    return p

def download(podcast):
    file_name = 'podcasts/'+slugify(podcast['title']+'-'+podcast['date'].strftime('%Y-%m-%d'))+'.mp3'
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
