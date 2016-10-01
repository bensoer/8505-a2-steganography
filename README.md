#8505-a2-steganography
8505-a2-steganography is an assignment program that demonstrates how simple
steganography works by storing a single image into another. The program
also uses a simple CaesarCipher which can be set as a command argument
to add additional security to the stego procedure

8505-a2-steganography uses the Pillow library to parse and manipulate
the images it uses. Unfortunatly this library is extremely slow when
accessing images via pixel values. Thus the program can take 1-2 minutes
depending on the size of the image, to parse or encode and image to or
from its carrier

Note: This product can be used to cause harm if used inappropriately, it
has been created strictly for educational purposes and is intended only
to be used as such

#Setup

##Prerequisits
The program requires `python3` to operate

##Installation
1. Clone the repo. cd into the root of the project
2. Execute pip3 install Pillow

#Usage

Execute the program with the following commands from the project root:
```
python3 src/stego.py -m <mode> -c <carrierimg> [-d <dataimg>] [-o <outputimg>] [-e <encryptionoffset>]
```

| Flag | Definition | Usage |
|------|------------|-------|
| -m | Specifies the mode | Valid values are either `stego` or `unstego` |
| -c | Dir to the Carrier Image | "./dir/to/img.png" |
| -d | Dir to the Data Image. Only valid in `stego` mode | "./dir/to/img.png" |
| -o | Dir/Name of output image. Only valid in `stego` mode | "./dir/to/stego/output.png" |
| -e | Offset for CaesarCipher | Integer value from 0 - Infinity |

For quick help, execute the program with no parameters of the `--HELP` flag

For developer output, exeucte the program with the `--DEBUG` flag. This
will cause verbose output to be dumped to the console. Note this will
dramaticaly slow down processing. Alternatively without the `--DEBUG` flag
all data is written to a log file instead of the console



#Developer Resources:

###Samples:
https://stevendkay.wordpress.com/2009/10/07/image-steganography-with-pil/
https://saxenarajat99.wordpress.com/2014/01/17/hiding-image-in-image-in-python-using-steganography/
###Get Pixels:
http://pillow.readthedocs.io/en/3.3.x/reference/PixelAccess.html?highlight=band
http://pillow.readthedocs.io/en/3.3.x/reference/PixelAccess.html?highlight=Pixel
###Bytes Conversion:
http://pillow.readthedocs.io/en/3.3.x/reference/Image.html?highlight=tobytes
###Logging Cookbook:
https://docs.python.org/3/howto/logging-cookbook.html