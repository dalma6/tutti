import logging, urllib, rstr, json
from grab import Grab

logging.basicConfig(level=logging.DEBUG)

g = Grab()

"""
    get params:
        limit -- number of items per page
        with_all_regions -- do we want items from all regions of Switzerland
"""
params = {
    'limit': '30',
    'with_all_regions': 'true',
}

"""
    generate a random string out of alphabet letters and digits in format 7-4-4-4-12 
    where e.g. 7 is the number of characters in a substring
"""
pattern = 'abcdefghijklmnopqrstuvwxyz0123456789'
x_tutti_hash = rstr.rstr(pattern, 7) + '-' + rstr.rstr(pattern, 4) + '-' + rstr.rstr(pattern, 4) + '-' \
               + rstr.rstr(pattern, 4) + '-' + rstr.rstr(pattern, 12)
"""
    headers for the get request:
        X-Tutti-Hash -- session token
"""
headers = {
    'X-Tutti-Hash': x_tutti_hash,
    'Accept-Encoding': 'gzip, deflate'
}

"""
    send first get request to the api, get info about items and dump them into a .txt file
"""
with open('out.txt', 'w') as outfile:
    g.go("https://www.tutti.ch/api/v10/list.json?" + urllib.parse.urlencode(params), headers=headers)
    for item in g.doc.json['items']:
        json.dump(item, outfile)
        outfile.write('\n')

total_items = g.doc.json['search_total']
num_pages = int(total_items / 30) if total_items % 30 == 0 else int(total_items / 30) + 1

from tutti.task import doTask
i = 2
"""
    loop exit condition changed from num_pages to 100 to avoid celery's BacklogLimitExceeded error
"""
#while (i < num_pages):
while (i < 100):
    r = doTask.delay(g, i, params, x_tutti_hash, outfile.name)
    r.ready()
    i += 1

"""
    zip results file
"""
import zipfile
zipfile.ZipFile('outfile.zip', 'w').write('out.txt')
