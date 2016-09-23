import logging
from src.dcutils import DCUtils

logger = logging.getLogger("stego")

class DCStego:

    __dcCarrierImage = None

    def __init__(self, dcCarrierImage):
        self.__dcCarrierImage = dcCarrierImage

    def __addHeaderInformation(self, totalDataPixels):

        #the totalCarrierPixels is the number of
        maxBytes, bitsNeeded = DCUtils.calculateMaxStorageCapacity(self.__dcCarrierImage.getPilImage())

        #go bitsNeeded far into the carrier image

        #then go backwards printing out the binary of the max bytes (print LSB -> MSB)

        #then 0 out everything else afterwards (this will be padding to the number)


    def addDataPixelImage(self, dcDataImage):

        cx = 0
        cy = 0
        carrierPixels = self.__dcCarrierImage.getPixelAccess()
        carrierHeight = self.__dcCarrierImage.getPilHeight()
        carrierWidth = self.__dcCarrierImage.getPilWidth()

        #add header information about the data image so we know how much to parse
        totalDataPixels = dcDataImage.getPilWidth() * dcDataImage.getPilHeight() * 3
        totalCarrierPixels = self.__dcCarrierImage.getPilWidth() * self.__dcCarrierImage.getPilHeight()

        cx, cy = self.__addHeaderInformation(totalDataPixels)

        dataPixels = dcDataImage.getPixelAccess()
        logger.info("DataPixel Width: " + str(dcDataImage.getPilWidth()))
        logger.info("DataPixel Height: " + str(dcDataImage.getPilHeight()))
        for dy in range(0, dcDataImage.getPilHeight()):
            for dx in range(0, dcDataImage.getPilWidth()):

                logger.info("Width: " + str(dy) + " Height: " + str(dx))
                dataPixel = dataPixels[dx, dy]
                dred, dgreen, dblue = dataPixel
                pixelList = [dred, dgreen,dblue]

                for index, plane in enumerate(pixelList):

                    carrierpixel1 = carrierPixels[cx, cy]
                    carrierpixel2 = None
                    carrierpixel3 = None

                    if (cx + 1) >= carrierWidth:
                        carrierpixel2 = carrierPixels[0, cy + 1]
                    else:
                        carrierpixel2 = carrierPixels[cx + 1, cy]

                    if (cx + 2) >= carrierWidth:
                        carrierpixel3 = carrierPixels[1, cy + 1]
                    else:
                        carrierpixel3 = carrierPixels[cx + 2, cy]


                    # we now have all the pixels in the carrier to put our data pixel into
                    r1,b1,g1 = carrierpixel1
                    r2,b2,g2 = carrierpixel2
                    r3,b3,g3 = carrierpixel3

                    carriers = [r1,b1,g1,r2,b2,g2,r3,b3,g3]

                    for i in range(0,8):
                        lsb = plane & 1

                        # if the carrier's lsb already matches the lsb of the data plane, don't do anything
                        if (carriers[i] & 1) != lsb:
                            if (carriers[i] & 1) == 1:
                                #the carrier has a 1 which means our lsb is 0. decrement carrier value
                                carriers[i] = carriers[i] - 1
                            else:
                                #the carrier has a 0 which means our lsb is a 1. increment the carrier value
                                carriers[i] = carriers[i] + 1

                    #set the planes back to their pixels
                    carrierpixel1 = (carriers[0], carriers[1], carriers[2])
                    carrierpixel2 = (carriers[3], carriers[3], carriers[4])
                    carrierpixel3 = (carriers[5], carriers[6], carriers[7])

                    #set the pixels back to their position in the carrier image array
                    carrierPixels[cx,cy] = carrierpixel1

                    if (cx + 1) >= carrierWidth:
                        carrierPixels[0, cy + 1] = carrierpixel2
                    else:
                        carrierPixels[cx + 1, cy] = carrierpixel2

                    if (cx + 2) >= carrierWidth:
                        carrierPixels[1, cy + 1] = carrierpixel3
                    else:
                        carrierPixels[cx + 2, cy] = carrierpixel3


                    # now increment our position in the carrier image for the next loop
                    if (cx + 3) >= carrierWidth:
                        cy = cy + 1
                        cx = abs(carrierWidth - (cx + 3))

    def parseDataPixelImage(self):
        print ("Nothing Happen s Here Yet!")

    def getCarrierImage(self):
        return self.__dcCarrierImage.getPilImage()

'''
        for y in range(self.__dcCarrierImage.getPilWidth()):
            for x in range(self.__dcCarrierImage.getPilHeight()):
                tuple = carrierPixels[x,y]
                print(tuple)
'''

'''

dblue = dataImage.split()

'''



'''
red2 = ImageMath.eval("convert(a&0xFE|b&0x1,'P')", a=cred, b=dred)
green2 = ImageMath.eval("convert(a&0xFE|b&0x1,'P')", a=cgreen, b=dgreen)
blue2 = ImageMath.eval("convert(a&0xFE|b&0x1,'P')", a=cblue, b=dblue)

out = Image.merge("RGB", (red2, green2, blue2))
out.save(r"../../imgs/stego.gif")
'''
