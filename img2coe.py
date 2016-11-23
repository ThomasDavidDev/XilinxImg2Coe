# import the necessary packages
import argparse
import os
import cv2
import numpy as np

# construct the argument parser and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True, help='Input Image path.')
parser.add_argument('-r', '--red', required=True, help='Red output COE path.')
parser.add_argument('-g', '--green', required=True, help='Green output COE path.')
parser.add_argument('-b', '--blue', required=True, help='Blue output COE path.')
parser.add_argument('-d', '--depth', required=True, help='Bit Depth.')
args = parser.parse_args()

pathInput = os.path.abspath(args.input)
pathRed = os.path.abspath(args.red)
pathGreen = os.path.abspath(args.green)
pathBlue = os.path.abspath(args.blue)
pathOutput = [pathRed, pathBlue, pathGreen]
bitDepth = int(args.depth)

print("Input: {0}".format(pathInput))
print("Red Channel: {0}".format(pathRed))
print("Green Channel: {0}".format(pathGreen))
print("Blue Channel: {0}".format(pathBlue))

# open the image and generate red, green and black array
imageInput = cv2.imread(pathInput, cv2.IMREAD_COLOR)
imageReshape = imageInput.reshape((-1, 3))
imageRedGreenBlue = np.transpose(imageReshape)

# generate coe files
for color in range(3):
    print("Exporting {0}".format("red" if color == 0 else "green" if color == 1 else "blue"))

    colorArray = imageRedGreenBlue[color]
    colorOuput = pathOutput[color]
    if os.path.exists(colorOuput):
        os.remove(colorOuput)
    file = open(colorOuput, 'w')

    file.write(";******************************************************************\n")
    file.write(";************ .COE file generator - By Thomas Devoogdt ************\n")
    file.write(";******************************************************************\n")
    file.write("; v1.0\n")
    file.write("memory_initialization_radix={0}\n".format(16))
    file.write("memory_initialization_vector=\n")

    length = len(colorArray)
    for index in range(length):
        file.write(
            "{0}{1}\n".format(
                format(colorArray[index], '08b')[0:bitDepth],
                ',' if index != length - 1 else ';'
            )
        )

    file.close()

print("Closed without errors")
