from PIL import Image

from src.dcutils import DCUtils


class DCImage:

    __imageDir = ''
    __pilImage = None

    def __init__(self, imageDir):
        self.__imageDir = imageDir

        self.__pilImage = Image.open(r"%s" % imageDir)
        self.__pilImage = self.__pilImage.convert("RGB")

    def canHoldImage(self, dataImage):
        return DCUtils.isLargeEnoughImg(self.__pilImage, dataImage.getPilImage())

    def getPixelAccess(self):
        return self.__pilImage.load()

    def getPilImage(self):
        return self.__pilImage

    def getPilWidth(self):
        width, height = self.__pilImage.size
        return width

    def getPilHeight(self):
        width, height = self.__pilImage.size
        return height

    @staticmethod
    def createNewImage(height, width, savedir=r"../imgs/dataImage.png"):

        # creates a plain ol' white image
        image = Image.new("RGB", (width, height), (0, 0, 0))
        image.save(savedir)

        return DCImage(savedir)
