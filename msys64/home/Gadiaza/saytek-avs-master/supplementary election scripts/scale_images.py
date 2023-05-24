#!/usr/bin/env python3

"""
An unoptomized wrapper to imagemagick resize.
Created expressly for Saytek AVS (resizing candidate images)
"""
####TODO: Maybe move to the third party imagemagick python module
import subprocess
import argparse
import os

width_px = 96
height_px = 96
density = 96
quality = 100
output_folder = "../"

def resizeImage(fileName, width_px, height_px, density=96, quality=100, source_folder=None, output_folder=None):
    source_folder = source_folder or "./"
    if output_folder is None:
        output_folder = "./resized_images/"

    if not source_folder or source_folder[-1] != "/":
        source_folder += "/"

    if not output_folder or output_folder[-1] != "/":
        output_folder += "/"

    if not os.access(output_folder, os.F_OK):
        os.mkdir(output_folder)

    if not isImage(source_folder + fileName):
        print("%s is not an image." % fileName)
        return

    dimensions = ("%sx%s" % (width_px, height_px))
    print(fileName)
    print("Resize with the following parameters\n  Dimensions: %s\n  Density: %s\n  Quality: %s\n" % (dimensions, density, quality))
    subprocess.run(["convert", source_folder + fileName, "-resize", dimensions, "-density", str(density), "-quality", str(quality), (output_folder + fileName)])

def isImage(fileName):
    formats = (".png", ".jpg", ".gif")
    for format in formats:
        if fileName.endswith(format):
            return True

    return False

def resizeImages(directory=None, output_folder=None):
    directory = directory or "./"
    files = subprocess.getoutput('ls "' + directory + '"').splitlines()
    for fileName in files:
        fileName =  fileName
        resizeImage(fileName, width_px, height_px, density, quality, directory, output_folder)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A wrapper around ImageMagick's convert to scale/resize images")
    parser.add_argument("source", default=None, nargs="?", help="directory containing the source image files")
    parser.add_argument("destination", default=None, nargs="?", help="folder to place the resized images in")
    args = parser.parse_args()

    resizeImages(args.source, args.destination)
    print("Done resizing images.")
