#!/usr/bin/env python

""" 

A simple utility to generate private chat avatars from two given images.

Usage: python mergeavatars.py firstavatar secondavatar folder

firstavatar, secondavatar: images of the avatars to combine. Must be in a graphical format 
supported by imagemagick

folder: the resulting folder where the result would be put. 

"""

__author__ = "Andrew Nenakhov"
__copyright__ = "Copyright 2020, redsolution OÜ"
__credits__ = ["Andrew Nenakhov"]
__license__ = "GNU AGPLv3"
__version__ = "0.1"
__maintainer__ = "Andrew Nenakhov"
__email__ = "andrew.nenakhov@redsolution.com"
__status__ = "Development"

import os
import sys
import json
import base64
import random
import string

from hashlib import sha1
from wand.image import Image
#from wand.drawing import Drawing
#from wand.color import Color

def hex_to_rgb(value):
    """ converts hex color value to nice tuple of R, G and B integer components """

    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def mergeAvatars( avatarLeft, avatarRight, folder ):
    """ Just as expected, this function gets two images and merges them into a private chat avatar """

    #with Image( filename = "results/" + avatarRight ) as compositeImage:
    with Image(width=128, height=128, background = "#F0F0F0") as compositeImage:

        try:
            with Image( filename = avatarLeft) as leftImage:

                #cropping image if it is not square
                leftImage.transform(resize='128x128^')

                sizeX, sizeY = leftImage.size

                deltaX = int( (sizeX - 128) / 2 )
                deltaY = int( (sizeY - 128) / 2 )


                with leftImage[ (deltaX+16):(deltaX+80), (deltaY):(deltaY+128) ] as cropped:
                    compositeImage.composite(cropped, left = 0, top = 0 )
        except:
            #raise Exception("first avatar can't be opened")
            sys.exit("First avatar file " + avatarLeft + " can't be opened or is not an image.")

        try:
            with Image( filename =  avatarRight) as rightImage:

                #cropping image if it is not square
                rightImage.transform(resize='128x128^')

                sizeX, sizeY = rightImage.size

                deltaX = int( (sizeX - 128) / 2 )
                deltaY = int( (sizeY - 128) / 2 )            

                with rightImage[(deltaX+48):(deltaX+112), (deltaY):(deltaY+128)] as cropped2:
                    compositeImage.composite(cropped2, left = 64, top = 0 )
        except:
            #raise Exception("second  avatar can't be opened")
            sys.exit("Second avatar file " + avatarRight + "  can't be opened or is not an image.")

        #check if destination folder exists, trying to create it
        if not os.path.exists( folder ):
            try:  
                os.mkdir( folder )  
            except OSError as error:  
                #raise Exception( "Failed to create specified folder" )
                sys.exit(error)

        #else:
        #    print ("All ok, proceeding")


        #save temporary file to specified folder 

        temporaryFile = folder + "/" + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10)) + ".png"
        compositeImage.save( filename = temporaryFile )

        #get sha1 hash of temporary file
        imageHash = sha1( open( temporaryFile, 'rb').read()).hexdigest() + ".png"

        resultFile = folder + "/" + imageHash

        #rename temporary file
        os.rename(temporaryFile, resultFile )

        #write filename to stdout
        sys.stdout.write( imageHash + "\n") 


# checking for a valid number of arguments

if len(sys.argv) > 1:
    if (sys.argv[1] == "help") | (sys.argv[1] == "-h") | (sys.argv[1] == "-help") | (sys.argv[1] == "--help") :
        sys.exit("usage: python mergeavatars.py firstavatar secondavatar folder")

if len(sys.argv)!=4:
    sys.exit("you should supply exactly four arguments" )

mergeAvatars( sys.argv[1], sys.argv[2], sys.argv[3] )




















