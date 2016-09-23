import logging
import sys

from PIL import Image

from src.dcimage import DCImage
from src.dcstego import DCStego
from src.utils.argparcer import ArgParcer

# Setup Logging
logger = logging.getLogger("stego")
logger.setLevel(logging.DEBUG)
#console logging channel
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s(%(levelname)s) - %(message)s', "%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

# Parse Command Arguments
mode = ArgParcer.getValue(sys.argv, "-m") # mode can be either 'stego' or 'unstego'
carrierImgDir = ArgParcer.getValue(sys.argv, "-c") # dir path to the carrier image
dataImgDir = ArgParcer.getValue(sys.argv, "-d") # dir path to the data image - this image will be hidden into the carrier

if mode == 'stego':

    dataImage = DCImage(dataImgDir)
    carrierImage = DCImage(carrierImgDir)

    if carrierImage.canHoldImage(dataImage) == False:
        logger.error("Stego - Image Sizes Are Not Compatable. Can't Stego The Data Image Into The Carrier. Aborting\n")
        exit(0)

    dcStegoManager = DCStego(carrierImage)
    dcStegoManager.addDataPixelImage(dataImage)

    stegoImage = dcStegoManager.getCarrierImage()
    stegoImage.save("../imgs/stego.gif")

elif mode == 'unstego':
    print("Nothing Set Here!")
else:
    logger.error("Stego - No Valid Option Selected. Please Try Again")
    exit(0)

#Start Parsing Images




