import logging

logger = logging.getLogger("stego")

class DCStego:

    __dcCarrierImage = None

    def __init__(self, dcCarrierImage):
        self.__dcCarrierImage = dcCarrierImage

    def addDataPixelImage(self, dcDataImage):

        cx = 0
        cy = 0
        carrierPixels = self.__dcCarrierImage.getPixelAccess()
        carrierHeight = self.__dcCarrierImage.getPilHeight()
        carrierWidth = self.__dcCarrierImage.getPilWidth()

        dataPixels = dcDataImage.getPixelAccess()
        for dy in range(dcDataImage.getPilWidth()):
            for dx in range(dcDataImage.getPilHeight()):

                dataPixel = dataPixels[dx, dy]
                dred, dgreen, dblue = dataPixel
                pixelList = [dred, dgreen,dblue]

                for plane in pixelList:
                    bplan = bin(plane)

                    # if we've gone over the edge we need to increment and wrap around
                    if cx >= carrierWidth:
                        cx = 0
                        cy = cy + 1

                    carrierpixel1 = carrierPixels[cx, cy]
                    carrierpixel2 = None
                    carrierpixel3 = None

                    if (cx + 1) >= carrierWidth:
                        carrierpixel2 = carrierPixels[0, cy + 1]
                    else:
                        carrierpixel2 = carrierPixels[cx + 1, cy]

                    if (cx + 2) >= carrierWidth:
                        carrierpixel3 = carrierPixels[0, cy + 1]
                    else:
                        carrierpixel3 = carrierPixels[cx + 2, cy]


                    # we now have all the pixels in the carrier to put our data pixel into











                # add back the pixels after had their bits updated


                # now increment our position in the carrier image for the next loop
                cx = cx + 9



'''
        for y in range(self.__dcCarrierImage.getPilWidth()):
            for x in range(self.__dcCarrierImage.getPilHeight()):
                tuple = carrierPixels[x,y]
                print(tuple)
'''






    def parseDataPixelImage(self):
        print ("Nothing Happen s Here Yet!")

    def getCarrierImage(self):
        return self.__dcCarrierImage.getPilImage()



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
