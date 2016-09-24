import logging
import math
from src.dcutils import DCUtils

logger = logging.getLogger("stego")

class DCStego:

    __dcCarrierImage = None

    def __init__(self, dcCarrierImage):
        self.__dcCarrierImage = dcCarrierImage

    def __getHeaderInformation(self):

        #get information about our carrier image
        maxBytes, bitsNeeded = DCUtils.calculateMaxStorageCapacity(self.__dcCarrierImage.getPilImage())

        pixelsNeeded = math.ceil(bitsNeeded / 3) #rounding up to the nearest pixel

        ex = (pixelsNeeded - 1) # minus 1 to get the index
        ey = 0

        # make sure we wrap around if how far in we need to go take multiple rows
        carrierWidth = self.__dcCarrierImage.getPilWidth()
        while ex >= carrierWidth:
            ex = abs(ex - carrierWidth)
            ey = ey + 1

        totalDataPixels = 0

        logger.debug("Last Pixel Point Index. X: " + str(ex) + " Y: " + str(ey))

        binaryBeforeProcessing = ""
        # now loop forward through the carrier from 0 to the end ex and ey pixels
        carrierPixels = self.__dcCarrierImage.getPixelAccess()
        for cy in range(0, ey + 1):
            for cx in range(0, ex + 1):
                logger.debug("Pixel Index: X: " + str(cx) + " Y: " + str(cy))
                carrierPixel = carrierPixels[cx,cy]
                cred, cgreen, cblue = carrierPixel
                pixelList = [cred,cgreen,cblue] # put them in forward order
                logger.debug("Initial Value: " + str(pixelList))

                for plane in pixelList:
                    totalDataPixels <<= 1

                    lsb = (plane & 1)

                    logger.debug("BEFORE: Plane: " + str(plane) + " As Binary: " + bin(plane) + " LSB Of Data: " + str(lsb))
                    binaryBeforeProcessing += str(lsb)  # were reading MSB -> LSB so should append to the end
                    if lsb == 1:
                        totalDataPixels |= 1
                    else:
                        totalDataPixels &= ~1

                    logger.debug("Running Binary: " + bin(totalDataPixels))
                    logger.debug("Running Value: " + str(totalDataPixels))

        logger.debug("Binary Of TotalDataPixels: " + bin(totalDataPixels))
        logger.debug("Binary Before Processing: " + binaryBeforeProcessing)

        # check if ex +1 is too far
        if (ex + 1) > carrierWidth:
            ex = 0
            ey = ey +1
        else:
            ex = ex + 1

        return (ex, ey, totalDataPixels)

    def __addHeaderInformation(self, totalDataBytes):

        logger.debug(" -- PROCESING HEADER INFORMATION INTO CARRIER -- ")

        logger.debug("Total Bytes In Data Image Is: " + str(totalDataBytes) + ". This Number Will Be Placed Into The"
            + " Header")
        logger.debug("In Binary That Is: " + bin(totalDataBytes))

        maxBytes, bitsNeeded = DCUtils.calculateMaxStorageCapacity(self.__dcCarrierImage.getPilImage())
        logger.debug("Bits Needed To Store Max Carrier Capacity: " + str(bitsNeeded))

        #go bitsNeeded far into the carrier image

        pixelsNeeded = math.ceil(bitsNeeded / 3) # round to the nearest pixel

        sx = (pixelsNeeded - 1) # minus 1 to get the index
        sy = 0

        # make sure we wrap around if how far in we need to go take multiple rows
        carrierWidth = self.__dcCarrierImage.getPilWidth()
        while sx >= carrierWidth:
            sx = abs(sx - carrierWidth)
            sy = sy +1

        logger.debug("Last Pixel Point Index. X: " + str(sx) + " Y: " + str(sy))

        #then go backwards printing out the binary of the max bytes (print LSB -> MSB)

        binaryBeforeProcessing = ""
        binaryAfterProcessing = ""

        carrierPixels = self.__dcCarrierImage.getPixelAccess()
        for cy in range(sy, -1, -1):
            for cx in range(sx, -1, -1):
                logger.debug("Pixel Index: X: " + str(cx) + " Y: " + str(cy))
                carrierPixel = carrierPixels[cx, cy]
                cred, cgreen, cblue = carrierPixel
                pixelList = [cblue, cgreen, cred] # note that this is backwards
                logger.debug("Initial Value: " + str(pixelList))

                for index, plane in enumerate(pixelList):
                    lsb = (totalDataBytes & 1)

                    binaryBeforeProcessing = str(plane & 1) + binaryBeforeProcessing

                    logger.debug("BEFORE: Plane: " + str(plane) + " As Binary: " + bin(plane) + " LSB Of Data: " + str(lsb))

                    if lsb == 1:
                        plane |= 1
                    else:
                        plane &= ~1

                    binaryAfterProcessing = str(plane & 1) + binaryAfterProcessing
                    pixelList[index] = plane

                    logger.debug("AFTER: Plane: " + str(plane) + " As Binary: " + bin(plane) + " LSB Of Data: " + str(lsb))
                    # bit shift over to be able to fetch the next least significant bit
                    totalDataBytes >>= 1
                    # this will automaticaly zero out and pad until we fill the designated space

                logger.debug("PostProcessed: In Pixel List: " + str(pixelList))
                carrierPixels[cx,cy] = (pixelList[2], pixelList[1], pixelList[0])

                #print(str(pixelList[2]) + " " + str(pixelList[1]) + " " + str(pixelList[0]))
                #carrierPixels[cx,cy] = (0, 0, 0)
                logger.debug("PostProcessed: In Carrier Pixels: " + str(carrierPixels[cx,cy]))

        # now return the results, giving the pixel coordinates to the start position of the image data

        logger.debug("Binary Before Processing: " + binaryBeforeProcessing)
        logger.debug("Binary After Processing: " + binaryAfterProcessing)
        logger.debug(" -- END OF PROCESING HEADER INFORMATION INTO CARRIER -- ")
        #logger.setLevel(logging.INFO)

        # check if sx +1 is too far
        if (sx + 1) >= carrierWidth:
            sx = 0
            sy = sy +1
        else:
            sx = sx + 1

        return (sx, sy)


    def addDataPixelImage(self, dcDataImage):


        carrierPixels = self.__dcCarrierImage.getPixelAccess()
        carrierHeight = self.__dcCarrierImage.getPilHeight()
        carrierWidth = self.__dcCarrierImage.getPilWidth()

        #add header information about the data image so we know how much to parse
        totalDataBytes = dcDataImage.getPilWidth() * dcDataImage.getPilHeight() * 3
        cx, cy = self.__addHeaderInformation(totalDataBytes) #adding header will return index to start inputting data at

        dataPixels = dcDataImage.getPixelAccess()
        logger.debug("DataPixel Width: " + str(dcDataImage.getPilWidth()))
        logger.debug("DataPixel Height: " + str(dcDataImage.getPilHeight()))
        for dy in range(0, dcDataImage.getPilHeight()):
            for dx in range(0, dcDataImage.getPilWidth()):

                logger.debug("Data Y Index: " + str(dy) + " Data X Index: " + str(dx))

                dataPixel = dataPixels[dx, dy]
                dred, dgreen, dblue = dataPixel
                pixelList = [dred, dgreen,dblue]

                for index, plane in enumerate(pixelList):

                    carrierpixel1 = carrierPixels[cx, cy]
                    carrierpixel2 = None
                    carrierpixel3 = None

                    yInclusiveUntil = cy # used for debug logging
                    if (cx + 1) >= carrierWidth:
                        carrierpixel2 = carrierPixels[0, cy + 1]
                        yInclusiveUntil = cy + 1
                    else:
                        carrierpixel2 = carrierPixels[cx + 1, cy]

                    if (cx + 2) >= carrierWidth:
                        carrierpixel3 = carrierPixels[1, cy + 1]
                        yInclusiveUntil = cy + 1
                    else:
                        carrierpixel3 = carrierPixels[cx + 2, cy]

                    logger.debug("Hiding Data In Carrier X Index: " + str(cx) + " Inclusively To: " + str(cx + 2))
                    logger.debug("Hiding Data In Carrier Y Index: " + str(cy) + " Inclusively To: " + str(yInclusiveUntil))

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
                    else:
                        cx = cx + 3

    def parseDataPixelImage(self):

        carrierPixels = self.__dcCarrierImage.getPixelAccess()
        carrierHeight = self.__dcCarrierImage.getPilHeight()
        carrierWidth = self.__dcCarrierImage.getPilWidth()
        cx, cy, totalDataPixels = self.__getHeaderInformation()

        logger.info("The Total Pixels In The Data Image Is: " + str(totalDataPixels) + "(" + str(totalDataPixels*3)
            + " Bytes Of Data)")
        logger.debug("Data Image Starts At X: " + str(cx) + ", Y: " + str(cy))


    def getCarrierImage(self):
        return self.__dcCarrierImage.getPilImage()
