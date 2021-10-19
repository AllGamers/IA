import string

from PIL import Image
import numpy as np
import enum


class Terrain(enum.Enum):
    Mountain = 0    #128,128,128
    Land = 1        #250,191,143
    Water = 2       #0,175,255
    Sand = 3        #255,192,0
    Forest = 4      #150,210,80

class Stage:
    # memory of cells (Tree)
    memory = None
    # point Initial
    init = None
    # point
    pointActual = None
    # pont final
    pointFinal = None

    def __init__(self, stage):
        self.stage = stage

    def setValuesStage(self, initPoint, finalPoint):
        self.init = initPoint
        self.pointActual = initPoint
        self.pointFinal = finalPoint

    def printStage(self):
        for x in self.stage:
            for y in x:
                print(y, end=" ")
            print()

    def cellInfo(self, num, letter):
        return num, letter, Terrain(self.stage[num - 1][ord(letter) - 65])

    def changeTerrain(self, num, letter, terrain):
        self.stage[num - 1][ord(letter) - 65] = terrain.value

    def escenarioToImage(self, colors, path):
        w, h = 750, 750
        wf, hf = w/len(self.stage),h/len(self.stage)
        data = np.zeros((h, w, 3), dtype=np.uint8)
        for countx,frameX in enumerate(self.stage):
            for county,frameY in enumerate(frameX):
                for countc,color in enumerate(colors):
                    if int(frameY)==countc:
                        data[countx*int(wf):(countx+1)*int(wf), county*int(hf):(county+1)*int(hf)] = color
                        #cuadrado
                        if countx > 0 or countx < 750 and county > 0 or county < 750:
                            data[countx*int(wf):(countx+1)*int(wf), county*int(hf)] = [0,0,0] #izquierda
                            data[countx*int(wf), county*int(hf):(county+1)*int(hf)] = [0,0,0] #abajo
                        break
                  
        img = Image.fromarray(data, 'RGB')
        img.save(path+'.png')
        img.show()


def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


def textToEscenario(words):
    return Stage([[int(x) for x in word.split(",")] for word in words])


stage1 = textToEscenario(readFile("lab1.txt"))
stage1.setValuesStage(initPoint=(7, 'B'), finalPoint=(2, 'B'))
stage1.printStage()
print(stage1.cellInfo(1, 'A'))
stage1.changeTerrain(1, 'A', Terrain.Sand)
stage1.printStage()
print(stage1.cellInfo(2, 'B'))
stage1.escenarioToImage([
    [128,128,128], 
    [255,255,255]
],'lab1')

stage2 = textToEscenario(readFile("lab2.txt"))
stage2.escenarioToImage([
    [128,128,128],
    [250,191,143],
    [0,175,255],
    [255,192,0],
    [150,210,80]
],'lab2')