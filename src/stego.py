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
    stegoImage = dcStegoManager.getCarrierImage()
    stegoImage.save("../imgs/stego.png")

elif mode == 'unstego':

    logger.info("UnStego Mode Selected. Fetching Images")
    carrierImage = DCImage(carrierImgDir)

    dcStegoManager = DCStego(carrierImage)
    dcStegoManager.parseDataPixelImage()

else:
    logger.error("Stego - No Valid Option Selected. Please Try Again")
    exit(0)

logger.info("Process Complete")




