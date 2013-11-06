'''
How to use:
    0) Go to http://www.mapcacher.com/ and generate a .map file. Use the "OpenStreetMaps.org Maps
    (Mapnik Renderer)" option.
    1) Download one or more .map files into ./input/
    2) Run cacher.py.
    3) The downloaded images will be written into ./output/
'''

import os
import math
import time
import random
import urllib2

INPUT_FOLDER = "./input"
OUTPUT_ROOT_FOLDER = "./output/"
API_KEY = "8ee2a50541944fb9bcedded5165f09d9"        # This needs to be replaced
STYLE_ID = 1
RESOLUTION = 256

class Tile:

    def __init__(self, zoom, x, y):

        self.zoom = zoom
        self.x = x
        self.y = y

    def cache(self):
        ''' This downloads the file and writes it to disk. '''

        print self.url()

        tileSetRoot = "%s/%i-%i/" %(OUTPUT_ROOT_FOLDER, STYLE_ID, RESOLUTION)
        outputFolder = "%s/%i/%i/" %(tileSetRoot, self.zoom, self.x)
        outputFilename = "%i.png" %self.y

        if os.path.exists(outputFolder+outputFilename):
            # we assume that if the file exists, then it was downloaded in the past (i.e. assume that
            # it's not corrupted or a renamed Word document, etc). Note that this also catches duplicates
            # in the same batch.
            return

        if not os.path.exists(outputFolder):    # create the output folder if it doesn't exist.
            os.makedirs(outputFolder)           # makedirs is recursive; it makes *all* required folders on the path.

        image = self.download()
        
        outputFile = open(outputFolder + outputFilename,'wb')
        outputFile.write(image)
        outputFile.close()

    def download(self):
        
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }

        request = urllib2.Request(self.url(), headers=headers)
        response = urllib2.urlopen(request)
        image = urllib2.urlopen(request).read()
        return image

    def url(self):
        pattern = "http://b.tile.cloudmade.com/%s/%i/%i/%i/%i/%i.png"
        return pattern %(API_KEY, STYLE_ID, RESOLUTION, self.zoom, self.x, self.y)

    def __str__(self):
        return self.url()

class Coordinate:

    def __init__(self, string):

        components = string.split(",")
        self.latitude = float(components[0].strip())     # in degrees
        self.longitude = float(components[1].strip())    # in degrees

    def setZoomLevel(self, zoom):

        long_deg = self.longitude
        lat_rad = math.radians(self.latitude)
        n = 2.0 ** zoom
        
        self.zoom = zoom
        self.x = int((long_deg + 180.0) / 360.0 * n)
        self.y = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)

class Plane:
    ''' This represents one zoom level of a region. '''

    def __init__(self, southWest, northEast, zoom):

        self.southWest = southWest
        self.southWest.setZoomLevel(zoom)
        
        self.northEast = northEast
        self.northEast.setZoomLevel(zoom)

        self.zoom = zoom

    def iterate(self):
        
        for x in range(self.southWest.x, self.northEast.x+1):       # the +1 makes the range inclusive: range(5,5) gives [], but we want [5].
            for y in range(self.northEast.y, self.southWest.y+1):
                yield Tile(self.zoom, x, y)

    def __str__(self):
        return "%i, (x: %i, y: %i), (x: %i, y: %i)" %(self.zoom, self.southWest.x, self.southWest.y, self.northEast.x, self.northEast.y)

        
class Region:
    ''' This class represents a region of tiles. In the .map file, each line (after the first)
    describes a single region. '''

    def __init__(self, line):
        
        fragments = line.split(":")   # [zoom, bottomLeftCorner, topRightCorner]

        zoom = fragments[0].split("-")
        self.minZoom = int(zoom[0])
        self.maxZoom = int(zoom[1])

        self.southWest = Coordinate(fragments[1])
        self.northEast = Coordinate(fragments[2])

    def iterate(self):

        for zoom in range(self.minZoom, self.maxZoom):
            yield Plane(self.southWest, self.northEast, zoom)

    def __str__(self):
        return "(x: %i, y: %i), (x: %i, y: %i)" %(self.southWest.x, self.southWest.y, self.northEast.x, self.northEast.y)
        

class MapFile:
    ''' This class represents a .map file. It hides all details about reading the file, and acts
    like a generator which returns Region objects, so we can say: "for region in MapFile(path):" '''
    
    def __init__(self, path):

        self.path = './input/' + path
        self.mapFile = open(self.path, 'r')

        self.lines = self.mapFile.readlines()

    def iterate(self):
        for line in self.lines[1:]:
            yield Region(line)

    def __str__(self):
        return self.path
        

class MapFolder:
    ''' This class represents a folder of .map files." '''

    def __init__(self, path):
        self.path = path
    
    def iterate(self):
        for filepath in os.listdir(self.path):
            if filepath.endswith(".map"):
                yield MapFile(filepath)


for mapFile in MapFolder(INPUT_FOLDER).iterate():
    for region in mapFile.iterate():
        for plane in region.iterate():
            for tile in plane.iterate():
                tile.cache()
                #time.sleep(random.uniform(0.1, 3.0))   # uncomment this to throttle the requests.

print 'done.'



