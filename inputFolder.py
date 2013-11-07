import config
from tile import Tile
import position
import os

class Plane:
    ''' This represents one zoom level of a region. '''

    def __init__(self, mapType, latitudeRange, longitudeRange, zoom):

        self.mapType = mapType
        
        self.latitudeRange = latitudeRange
        self.longitudeRange = longitudeRange

        self.zoom = zoom

    def __iter__(self):
        
        for x in self.longitudeRange.atZoom(self.zoom):
            for y in self.latitudeRange.atZoom(self.zoom):
                tile = Tile(self.mapType, config.STYLE_ID, config.RESOLUTION, self.zoom, x, y)
                yield tile
        raise StopIteration

    def __str__(self):
        return "%i, (x: %i, y: %i), (x: %i, y: %i)" %(self.zoom, self.southWest.x, self.southWest.y, self.northEast.x, self.northEast.y)

        
class Region:
    ''' This class represents a region of tiles. In the .map file, each line (after the first)
    describes a single region. '''

    def __init__(self, mapType, line):
        
        fragments = line.split(":")   # [zoom, bottomLeftCorner, topRightCorner]

        zoom = fragments[0].split("-")
        self.minZoom = int(zoom[0])
        self.maxZoom = int(zoom[1])

        southWest = position.Position(fragments[1])
        northEast = position.Position(fragments[2])
        self.latitudeRange = position.LatitudeRange(southWest, northEast)
        self.longitudeRange = position.LongitudeRange(southWest, northEast)

        self.mapType = mapType

    def __iter__(self):
        
        for zoom in range(self.minZoom, self.maxZoom+1):
            plane = Plane(self.mapType, self.latitudeRange, self.longitudeRange, zoom)
            for tile in plane:
                yield tile
        raise StopIteration
        

class MapFile:
    ''' This class represents a .map file. It hides all details about reading the file, and acts
    like a generator which returns Region objects, so we can say: "for region in MapFile(path):" '''
    
    def __init__(self, path):

        self.path = './input/' + path

        with open(self.path, 'r') as f:
            lines = f.readlines()
            self.mapType = lines[0]
            self.regionLines = lines[1:]

    def __iter__(self):
        
        for line in self.regionLines:
            region = Region(self.mapType, line)
            for tile in region:
                yield tile
        raise StopIteration


class InputFolder:
    ''' This class represents a folder of .map files." '''

    def __init__(self, path):
        self.path = path

    def __iter__(self):
        
        for filepath in os.listdir(self.path):
            if filepath.endswith(".map"):
                mapfile = MapFile(filepath)
                for tile in mapfile:
                    yield tile
        raise StopIteration
