import config
from tile import Tile
import threading
import os

class OutputFolder:

    lock = threading.Lock()
    
    def __init__(self, path):
        self.path = path

    def write(self, tile):

        with self.__class__.lock:
            with open(tile.getFilepath(), 'wb') as outputFile:
                outputFile.write(tile.image)

    def __contains__(self, tile):

        with self.__class__.lock:
            tilePath = tile.getFilepath()
            if os.path.exists(tilePath):
                return True
            else:
                return False
        
    def createRequiredFolders(self, tile):

        with self.__class__.lock:
            folderPath = tile.getFolderPath()
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)
