from PIL import Image
from dcutils import DCUtils

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
        '''
        getImageNameLength gets the length of the image name it represents
        :return: Int - the size of the name of the image
        '''
        return len(self.__imageName)

    def canHoldImage(self, dataImage):
        '''
        canHoldImage uses the DCUtils isLArgeEnoughImg method to determine if the passed in image will fit inside this
        DCImage
        :param dataImage: DCImage - A wrapper of an Image object representing a data image that may be stored in this
        image
        :return: Boolean - True or Flase as to whether the dataImage will fit or not
        '''
        return DCUtils.isLargeEnoughImg(self.__pilImage, dataImage.getPilImage())

    def getPixelAccess(self):
        '''
        getPixelAccess is a convenience method that gets the PixelAccess object of the Image object the DCImage wraps
        :return: PixelAccess - An object representing the pixels of the Image
        '''
        return self.__pilImage.load()

    def getPilImage(self):
        '''
        getPilImage is a convenience method that returns the origin Image object being wrapped by the DCImage class
        :return: Image - The image being wrapped by the DCImage class
        '''
        return self.__pilImage

    def getPilWidth(self):
        '''
        getPilWidth gets the width of the Image
        :return: Int - The width of the image
        '''
        width, height = self.__pilImage.size
        return width

    def getPilHeight(self):
        '''
        getPilHeight gets the height of the Image
        :return: Int - The height of the image
        '''
        width, height = self.__pilImage.size
        return height

    def getImageName(self):
        '''
        getImageName gets the name fo the image that was parsed off the name of the file directory. This name
        includes the extensions
        :return: String - the filename of the image based of the directory
        '''
        return self.__imageName

    @staticmethod
    def createNewImage(height, width, savedir=r"../imgs/dataImage.png"):
        '''
        createNewImage is a helper constructor that creates a new Image object and saves it so that it can be imported
        and used in the default manner of the DCImage.
        :param height: Int - the height of the image being created
        :param width: Int - the width of the image being created
        :param savedir: String - the location the image will be saved
        :return: DCImage - An instance of the DCImage object after being created
        '''

        # creates a plain ol' white image
        image = Image.new("RGB", (width, height), (0, 0, 0))
        image.save(savedir)
        image.close()

        return DCImage(savedir)
