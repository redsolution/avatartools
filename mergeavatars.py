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

import argparse
import os
import sys
import random
import string

from hashlib import sha1
from wand.image import Image
# from wand.drawing import Drawing
from wand.color import Color


def hex_to_rgb(value):
    """ converts hex color value to nice tuple of R, G and B integer components """

    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def mergeAvatars(avatarLeft, avatarRight, folder):
    """ Just as expected, this function gets two images and merges them into a private chat avatar """

    # with Image( filename = "results/" + avatarRight ) as compositeImage:
    with Image(width=128, height=128, background=Color("#F0F0F0")) as compositeImage:

        try:
            with Image(filename=avatarLeft) as leftImage:

                # cropping image if it is not square
                leftImage.transform(resize='128x128^')

                sizeX, sizeY = leftImage.size

                deltaX = int((sizeX - 128) / 2)
                deltaY = int((sizeY - 128) / 2)

                with leftImage[(deltaX+16):(deltaX+80), (deltaY):(deltaY+128)] as cropped:
                    compositeImage.composite(cropped, left=0, top=0)
        except:
            # raise Exception("first avatar can't be opened")
            sys.exit("First avatar file " + avatarLeft + " can't be opened or is not an image.")

        try:
            with Image(filename=avatarRight) as rightImage:

                # cropping image if it is not square
                rightImage.transform(resize='128x128^')

                sizeX, sizeY = rightImage.size

                deltaX = int((sizeX - 128) / 2)
                deltaY = int((sizeY - 128) / 2)

                with rightImage[(deltaX+48):(deltaX+112), (deltaY):(deltaY+128)] as cropped2:
                    compositeImage.composite(cropped2, left=64, top=0)
        except:
            # raise Exception("second  avatar can't be opened")
            sys.exit("Second avatar file " + avatarRight + "  can't be opened or is not an image.")

        # save temporary file to specified folder

        temporaryFile = folder + "/" + ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10)) + ".png"
        compositeImage.save(filename=temporaryFile)

        # get sha1 hash of temporary file
        imageHash = sha1(open(temporaryFile, 'rb').read()).hexdigest() + ".png"

        resultFile = folder + "/" + imageHash

        # rename temporary file
        os.rename(temporaryFile, resultFile)

        # write filename to stdout
        sys.stdout.write(imageHash + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A simple utility to generate avatars from two given images.')
    parser.add_argument('FirstAvatar', metavar='first-avatar', type=str,
                        help='You must specify path to first avatar')
    parser.add_argument('SecondAvatar', metavar='second-avatar', type=str,
                        help='You must specify path to second avatar')
    parser.add_argument('Path', metavar='path', type=str,
                        help='You must specify path to store generated image')

    args = parser.parse_args()
    dst_folder = os.path.abspath(args.Path)

    # check if destination folder exists, trying to create it
    if not os.path.exists(dst_folder):
        try:
            os.mkdir(dst_folder)
        except OSError as err:
            sys.exit(err)

    mergeAvatars(args.FirstAvatar, args.SecondAvatar, dst_folder)
