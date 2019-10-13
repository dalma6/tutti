import logging, urllib, json
from celery import Celery

logging.basicConfig(level=logging.DEBUG)

"""
    make Celery object
"""
app = Celery('task',
             backend='rpc://',
             broker='pyamqp://guest@localhost//'
             )

"""
    update celery configuration to accept pickle
"""
app.conf.update(
    CELERY_ACCEPT_CONTENT = ['pickle'],
    CELERY_TASK_SERIALIZER = 'pickle',
    CELERY_RESULT_SERIALIZER = 'pickle',
)

"""
send a get request to the api, get info about items and dump them into a .txt file
    args:
        g -- Grab object
        i -- page number
        params -- get request parameters
        x_tutti_hash -- current session token
        outfile -- .txt for for dumping results
    headers:
        X-Tutti-Hash -- session token
        Referer -- previous page
"""
@app.task
def doTask(g, i, params, x_tutti_hash, outfile):
    headers = {
        'X-Tutti-Hash': x_tutti_hash,
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'https://www.tutti.ch/api/v10/de/li/ganze-schweiz/o=' + str(i-1)
    }
    g.go("https://www.tutti.ch/api/v10/list.json?" + urllib.parse.urlencode(params), headers=headers)
    for item in g.doc.json['items']:
        with open(outfile, 'a') as outfile_task:
            json.dump(item, outfile_task)
            outfile_task.write('\n')
