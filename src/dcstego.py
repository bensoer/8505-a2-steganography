import logging
import math
from dcutils import DCUtils
from dcimage import DCImage

logger = logging.getLogger("stego")

class DCStego:

    __dcCarrierImage = None
    __encryptionOffset = 0

    def __init__(self, dcCarrierImage, encryptionOffset = 0):
        self.__dcCarrierImage = dcCarrierImage
        self.__encryptionOffset = encryptionOffset

    def __getHeaderInformation(self):
        '''
        getHeaderInformation is a private helper method that parses out the required header tag placed at the
        beginning of the stego carrier image. This header contains the size, height, widht and name information of
        the data image that is being stored in the carreir
        :return: Tuple<Int,Int,Int,Int,Int,String>
        '''

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

        totalDataBytes = 0

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
                    totalDataBytes <<= 1

                    lsb = (plane & 1)

                    logger.debug("BEFORE: Plane: " + str(plane) + " As Binary: " + bin(plane) + " LSB Of Data: " + str(lsb))
                    binaryBeforeProcessing += str(lsb)  # were reading MSB -> LSB so should append to the end
                    if lsb == 1:
                        totalDataBytes |= 1
                    else:
                        totalDataBytes &= ~1

                    logger.debug("Running Binary: " + bin(totalDataBytes))
                    logger.debug("Running Value: " + str(totalDataBytes))

        logger.debug("Binary Of TotalDataBytes: " + bin(totalDataBytes))
        logger.debug("Binary Before Processing: " + binaryBeforeProcessing)

        # ---- DECODING WIDTH PIXELS ----

        maxWidthPixels, bitsNeededToRepresentWidth = DCUtils.calculateMaxWidthAndHeight(maxBytes)
        pixelsNeeded = math.ceil(bitsNeededToRepresentWidth / 3)  # rounding up to the nearest pixel

        wx = ex + pixelsNeeded  # minus 1 to get the index
        wy = ey

        while wx >= carrierWidth:
            wx = abs(wx - carrierWidth)
            wy = wy + 1

        totalDataWidth = 0

        binaryBeforeProcessing = ""
        # now loop forward through the carrier from 0 to the end ex and ey pixels
        for cy in range(ey, wy + 1):
            for cx in range(ex, wx + 1):
                logger.debug("Pixel Index: X: " + str(cx) + " Y: " + str(cy))
                carrierPixel = carrierPixels[cx, cy]
                cred, cgreen, cblue = carrierPixel
                pixelList = [cred, cgreen, cblue]  # put them in forward order
                logger.debug("Initial Value: " + str(pixelList))

                for plane in pixelList:
                    totalDataWidth <<= 1
                    lsb = (plane & 1)

                    logger.debug(
                        "BEFORE: Plane: " + str(plane) + " As Binary: " + bin(plane) + " LSB Of Data: " + str(lsb))
                    binaryBeforeProcessing += str(lsb)  # were reading MSB -> LSB so should append to the end
                    if lsb == 1:
                        totalDataWidth |= 1
                    else:
                        totalDataWidth &= ~1

                    logger.debug("Running Binary: " + bin(totalDataWidth))
                    logger.debug("Running Value: " + str(totalDataWidth))

        logger.debug("Binary Of TotalDataWidth: " + bin(totalDataWidth))
        logger.debug("Binary Before Processing: " + binaryBeforeProcessing)

        # ---- DECODING HEIGHT PIXELS ----

        maxHeightPixels, bitsNeededToRepresentHeight = DCUtils.calculateMaxWidthAndHeight(maxBytes)
        pixelsNeeded = math.ceil(bitsNeededToRepresentHeight / 3)  # rounding up to the nearest pixel

        hx = wx + pixelsNeeded  # minus 1 to get the index
        hy = wy

        while hx >= carrierWidth:
            hx = abs(hx - carrierWidth)
            hy = hy + 1

        totalDataHeight = 0

        binaryBeforeProcessing = ""
        # now loop forward through the carrier from 0 to the end ex and ey pixels
        for cy in range(wy, hy + 1):
            for cx in range(wx, hx + 1):
                logger.debug("Pixel Index: X: " + str(cx) + " Y: " + str(cy))
                carrierPixel = carrierPixels[cx, cy]
                cred, cgreen, cblue = carrierPixel
                pixelList = [cred, cgreen, cblue]  # put them in forward order
                logger.debug("Initial Value: " + str(pixelList))

                for plane in pixelList:
                    totalDataHeight <<= 1
                    lsb = (plane & 1)

                    logger.debug(
                        "BEFORE: Plane: " + str(plane) + " As Binary: " + bin(plane) + " LSB Of Data: " + str(lsb))
                    binaryBeforeProcessing += str(lsb)  # were reading MSB -> LSB so should append to the end
                    if lsb == 1:
                        totalDataHeight |= 1
                    else:
                        totalDataHeight &= ~1

                    logger.debug("Running Binary: " + bin(totalDataHeight))
                    logger.debug("Running Value: " + str(totalDataHeight))

        logger.debug("Binary Of TotalDataHeight: " + bin(totalDataHeight))
        logger.debug("Binary Before Processing: " + binaryBeforeProcessing)

        # ---- DECODING FILENAME ----

        # make sure its always 30 characters without spaces
        # = 240 bits
        # = 80 carrier pixels
        fileName = ""

        nx = hx + 1
        ny = hy

        while nx >= carrierWidth:
            nx = abs(nx - carrierWidth)
            ny = ny + 1

        offsetInPixel = 0

        for byte in range(0,30):
            fileNameByte = 0
            for i in range(0, 7):

                fileNameByte <<= 1

                carrierPixel = carrierPixels[nx, ny]
                cred, cgreen, cblue = carrierPixel
                pixelList = [cred, cgreen, cblue]

                plane = pixelList[offsetInPixel]
                lsb = (plane & 1)

                logger.debug("Parsing MSB Of: " + str(lsb) + " At Index: X: " + str(nx) + " Y: " + str(ny) + " Offset: " + str(offsetInPixel))

                if lsb == 1:
                    fileNameByte |= 1
                else:
                    fileNameByte &= ~1

                logger.debug("Created Number Of: " + str(fileNameByte) + " ( Binary: " + bin(fileNameByte) + " )")

                offsetInPixel = offsetInPixel + 1
                if offsetInPixel == 3:
                    nx = nx + 1
                    offsetInPixel = 0

                if nx >= carrierWidth:
                    nx = 0
                    ny = ny + 1

            logger.debug("Parsing Found Number Of: " + str(fileNameByte))
            logger.debug("Parsing Found Number In Binary As: " + bin(fileNameByte))
            logger.debug("Parsing Name Found Letter: " + chr(fileNameByte))
            fileName += chr(fileNameByte)
            logger.debug("Total FileName As This Point Is: >" + fileName + "<")

        fileName = fileName.replace(" ", "")
        logger.debug("FileName After Cleaning: >" + fileName + "<")

        # check if ex +1 is too far
        if (nx + 1) > carrierWidth:
            nx = 0
            ny = ny +1
        else:
            nx = nx + 1

        return (nx, ny, totalDataBytes, totalDataWidth, totalDataHeight, fileName)

    def __addHeaderInformation(self, totalDataBytes, totalWidthPixels, totalHeightPixels, fileName):
        '''
        addHeaderInformation is a private helper method that places a header into the carrier image so that the data
        image can be retrieved by the program when it is parsed out. The header contains the total size, width, height
        and name of the data file being stored in the carrier
        :param totalDataBytes: Int - Number of total bytes which makes up the data image
        :param totalWidthPixels: Int - Total number of pixels that make up the width of the image
        :param totalHeightPixels: Int - Total number of pixels that make up the height of the image
        :param fileName: String - The name of the data image file including extension
        :return: Tuple<int,int> - The X, and Y coordinated of where to start adding the image data into the carreir
        '''

        logger.debug(" -- PROCESING HEADER INFORMATION INTO CARRIER -- ")
        logger.debug("Total Bytes In Data Image Is: " + str(totalDataBytes) + ". This Number Will Be Placed Into The"
            + " Header")
        logger.debug("In Binary That Is: " + bin(totalDataBytes))

        # ---- ENCODE MAX BYTES ----

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

        logger.debug("Binary Before Processing: " + binaryBeforeProcessing)
        logger.debug("Binary After Processing: " + binaryAfterProcessing)

        # ---- ENCODE WIDTH PIXELS ----

        # move bitsNeedToRepresentWidth in to store width in reverse
        maxWidthPixels, bitsNeededToRepresentWidth = DCUtils.calculateMaxWidthAndHeight(maxBytes)
        pixelsNeeded = math.ceil(bitsNeededToRepresentWidth / 3)

        logger.debug("Total Data Width Is: " + str(totalWidthPixels))
        logger.debug("In Binary That Is: " + bin(totalWidthPixels))
        logger.debug("Allocation Gives A Max Of: " + str(bitsNeededToRepresentWidth) + " To Store The Width")

        binaryBeforeProcessing = ""
        binaryAfterProcessing = ""

        wx = sx + pixelsNeeded # no need to minus to get the index, sx will be already incremented correctly
        wy = sy
        # wrap around
        while wx >= carrierWidth:
            wx = abs(wx - carrierWidth)
            wy = wy +1

        # now go backwards from wx to sx
        for cy in range(wy, sy - 1, -1):
            for cx in range(wx, sx - 1, -1):
                logger.debug("Pixel Index: X: " + str(cx) + " Y: " + str(cy))
                carrierPixel = carrierPixels[cx, cy]
                cred, cgreen, cblue = carrierPixel
                pixelList = [cblue, cgreen, cred]  # note that this is backwards
                logger.debug("Initial Value: " + str(pixelList))

                for index, plane in enumerate(pixelList):
                    lsb = (totalWidthPixels & 1)

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
                    totalWidthPixels >>= 1
                    # this will automaticaly zero out and pad until we fill the designated space

                logger.debug("PostProcessed: In Pixel List: " + str(pixelList))
                carrierPixels[cx, cy] = (pixelList[2], pixelList[1], pixelList[0])

                # print(str(pixelList[2]) + " " + str(pixelList[1]) + " " + str(pixelList[0]))
                # carrierPixels[cx,cy] = (0, 0, 0)
                logger.debug("PostProcessed: In Carrier Pixels: " + str(carrierPixels[cx, cy]))

        logger.debug("Binary Before Processing: " + binaryBeforeProcessing)
        logger.debug("Binary After Processing: " + binaryAfterProcessing)

        # ---- ENCODE HEIGHT PIXELS ----

        # move bitsNeedToRepresentWidth in to store width in reverse
        maxHightPixels, bitsNeededToRepresentHeight = DCUtils.calculateMaxWidthAndHeight(maxBytes)
        pixelsNeeded = math.ceil(bitsNeededToRepresentHeight / 3)

        logger.debug("Total Data Height Is: " + str(totalWidthPixels))
        logger.debug("In Binary That Is: " + bin(totalWidthPixels))
        logger.debug("Allocation Gives A Max Of: " + str(bitsNeededToRepresentWidth) + " To Store The Width")

        binaryBeforeProcessing = ""
        binaryAfterProcessing = ""

        hx = wx + pixelsNeeded  # no need to minus to get the index, sx will be already incremented correctly
        hy = wy
        # wrap around
        while hx >= carrierWidth:
            hx = abs(hx - carrierWidth)
            hy = hy +1

        # now go backwards from wx to sx
        for cy in range(hy, wy - 1, -1):
            for cx in range(hx, wx - 1, -1):
                logger.debug("Pixel Index: X: " + str(cx) + " Y: " + str(cy))
                carrierPixel = carrierPixels[cx, cy]
                cred, cgreen, cblue = carrierPixel
                pixelList = [cblue, cgreen, cred]  # note that this is backwards
                logger.debug("Initial Value: " + str(pixelList))

                for index, plane in enumerate(pixelList):
                    lsb = (totalHeightPixels & 1)

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
                    totalHeightPixels >>= 1
                    # this will automaticaly zero out and pad until we fill the designated space

                logger.debug("PostProcessed: In Pixel List: " + str(pixelList))
                carrierPixels[cx, cy] = (pixelList[2], pixelList[1], pixelList[0])

                # print(str(pixelList[2]) + " " + str(pixelList[1]) + " " + str(pixelList[0]))
                # carrierPixels[cx,cy] = (0, 0, 0)
                logger.debug("PostProcessed: In Carrier Pixels: " + str(carrierPixels[cx, cy]))

        logger.debug("Binary Before Processing: " + binaryBeforeProcessing)
        logger.debug("Binary After Processing: " + binaryAfterProcessing)

        # ---- ENCODE FILENAME ----

        # make sure its always 30 characters without spaces
        # = 240 bits
        # = 80 carrier pixels
        fileName = fileName.replace(" ", "")
        while len(fileName) < 30:
            fileName += " "

        #fileNameBytes = fileName.encode()
        nx = hx + 1
        ny = hy

        while nx >= carrierWidth:
            nx = abs(nx - carrierWidth)
            ny = ny + 1

        offsetInPixel = 0

        for letter in fileName:
            logger.debug("Processing Letter: " + letter)
            logger.debug("As ASCII That Is Number: " + str(ord(letter)))
            logger.debug("As Binary The Number IS: " + bin(ord(letter)))

            ordinal = ord(letter)

            for i in range(6,-1, -1):
                msb = (ordinal >> i) & 1

                logger.debug("Placing MSB Of: " + str(msb) + " At Index: X " + str(nx) + " Y " + str(ny) + " Offset: " + str(offsetInPixel))

                carrierPixel = carrierPixels[nx,ny]
                cred, cgreen, cblue = carrierPixel
                pixelList = [cred,cgreen,cblue]

                plane = pixelList[offsetInPixel]

                if msb == 1:
                    plane |= 1
                else:
                    plane &= ~1

                pixelList[offsetInPixel] = plane
                carrierPixel = (pixelList[0], pixelList[1], pixelList[2])
                carrierPixels[nx,ny] = carrierPixel

                offsetInPixel = offsetInPixel + 1

                if offsetInPixel == 3:
                    nx = nx +1
                    offsetInPixel = 0

                if nx >= carrierWidth:
                    nx = 0
                    ny = ny + 1



        # check if sx +1 is too far
        if (nx + 1) >= carrierWidth:
            nx = 0
            ny = ny + 1
        else:
            nx = nx + 1

        # now return the results, giving the pixel coordinates to the start position of the image data


        logger.debug(" -- END OF PROCESING HEADER INFORMATION INTO CARRIER -- ")
        #logger.setLevel(logging.INFO)

        return (nx, ny)

    def __encryptPixel(self, pixel):
        '''
        encryptPixel is a private helper method that applies a basic caesarcipher to the passed in pixel. This is
        done by taking the RGB value fo the pixel and adding an offset value to the pixel. It is then corrected
        to make sure it falls within the RGB value range of 0 - 255
        :param pixel: Tuple<int,int,int> - Represents a pixel with an int representing the Red, Green, Blue values of an RGB pixel
        :return: Tuple<int,int,int> - The encrypted pixel
        '''
        pred, pgreen, pblue = pixel

        pred = pred + self.__encryptionOffset
        pgreen = pgreen + self.__encryptionOffset
        pblue = pblue + self.__encryptionOffset


        if pred > 255:
            pred = 0 + abs(pred - 256)

        if pgreen > 255:
            pgreen = 0 + abs(pgreen - 256)

        if pblue > 255:
            pblue = 0 + abs(pblue - 256)

        return (pred, pgreen, pblue)

    def __decryptPixel(self, pixel):
        '''
        decryptPixel is a private helper method that applies a basic caesarcipher to the passed in pixel. This is done
        by taking the RB value fo the pixel adn substracting an offset value from the pixe. It is then corrected
        to make sure it falls within the RGB value range of 0 - 255. Assuming the pixel passed in was encrypted
        the original pixel value will then ve successfuly restored
        :param pixel:  Tuple<int,int,int> - Represents a pixel with an int representing the Red, Green, Blue values of
        an RGB pixel
        :return:  Tuple<int,int,int> - The decrypted pixel
        '''
        pred, pgreen, pblue = pixel

        pred = pred - self.__encryptionOffset
        pgreen = pgreen - self.__encryptionOffset
        pblue = pblue - self.__encryptionOffset

        if pred < 0:
            pred = 256 + pred

        if pgreen < 0:
            pgreen = 256 + pgreen

        if pblue < 0:
            pblue = 256 + pblue

        return (pred, pgreen, pblue)

    def addDataPixelImage(self, dcDataImage):
        '''
        addDataPixelImage parses and encodes the passed in data image into the carrier image
        :param dcDataImage: DCImage - A wrapper around an Image object representing a data image to be stored into
        the carrier
        :return:
        '''

        carrierPixels = self.__dcCarrierImage.getPixelAccess()
        carrierHeight = self.__dcCarrierImage.getPilHeight()
        carrierWidth = self.__dcCarrierImage.getPilWidth()

        #add header information about the data image so we know how much to parse
        totalDataBytes = dcDataImage.getPilWidth() * dcDataImage.getPilHeight() * 3
        cx, cy = self.__addHeaderInformation(totalDataBytes, dcDataImage.getPilWidth(), dcDataImage.getPilHeight(), dcDataImage.getImageName()) #adding header will return index to start inputting data at

        dataPixels = dcDataImage.getPixelAccess()
        logger.debug("DataPixel Width: " + str(dcDataImage.getPilWidth()))
        logger.debug("DataPixel Height: " + str(dcDataImage.getPilHeight()))
        logger.debug("Placement of Data Image Starts At Indexes: X: " + str(cx) + " Y: " + str(cy))
        for dy in range(0, dcDataImage.getPilHeight()):
            for dx in range(0, dcDataImage.getPilWidth()):

                logger.debug("Data Y Index: " + str(dy) + " Data X Index: " + str(dx))

                dataPixel = dataPixels[dx, dy]
                logger.debug("Data Pixel Value: " + str(dataPixel) + " at position: X: " + str(dx) + " Y: " + str(dy))
                dataPixel = self.__encryptPixel(dataPixel)
                dred, dgreen, dblue = dataPixel
                pixelList = [dred, dgreen, dblue]

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
                        carrierpixel3 = carrierPixels[abs((cx + 2) - carrierWidth), cy + 1]
                        yInclusiveUntil = cy + 1
                    else:
                        carrierpixel3 = carrierPixels[cx + 2, cy]

                    logger.debug("Hiding Data In Carrier X Index: " + str(cx) + " Inclusively To: " + str(cx + 2))
                    logger.debug("Hiding Data In Carrier Y Index: " + str(cy) + " Inclusively To: " + str(yInclusiveUntil))

                    # we now have all the pixels in the carrier to put our data pixel into
                    r1,g1,b1 = carrierpixel1
                    r2,g2,b2 = carrierpixel2
                    r3,g3,b3 = carrierpixel3

                    carriers = [r1,g1,b1,r2,g2,b2,r3,g3,b3]

                    logger.debug("Putting The Following Plane Into The Carrier: " + str(plane) + ". Binary: "
                        + bin(plane))
                    logger.debug("BEFORE: Carriers In Order To Be Injected: " + str(carriers))

                    for i in range(0,8):
                        lsb = (plane >> i) & 1

                        if lsb == 1:
                            carriers[i] |= 1
                        else:
                            carriers[i] &= ~1

                    logger.debug("AFTER: Carriers In Order To Be Injected: " + str(carriers))

                    #set the planes back to their pixels
                    carrierpixel1 = (carriers[0], carriers[1], carriers[2])
                    carrierpixel2 = (carriers[3], carriers[4], carriers[5])
                    carrierpixel3 = (carriers[6], carriers[7], carriers[8])

                    #set the pixels back to their position in the carrier image array
                    carrierPixels[cx,cy] = carrierpixel1

                    if (cx + 1) >= carrierWidth:
                        carrierPixels[0, cy + 1] = carrierpixel2
                    else:
                        carrierPixels[cx + 1, cy] = carrierpixel2

                    if (cx + 2) >= carrierWidth:
                        carrierPixels[abs((cx + 2) - carrierWidth), cy + 1] = carrierpixel3
                    else:
                        carrierPixels[cx + 2, cy] = carrierpixel3


                    # now increment our position in the carrier image for the next loop
                    if (cx + 3) >= carrierWidth:
                        cy = cy + 1
                        cx = abs(carrierWidth - (cx + 3))
                    else:
                        cx = cx + 3


    def parseDataPixelImage(self):
        '''
        parseDataPixelImage parses a data image out of this image (being the assumed carrier). This is done by first
        pulling out the header information of the image, after which the rest of the image data is parsed out and a
        data image is then generated
        :return: Image - the data image being stored in the carrier
        '''
        carrierPixels = self.__dcCarrierImage.getPixelAccess()
        carrierHeight = self.__dcCarrierImage.getPilHeight()
        carrierWidth = self.__dcCarrierImage.getPilWidth()
        cx, cy, totalDataBytes, totalDataWidth, totalDataHeight, fileName = self.__getHeaderInformation()

        logger.info("The Total Bytes In The Data Image Is: " + str(totalDataBytes))
        logger.info("The Total Width In Pixels of The Data Image Is: " + str(totalDataWidth))
        logger.info("The Total Height In Pixels of The Data Image Is: " + str(totalDataHeight))
        logger.info("The File Name Is: " + fileName)
        logger.debug("Data Image Starts At Index X: " + str(cx) + ", Y: " + str(cy))

        logger.info("Creating Image Placeholder")
        # create a new image
        dataImage = DCImage.createNewImage(totalDataHeight, totalDataWidth, savedir=fileName)
        dataPixels = dataImage.getPixelAccess()

        logger.info("Now Parsing Image...")

        for dy in range(0, totalDataHeight):
            for dx in range(0, totalDataWidth):

                dataPixel = dataPixels[dx, dy]
                dred, dgreen, dblue = dataPixel
                pixelList = [dred, dgreen, dblue]

                for index, plane in enumerate(pixelList):

                    carrierpixel1 = carrierPixels[cx,cy]
                    logger.debug("Carrier Pixel Values: " + str(carrierpixel1) + "At Carrier Index: X: " + str(cx)
                        + " Y: " + str(cy))
                    carrierpixel2 = None
                    carrierpixel3 = None
                    yInclusiveUntil = cy  # used for debug logging

                    if (cx + 1) >= carrierWidth:
                        carrierpixel2 = carrierPixels[0, cy + 1]
                        logger.debug("Carrier Pixel Values: " + str(carrierpixel2) + "At Carrier Index: X: " + str(0)
                                     + " Y: " + str(cy + 1))
                        yInclusiveUntil = cy + 1
                    else:
                        carrierpixel2 = carrierPixels[cx + 1, cy]
                        logger.debug("Carrier Pixel Values: " + str(carrierpixel2) + "At Carrier Index: X: " + str(cx+1)
                                     + " Y: " + str(cy))

                    if (cx + 2) >= carrierWidth:
                        carrierpixel3 = carrierPixels[abs((cx + 2) - carrierWidth), cy + 1]
                        logger.debug("Carrier Pixel Values: " + str(carrierpixel3) + "At Carrier Index: X: " + str(abs((cx + 2) - carrierWidth))
                                     + " Y: " + str(cy+1))
                        yInclusiveUntil = cy + 1
                    else:
                        carrierpixel3 = carrierPixels[cx + 2, cy]
                        logger.debug("Carrier Pixel Values: " + str(carrierpixel3) + "At Carrier Index: X: " + str(cx + 2)
                                     + " Y: " + str(cy))

                    logger.debug("Retrieving Data In Carrier X Index: " + str(cx) + " Inclusively To: " + str(cx + 2))
                    logger.debug("Retrieving Data In Carrier Y Index: " + str(cy) + " Inclusively To: " + str(yInclusiveUntil))

                    r1,g1,b1 = carrierpixel1
                    r2,g2,b2 = carrierpixel2
                    r3,g3,b3 = carrierpixel3

                    carriers = [g3,r3,b2,g2,r2,b1,g1,r1] # reversed to go MSB -> LSB

                    logger.debug("Carriers In Order To Be Parsed: " + str(carriers))

                    dPlaneValue = 0
                    for i in range(0,8):
                        dPlaneValue <<= 1
                        lsb = (carriers[i] & 1)

                        if lsb == 1:
                            dPlaneValue |= 1
                        else:
                            dPlaneValue &= ~1

                    logger.debug("The Plane That Was Parsed and Created: " + str(dPlaneValue) + " Binary: "
                        + bin(dPlaneValue) + ". It Will Go into index: " + str(index))
                    pixelList[index] = dPlaneValue

                    # now increment our position in the carrier image for the next loop
                    if (cx + 3) >= carrierWidth:
                        cy = cy + 1
                        cx = abs(carrierWidth - (cx + 3))
                    else:
                        cx = cx + 3

                # put the planes back into their pixel
                dataPixel = (pixelList[0], pixelList[1], pixelList[2])
                logger.debug("Data Pixel Value: " + str(dataPixel) + " at position: X: " + str(dx) + " Y: " + str(dy))
                dataPixel = self.__decryptPixel(dataPixel)
                # put the pixel back into the image
                dataPixels[dx,dy] = dataPixel



        return dataImage


    def getCarrierImage(self):
        '''
        getCarrierImage fetches the stores carrier image in this class so that it can be saved to the file system
        after it has either had a data image encoded into it or removed from it
        :return: DCImage - A wrapper of an Image object representing an image
        '''
        return self.__dcCarrierImage
