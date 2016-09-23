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

        logger.info("Carrier Max Byte Storage: " + str(maxBytes) + " Data Image Total Bytes: " + str(dTotalBytes))

        if maxBytes < dTotalBytes:
            logger.error("The Carrier Image Is Too Small. Can't Stego Data Image Into The Carrier")
            return False

        logger.info("Carrier Image Is Large Enough To Fit The Data")
        return True

    @staticmethod
    def calculateMaxStorageCapacity(carrierImg):
        cwidth, cheight = carrierImg.size
        totalPixels = cwidth * cheight
        totalCarrierBytes = totalPixels * 3 # 3 bands for RGB

        maxDataBytes = math.floor(totalCarrierBytes / 9)  # as 9 bytes of carrier image is needed for 1 byte of data image

        # find how many bits are needed to represent this total
        bitsToRepresentMaxDataBytes = math.ceil(math.log2(maxDataBytes))

        # now from this max subtract header data space needed
        maxDataBytes = maxDataBytes - math.ceil((bitsToRepresentMaxDataBytes / 8)) # this calculation should always come out rounded

        return (maxDataBytes, bitsToRepresentMaxDataBytes)