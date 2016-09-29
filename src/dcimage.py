from PIL import Image
from src.dcutils import DCUtils
from Crypto.Cipher import DES3
from Crypto import Random

import ntpath
import io



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

    def encryptImage(self, password="Sixteen byte key"):

        # password must be 16 bytes OR 16 characters long

        iv = Random.new().read(DES3.block_size)
        cipher = DES3.new(password.encode(), DES3.MODE_OFB, iv)

        bytesOfImage = self.__pilImage.tobytes()
        imageSize = self.__pilImage.size
        encryptedImage = iv + cipher.encrypt(bytesOfImage)

        self.__pilImage = Image.frombytes("RGB", imageSize, encryptedImage)

        self.__pilImage.show()

    def decryptImage(self, password="Sixteen byte key"):

        bytesOfImage = self.__pilImage.tobytes()
        imageSize = self.__pilImage.size

        iv = bytesOfImage[:DES3.block_size]
        cipher = DES3.new(password.encode(), DES3.MODE_OFB, iv)
        decryptedImage = cipher.decrypt(bytesOfImage[DES3.block_size:])

        #self.__pilImage = Image.frombytes("RGB", imageSize, decryptedImage)
        self.__pilImage = Image.open(io.BytesIO(decryptedImage))

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
