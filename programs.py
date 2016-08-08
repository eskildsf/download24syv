import requests, csv
json = requests.get('http://api.radio24syv.dk/programs').json()
programs = []
for e in [e for e in json if 'videoProgramId' in e]:
    programs.append({'title': e['name'], 'videoProgramId': str(e['videoProgramId'])})
    print('%s\t %s' % (e['videoProgramId'], e['name']))

with open('programs.csv', 'wb') as f:
    w = csv.DictWriter(f, ['title', 'videoProgramId'])
    w.writeheader()
    for row in programs:
        w.writerow(dict((k, v.encode('utf-8')) for k, v in row.iteritems()))
