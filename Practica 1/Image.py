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


class stage():

    def __init__(self, stage):
        self.stage = stage

    def printStage(self):
        for x in self.stage:
            for y in x:
                print(y, end=" ")
            print()

    def cellInfo(self, num, letter):
        return num, letter, Terrain(self.stage[num - 1][ord(letter) - 65])

    def changeTerrain(self, num, letter, terrain):
        self.stage[num - 1][ord(letter) - 65] = terrain.value


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


def textToEscenario(words):
    return stage([[int(x) for x in word.split(",")] for word in words])


stage1 = textToEscenario(readFile("lab1.txt"))
stage1.printStage()
print(stage1.cellInfo(1, 'A'))
stage1.changeTerrain(1, 'A', Terrain.Sand)
stage1.printStage()
print(stage1.cellInfo(2, 'B'))
