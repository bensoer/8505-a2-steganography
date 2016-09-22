import logging

from PIL import Image, ImageMath

logger = logging.getLogger("unstego")
logger.setLevel(logging.DEBUG)
#console logging channel
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s(%(levelname)s) - %(message)s', "%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)


logger.info("Initializing")

stegoImage = Image.open(r"../../imgs/stego.jpg")
red, green, blue = stegoImage.split()

dred = ImageMath.eval("(a&0x1)*255",a=red)
#dgreen = ImageMath.eval("(a&0x1)*255",a=green)
#dblue = ImageMath.eval("(a&0x1)*255",a=blue)

dred = dred.convert("L")
#dgreen = dgreen.convert("L")
#dblue = dblue.convert("L")

#out = Image.merge("RGB", ( dred, dgreen, dblue))
#out.save(r"../../imgs/unstego.jpg")

dred.save(r"../../imgs/unstego.jpg")