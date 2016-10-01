import logging
import sys

from dcimage import DCImage
from dcstego import DCStego
from utils.argparcer import ArgParcer

# Setup Logging
logger = logging.getLogger("stego")
logger.setLevel(logging.DEBUG)
#console logging channel
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s(%(levelname)s) - %(message)s', "%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)


def printHelp():
    '''
    printHelp is a helper method that simply prints out information on how to use the stego program and all of its flags
    and options
    :return:
    '''
    logger.info("Image Steganography Program By Ben Soer")
    logger.info("-------------------------------")
    logger.info("Usage:")
    logger.info("       python3 src/stego.py -m <mode> -c <carrierimg> [-d <dataimg>] [-o <outputimg>] [-e <encryptionoffset>]")
    logger.info ("Flags:")
    logger.info("       -m      Mode. Can either be 'stego' or 'unstego'. 'stego' is for merging images. 'unstego' is for parsing out images")
    logger.info("       -c      Carrier Image. Dir To The Carrier Image")
    logger.info("       -d      Data Image. Dir To The Data Image")
    logger.info("       -o      Output Image. Dir And Name For The Output Image. Only valid in 'stego' mode")
    logger.info("       -e      Encryption Offset. Integer offset for encryption data image. Offset in 'unstego' mode must match that of offset during 'stego' mode")
    logger.info("-------------------------------")

if len(sys.argv) <= 2 or ArgParcer.keyExists(sys.argv,"--HELP"):
    printHelp()
    exit(0)

# Parse Command Arguments
mode = ArgParcer.getValue(sys.argv, "-m") # mode can be either 'stego' or 'unstego'
carrierImgDir = ArgParcer.getValue(sys.argv, "-c") # dir path to the carrier image
dataImgDir = ArgParcer.getValue(sys.argv, "-d") # dir path to the data image - this image will be hidden into the carrier
outputFileName = ArgParcer.getValue(sys.argv, "-o")
encryptionOffset = 0
try:
    encryptionOffset = int(ArgParcer.getValue(sys.argv, "-e"))
except:
    encryptionOffset = 0


if ArgParcer.keyExists(sys.argv, "--DEBUG"):
    ch.setLevel(logging.DEBUG)

if mode == 'stego':

    fh = logging.FileHandler("stego.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("Stego Mode Selected. Checking Images")
    dataImage = DCImage(dataImgDir)
    #dataImage.encryptImage()
    carrierImage = DCImage(carrierImgDir)

    if carrierImage.canHoldImage(dataImage) == False:
        logger.error("Stego - Image Sizes Are Not Compatable. Can't Stego The Data Image Into The Carrier. Aborting\n")
        exit(0)

    if dataImage.getImageNameLength() > 30:
        logger.error("Stego. The Name Of The Data Image (Including Extension) Is Longer Then 30 Characters. Please "
            + "rename the file to contain less then 30 characters")
        exit(0)

    logger.info("Parsing Data Image Into The Carrier...")
    dcStegoManager = DCStego(carrierImage, encryptionOffset)
    dcStegoManager.addDataPixelImage(dataImage)

    logger.info("Parsing Complete. Exporting...")
    dcStegoImage = dcStegoManager.getCarrierImage()

    if outputFileName == "":
        dcStegoImage.getPilImage().save(dcStegoImage.getImageName())
    else:
        dcStegoImage.getPilImage().save(outputFileName)

    dcStegoImage.getPilImage().close()
    dataImage.getPilImage().close()
    carrierImage.getPilImage().close()

elif mode == 'unstego':

    fh = logging.FileHandler("unstego.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info("UnStego Mode Selected. Fetching Images")
    carrierImage = DCImage(carrierImgDir)

    dcStegoManager = DCStego(carrierImage, encryptionOffset)
    dcDataImage = dcStegoManager.parseDataPixelImage()
    #dcDataImage.decryptImage()

    image = dcDataImage.getPilImage()
    image.save(dcDataImage.getImageName())
    image.close()

    carrierImage.getPilImage().close()

else:
    logger.error("Stego - No Valid Option Selected. Please Try Again")
    exit(0)

logger.info("Process Complete")




