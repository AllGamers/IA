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


class Stage:
    # memory of cells (Tree)
    memory = None
    # point Initial
    init = None
    # point
    point = None
    # pont final
    pointFinal = None

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

    def escenarioToImage(self):
        w, h = 750, 750
        print(len(self.stage))
        wf, hf = w/len(self.stage),h/len(self.stage)
        print(wf,hf) 
        data = np.zeros((h, w, 3), dtype=np.uint8)
        for countx,frameX in enumerate(self.stage):
            for county,frameY in enumerate(frameX):
                if int(frameY)==1:
                    data[countx*int(wf):(countx+1)*int(wf), county*int(hf):(county+1)*int(hf)] = [255, 0, 0]
                else:
                    data[countx*int(wf):(countx+1)+int(wf), county*int(hf):(county+1)*int(hf)] = [0,0,0]
        img = Image.fromarray(data, 'RGB')
        img.save('my.png')
        img.show()


def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


def textToEscenario(words):
    return Stage([[int(x) for x in word.split(",")] for word in words])


stage1 = textToEscenario(readFile("lab1.txt"))
stage1.printStage()
print(stage1.cellInfo(1, 'A'))
stage1.changeTerrain(1, 'A', Terrain.Sand)
stage1.printStage()
print(stage1.cellInfo(2, 'B'))
stage1.escenarioToImage()