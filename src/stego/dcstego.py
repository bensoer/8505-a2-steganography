import logging

from PIL import Image, ImageMath

from src.stego.dcutils import DCUtils
from src.utils.argparcer import ArgParcer
import os, sys

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


#Start Parsing Images

dataImage = Image.open(r"/mnt/DATA/PROJECTS/PycharmProjects/8505-a2-steganography/imgs/strawberry.gif")
carrierImage = Image.open(r"/mnt/DATA/PROJECTS/PycharmProjects/8505-a2-steganography/imgs/rockets.gif")
dataImage = dataImage.resize(carrierImage.size)

dataImage = dataImage.convert("RGB")
carrierImage = carrierImage.convert("RGB")

if DCUtils.isLargeEnoughImg(carrierImage, dataImage) == False:
    print("Stego - Image Sizes Are Not Compatable. Can't Stego The Data Image Into The Carrier\n")


dataImagePxAcs = dataImage.load()
carrierImagePxAcs = carrierImage.load()




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
