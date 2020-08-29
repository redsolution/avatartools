#!/usr/bin/env python

""" 

A simple utility to generate nicknames and matching avatars in incognito groups.
Usage:

python generateavatar.py folder

folder: a folder to store the generated avatar.

If the randomly generated avatar name/color already used, it returns the name of
the existing file. Future updates may take into account multiple possible background
colors, for now only color + image are considered for uniqueness.

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
#import collections #used only in examineLuminance()

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

backgroundsLight = {
    "red":          "#FFEBEE",
    "pink":         "#FCE4EC",
    "purple":       "#F3E5F5",
    "deeppurple":   "#EDE7F6",
    "indigo":       "#E8EAF6",
    "blue":         "#E3F2FD",
    "lightblue":    "#E1F5FE",
    "cyan":         "#E0F7FA",
    "teal":         "#E0F2F1",
    "green":        "#E8F5E9",
    "lightgreen":   "#F1F8E9",
    "lime":         "#F9FBE7",
    "yellow":       "#FFFDE7",
    "amber":        "#FFF8E1",
    "orange":       "#FFF3E0",
    "brown":        "#FFF3E0",
    "grey":         "#FFF3E0",
    "bluegrey":     "#FFF3E0"
}

backgroundsDark = {
    "red900":        "#b71c1c",
    "pink900":       "#880e4f",
    "purple900":     "#4a148c",
    "deeppurple900": "#311b92",
    "indigo900":     "#1a237e",
    "blue900":       "#0d47a1",
    "lightblue900":  "#01579b",
    "cyan900":       "#006064",
    "teal900":       "#004d40",
    "green900":      "#1b5e20",
    "lightgreen900": "#33691e",
    "lime900":       "#827717",
    #"yellow900":     "#f57f17",
    #"amber900":      "#ff6f00",
    #"orange900":     "#e65100",
    #"deeporange900": "#bf360c",
    "brown900":      "#3e2723",
    "grey900":       "#212121",
    "bluegrey900":   "#263238"
}

def hex_to_rgb(value):
    """ converts hex color value to nice tuple of R, G and B integer components """

    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def brightness(color):
    """ function to determine brightness of the color """ 

    colorRGB = hex_to_rgb(color)

    return colorRGB[0]*0.7+colorRGB[1]*0.7+colorRGB[2]

def luminance(color):
    """ function to determine brightness of the color """ 

    colorRGB = hex_to_rgb(color)

    return int( colorRGB[0]*0.299+colorRGB[1]*0.587+colorRGB[2]*0.114 )

def determineBackgroundColor(color):
    """ Returns one of the background colors, light or dark, for best use with given color """

    if luminance(color) > 200:
        return random.choice( list(backgroundsDark.items() ) )[1]
    else:
        return random.choice( list(backgroundsLight.items() ) )[1]

    return


def generateAvatarImage( folder ):
    """ generates and saves avatar image, with background """

    avatarImage = random.choice( files )
    pickedColorKey = random.choice( list(colors) )

    avatarColor = colors[ pickedColorKey ]["hex"]
    avatarImageName = colors[ pickedColorKey ]["name"] + " " + avatarImage

    # now, we have chosen an image and color, check if it already exists
    try:
        f = open( folder + "/" + avatarImageName )
        #print("File already exists", avatarImageName)
        f.close()
        # since the file was already generated, just return it's name
        sys.stdout.write( avatarImageName + "\n") 

    except IOError:
        #so, such file doesn't yet exist
        
        avatarBackgroundColor = determineBackgroundColor( avatarColor )

        with Image(width=128,
                   height=128,
                   background=Color( avatarBackgroundColor )) as image:

            try:
                with Image( filename = "images/" + avatarImage ) as foregroundImage:

                    foregroundImage.colorize( color = avatarColor, alpha="rgb(100%, 100%, 100%)")
                    image.composite(foregroundImage, left = 0, top = 0 )

                    image.save( filename = folder + "/" + avatarImageName )
            except IOError:
                sys.exit("File %s is not a valid image. Program stopped.", avatarImage)

                # NOw, this worked, but not quite as I expected
                #
                # image.format = "png"
                
                # png_bin = image.make_blob()
                # png_bin_base64 = base64.b64encode( png_bin )

                # sys.stdout.write( str(png_bin_base64) ) 

                #sys.stdout.detach()


                # Another thing that kinda works but not quite clear if it does the exact thing we need
                # image.format = "png"
                # png_bin = image.make_blob()

                # sys.stdout.buffer.write( png_bin )

        sys.stdout.write( avatarImageName + "\n" ) 

    return

#check if the user had provided a folder

if len(sys.argv) > 1:
    if (sys.argv[1] == "help") | (sys.argv[1] == "-h") | (sys.argv[1] == "-help") | (sys.argv[1] == "--help") :
        sys.exit("usage: python generateavatar.py folder")

if len(sys.argv)!=2:
    sys.exit("You must specify folder to store generated images" )

destinationFolder = sys.argv[1] 

if not os.path.exists( destinationFolder ):
    try:  
        os.mkdir( destinationFolder )  
    except OSError as error:  
        sys.stdout.write( "Failed to create folder: " )
        sys.exit( error)
else:
    print ("All ok, proceeding")

#fetching list of sample images

files = os.listdir("images")

if len( files ) == 0:
    sys.exit("Images folder empty. Program stopped")


#fetching JSON file with list of colores

with open('colors.json', 'r') as source:
    colorsfile = source.read()

colors = json.loads( colorsfile )

#generating image

generateAvatarImage( destinationFolder )


#print(datetime.datetime.now())

# for i in range(256):
#     #if ( i % 100 == 0 ):
#     #    print(i)
#     generateAvatarImage( destinationFolder )

#print(datetime.datetime.now())












