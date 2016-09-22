import logging

logger = logging.getLogger("stego")


class DCUtils:
    @staticmethod
    def isLargeEnoughImg(carrierImg, dataImg):
        cwidth, cheight = carrierImg.size
        cTotalPixels = cwidth * cheight

        dwidth, dheight = dataImg.size
        dTotalPixels = dwidth * dheight
        dTotalData = dTotalPixels * 3  # assuming 3 plains in RGB

        logger.info("Carrier Total Pixels: " + str(cTotalPixels) + " Data Image Total Pixels (Across All 3 Plains)"
                     + ": " + str(dTotalData))

        if cTotalPixels < dTotalData:
            logger.error("The Carrier Image Is Too Small. Can't Stego Data Image Into The Carrier")
            return False

        logger.info("Carrier Image Is Large Enough To Fit The Data")
        return True
