import logging
import sys

from src.dcimage import DCImage
from src.dcstego import DCStego
from src.utils.argparcer import ArgParcer

# Setup Logging
logger = logging.getLogger("stego")
logger.setLevel(logging.DEBUG)
#console logging channel
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s(%(levelname)s) - %(message)s', "%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)


# Parse Command Arguments
mode = ArgParcer.getValue(sys.argv, "-m") # mode can be either 'stego' or 'unstego'
carrierImgDir = ArgParcer.getValue(sys.argv, "-c") # dir path to the carrier image
dataImgDir = ArgParcer.getValue(sys.argv, "-d") # dir path to the data image - this image will be hidden into the carrier

if ArgParcer.keyExists(sys.argv, "--DEBUG"):
    ch.setLevel(logging.DEBUG)

if mode == 'stego':

    fh = logging.FileHandler("stego.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("Stego Mode Selected. Checking Images")
    dataImage = DCImage(dataImgDir)
    carrierImage = DCImage(carrierImgDir)

    if carrierImage.canHoldImage(dataImage) == False:
        logger.error("Stego - Image Sizes Are Not Compatable. Can't Stego The Data Image Into The Carrier. Aborting\n")
        exit(0)

    logger.info("Parsing Data Image Into The Carrier...")
    dcStegoManager = DCStego(carrierImage)
    dcStegoManager.addDataPixelImage(dataImage)

    logger.info("Parsing Complete. Exporting...")
    dcStegoImage = dcStegoManager.getCarrierImage()
    dcStegoImage.getPilImage().save(dcStegoImage.getImageName())

elif mode == 'unstego':

    fh = logging.FileHandler("unstego.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("UnStego Mode Selected. Fetching Images")
    carrierImage = DCImage(carrierImgDir)

    dcStegoManager = DCStego(carrierImage)
    dcDataImage = dcStegoManager.parseDataPixelImage()

    image = dcDataImage.getPilImage()
    image.save(dcDataImage.getImageName())

else:
    logger.error("Stego - No Valid Option Selected. Please Try Again")
    exit(0)

logger.info("Process Complete")




