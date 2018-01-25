import requests, csv

json = requests.get('http://api.radio24syv.dk/programs').json()

programs = []
for e in [e for e in json if 'videoProgramId' in e]:
    programs.append({'name': e['name'].encode('utf-8'), 'videoProgramId': str(e['videoProgramId'])})
    print('%s\t %s' % (e['videoProgramId'], e['name'].encode('utf-8')))

with open('programs.csv', 'wb') as f:
    w = csv.DictWriter(f, ['name', 'videoProgramId'])
    w.writeheader()
    for row in programs:
        w.writerow(dict((k, v) for k, v in row.iteritems()))
