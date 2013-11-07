'''
How to use:
    0) Go to http://www.mapcacher.com/ and generate a .map file. Use the "OpenStreetMaps.org Maps
    (Mapnik Renderer)" option.
    1) Download one or more .map files into ./input/
    2) Run cacher.py.
    3) The downloaded images will be written into ./output/
'''

import Queue
from jobProducer import JobProducer
from workerPool import WorkerPool

print 'starting to download files'

workers = []
tileQueue = Queue.Queue(maxsize=0)

producer = JobProducer(tileQueue)
workerPool = WorkerPool(tileQueue)

producer.start()
workerPool.start()

producer.join()
workerPool.join()

print 'done'
