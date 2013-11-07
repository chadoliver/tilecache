import config
from tile import Tile
from inputFolder import InputFolder
from outputFolder import OutputFolder
from Queue import Queue
import threading

class JobProducer:

    ''' This class represents a thread which populates a Queue.Queue() with Tile() objects. The Tile
    class is just a convenient of packaging all metadata relating to a tile image; in this case the
    tiles act as job descriptors, to be processed by the worker queues. '''

    def __init__(self, tileQueue):

        self.tileQueue = tileQueue
        self.thread = None

    def generateJobs(self):
        
        outputFolder = OutputFolder(config.OUTPUT_ROOT_FOLDER)
        inputFolder = InputFolder(config.INPUT_FOLDER)

        for tile in inputFolder:
            if tile not in outputFolder:
                outputFolder.createRequiredFolders(tile)    # recursively create any required folders, if they don't already exist.
                self.tileQueue.put(tile, block=True)        # put the tile on the queue, to be downloaded and saved by a worker thread.

        print "generated all tiles"

    def start(self):

        print 'starting boss thread'
        self.thread = threading.Thread(target=self.generateJobs)
        self.thread.start()

    def join(self):
        
        self.thread.join()
