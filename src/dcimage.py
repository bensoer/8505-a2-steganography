from PIL import Image

from src.dcutils import DCUtils

import ntpath


class DCImage:

    __imageDir = ''
    __pilImage = None
    __imageName = ''

    def __init__(self, imageDir):
        self.__imageDir = imageDir

        self.__pilImage = Image.open(r"%s" % imageDir)
        self.__pilImage = self.__pilImage.convert("RGB")

        # get the image name from the dir
        head, tail = ntpath.split(imageDir)
        self.__imageName = tail or ntpath.basename(head)
        self.__imageName = self.__imageName.replace(" ", "")

    def getImageNameLength(self):
        return len(self.__imageName)

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

    def getImageName(self):
        return self.__imageName

    @staticmethod
    def createNewImage(height, width, savedir=r"../imgs/dataImage.png"):

        # creates a plain ol' white image
        image = Image.new("RGB", (width, height), (0, 0, 0))
        image.save(savedir)

        return DCImage(savedir)
