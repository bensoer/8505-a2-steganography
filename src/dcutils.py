import logging
import math

logger = logging.getLogger("stego")


class DCUtils:
    @staticmethod
    def isLargeEnoughImg(carrierImg, dataImg):

        maxBytes, bitsNeeded = DCUtils.calculateMaxStorageCapacity(carrierImg)

        dwidth, dheight = dataImg.size
        dTotalPixels = dwidth * dheight
        dTotalBytes = dTotalPixels * 3  # assuming 3 plains in RGB

        logger.info("Carrier Max Byte Storage: " + str(maxBytes) + ". Data Image Total Bytes: " + str(dTotalBytes))

        if maxBytes < dTotalBytes:
            logger.error("The Carrier Image Is Too Small. Can't Stego Data Image Into The Carrier")
            return False

        logger.info("Carrier Image Is Large Enough To Fit The Data")
        return True

    @staticmethod
    def calculateMaxStorageCapacity(carrierImg):
        '''
        calculateMaxStorageCapacity Detemines the maximum amount of data that can be stored in the passed in carrier
        image. This calculation includes leaving enough space for the header data needed for the size of data image
        that could be stored within the image. All calculations use cautious metrics so as to allow extra room for
        the header
        :param carrierImg: DCImage - A wrapper of the Pillow Image object representing an image file
        :return: Tuple(int, int) - The tuple's first value contains the maxDataBytes that can be stored in the carrier
        image, leaving enough room for the required header. The tuple's second value is then how many bits will be
        needed in the header in order to store the max data bytes value. Note that cautious calculations means the bits
        needed may be equal to or greater the the space needed to represent the max data byte value. So

                maxDataBytes <= 2 ^ bitsNeededToRepresentMaxDataBytes

                where:
                Tuple(maxDataBytes, bitsNeededToRepresentMaxDataBytes)
        '''

        cwidth, cheight = carrierImg.size
        totalPixels = cwidth * cheight
        totalCarrierBytes = totalPixels * 3 # 3 bands for RGB

        maxDataBytes = math.floor(totalCarrierBytes / 9)  # as 9 bytes of carrier image is needed for 1 byte of data image

        # find how many bits are needed to represent this total
        bitsToRepresentMaxDataBytes = math.ceil(math.log2(maxDataBytes))

        # round this up to the highest number of pixels this will need
        pixelsNeedToRepresentMaxDataBytes = math.ceil(bitsToRepresentMaxDataBytes / 3)
        # recalculate bits as we may have rounded up
        bitsToRepresentMaxDataBytes = pixelsNeedToRepresentMaxDataBytes * 3

        # now from this max subtract header data space needed
        maxDataBytes = maxDataBytes - math.ceil((bitsToRepresentMaxDataBytes / 8)) # round up so that more is taken for header

        maxTotalWidthOrHeightPixels, bitsToRepresentMaxHeightOrWidthPixels = DCUtils.calculateMaxWidthAndHeight(
            maxDataBytes)

        bytesToRepresentMaxHeightOrWidthPixels = math.ceil(bitsToRepresentMaxHeightOrWidthPixels / 8)
        maxDataBytes = maxDataBytes - (bytesToRepresentMaxHeightOrWidthPixels * 2) # *2 for storing both width and height parameters

        maxDataBytes = maxDataBytes - 30 # 30 bytes for 30 character max for data file names

        return (maxDataBytes, bitsToRepresentMaxDataBytes)

    @staticmethod
    def calculateMaxWidthAndHeight(maxDataBytes):

        maxTotalWidthOrHeightPixels = math.ceil(maxDataBytes / 3)

        bitToRepresentMaxHeightOrWidth = math.ceil(math.log2(maxTotalWidthOrHeightPixels))

        return (maxTotalWidthOrHeightPixels, bitToRepresentMaxHeightOrWidth)