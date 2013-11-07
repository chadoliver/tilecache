import config

class Tile:

    def __init__(self, mapType, style, resolution, zoom, x, y):

        self.mapType = mapType.strip()
        self.style = style
        self.resolution = resolution
        self.zoom = zoom
        self.x = x
        self.y = y
        self.image = None   # will hold downloaded tile image

    def getURL(self):
        pattern = "http://b.tile.cloudmade.com/%s/%i/%i/%i/%i/%i.png"
        return pattern %(config.API_KEY, config.STYLE_ID, config.RESOLUTION, self.zoom, self.x, self.y)

    def getFilepath(self):

        return "%s/%i.png" %(self.getFolderPath(), self.y)

    def getFolderPath(self):

        tilesetLabel = '%s-%i-%i' %(self.mapType, self.style, self.resolution)
        path = "%s/%s/%i/%i/" %(config.OUTPUT_ROOT_FOLDER, tilesetLabel, self.zoom, self.x)
        return path

    def __repr__(self):
        return "(%i, %i, %i)" %(self.zoom, self.x, self.y)
