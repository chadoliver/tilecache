import math

class Latitude:

    def __init__(self, latitude):

        self.latitude = float(latitude)

    def toIntegerAtZoom(self, zoom):
        n = 2.0 ** zoom
        lat_rad = math.radians(self.latitude)
        return int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)

class Longitude:

    def __init__(self, longitude):

        self.longitude = float(longitude)

    def toIntegerAtZoom(self, zoom):
        n = 2.0 ** zoom
        return int((self.longitude + 180.0) / 360.0 * n)
        
class Position:
    ''' represents a lat/long pair. Contructed from a fragment of the .map file. '''

    def __init__(self, string):

        components = string.split(",")
        lat_str = components[0].strip()
        long_str = components[1].strip()

        self.latitude = Latitude(lat_str)
        self.longitude = Longitude(long_str)

class LatitudeRange:

    def __init__(self, positionA, positionB):

        self.start = positionA.latitude
        self.end = positionB.latitude

    def atZoom(self, zoom):
        ''' This is an iterator that generates y-coordinates between the start and end points, for a
        specified zoom level. "for y in latitudeRange.atZoom(zoom):" '''

        start = self.start.toIntegerAtZoom(zoom)
        end = self.end.toIntegerAtZoom(zoom)
        if start > end:
            start, end = end, start
        
        for y in range(start, end+1):
            yield y
        

class LongitudeRange:

    def __init__(self, positionA, positionB):

        self.start = positionA.longitude
        self.end = positionB.longitude

    def atZoom(self, zoom):
        ''' This is an iterator that generates y-coordinates between the start and end points, for a
        specified zoom level. "for x in longitudeRange.atZoom(zoom):" '''

        start = self.start.toIntegerAtZoom(zoom)
        end = self.end.toIntegerAtZoom(zoom)
        if start > end:
            start, end = end, start
        
        for x in range(start, end+1):
            yield x
