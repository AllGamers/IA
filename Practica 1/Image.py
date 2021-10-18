import string

from PIL import Image
import numpy as np
import enum


class Terrain(enum.Enum):
    Mountain = 0
    Land = 1
    Water = 2
    Sand = 3
    Forest = 4


def cellInfo(environment, num, letter):
    print(Terrain(int(environment[num - 1][ord(letter) - 65])))


def a():
    w, h = 750, 750
    data = np.zeros((h, w, 3), dtype=np.uint8)
    data[0:256, 0:256] = [255, 0, 0]  # red patch in upper left
    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    img.show()


def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


def textToArray(words):
    return [word.split(",") for word in words]


def printMatrix(matrix):
    for x in matrix:
        for y in x:
            print(y, end=" ")
        print()


matrix = textToArray(readFile("lab1.txt"))
printMatrix(matrix)
cellInfo(matrix, 1, 'A')
cellInfo(matrix, 2, 'B')
