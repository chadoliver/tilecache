''' workerPool.py '''

import config
from tile import Tile
from outputFolder import OutputFolder
from Queue import Queue
import threading
import urllib2

class ProgressCounter:

    def __init__(self, initialValue=0):

        self.value = initialValue
        self.lock = threading.Lock()

    def increment(self):
        
        with self.lock:
            self.value += 1
            print "processed %i tiles" %self.value

    def getValue(self):
        
        with self.lock:
            return self.value

class Worker:

    def __init__(self, tileQueue, progressCounter):

        self.tileQueue = tileQueue
        self.thread = None
        self.isTimeToDie = False
        self.progressCounter = progressCounter

    def doWork(self):

        outputFolder = OutputFolder(config.OUTPUT_ROOT_FOLDER)
        
        while True:
            tile = self.tileQueue.get()
            tile.image = self.download(tile)
            outputFolder.write(tile)
            self.tileQueue.task_done()  # this controls queue.join()
            self.progressCounter.increment()

    def download(self, tile):

        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }

        request = urllib2.Request(tile.getURL(), headers=headers)
        response = urllib2.urlopen(request)
        image = urllib2.urlopen(request).read()

        return image

    def start(self):

        self.thread = threading.Thread(target=self.doWork)
        self.thread.start()

    def join(self):
        
        self.thread.join()

class WorkerPool:

    def __init__(self, tileQueue, numWorkers=config.NUM_WORKER_THREADS):

        self.tileQueue = tileQueue
        self.progressCounter = ProgressCounter()
        
        self.workers = []
        self.numWorkers = numWorkers


    def start(self):

        print 'starting worker threads'
        
        for i in range(self.numWorkers):
            worker = Worker(self.tileQueue, self.progressCounter)

            # Making our threads 'daemons' means that we don't need to join() them before our program
            # finishes. To make sure all jobs are completed, we use tileQueue.join() instead.
            worker.daemon = True
            
            worker.start()
            self.workers.append(worker)

    def join(self):

        self.tileQueue.join()   # wait until all tiles on the queue have been fully processed.

        processedJobs = self.progressCounter.getValue()
        if processedJobs == 0:
            print "There was nothing to download. (Perhaps they were already downloaded?)"
        elif processedJobs == 1:
            print "1 tile was downloaded"
        elif processedJobs > 1:
            print "%i tiles were downloaded" %processedJobs
        
            
            
        
            

    
