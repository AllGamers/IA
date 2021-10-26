__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 1"
__asginatura__ = "Inteligencia Artificial"

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import enum
import array as arr


class MovsTerrainCosts:
    def __init__(self, agent):
        self.movsCost = arr.array('i', 7 * [0])
        if agent == TypeAgent.humano:
            self.movsCost[int(Terrain.Mountain.value)] = 0
            self.movsCost[int(Terrain.Land.value)] = 1
            self.movsCost[int(Terrain.Water.value)] = 2
            self.movsCost[int(Terrain.Sand.value)] = 3
            self.movsCost[int(Terrain.Forest.value)] = 3
            self.movsCost[int(Terrain.Swamp.value)] = 5
            self.movsCost[int(Terrain.Snow.value)] = 5
        elif agent == TypeAgent.mono:
            self.movsCost[int(Terrain.Mountain.value)] = 0
            self.movsCost[int(Terrain.Land.value)] = 2
            self.movsCost[int(Terrain.Water.value)] = 4
            self.movsCost[int(Terrain.Sand.value)] = 3
            self.movsCost[int(Terrain.Forest.value)] = 1
            self.movsCost[int(Terrain.Swamp.value)] = 5
            self.movsCost[int(Terrain.Snow.value)] = 0
        elif agent == TypeAgent.pulpo:
            self.movsCost[int(Terrain.Mountain.value)] = 0
            self.movsCost[int(Terrain.Land.value)] = 2
            self.movsCost[int(Terrain.Water.value)] = 1
            self.movsCost[int(Terrain.Sand.value)] = 0
            self.movsCost[int(Terrain.Forest.value)] = 3
            self.movsCost[int(Terrain.Swamp.value)] = 2
            self.movsCost[int(Terrain.Snow.value)] = 0
        elif agent == TypeAgent.sasquatch:
            self.movsCost[int(Terrain.Mountain.value)] = 15
            self.movsCost[int(Terrain.Land.value)] = 4
            self.movsCost[int(Terrain.Water.value)] = 0
            self.movsCost[int(Terrain.Sand.value)] = 0
            self.movsCost[int(Terrain.Forest.value)] = 4
            self.movsCost[int(Terrain.Swamp.value)] = 5
            self.movsCost[int(Terrain.Snow.value)] = 3


class Terrain(enum.Enum):
    Mountain = 0  # 128,128,128
    Land = 1  # 250,191,143
    Water = 2  # 0,175,255
    Sand = 3  # 255,192,0
    Forest = 4  # 150,210,80
    Swamp = 5  # 178,162,198
    Snow = 6  # 242,242,242


class TypeAgent(enum.Enum):
    humano = 0
    mono = 1
    pulpo = 2
    sasquatch = 3


class Stage:
    # cells hide

    def __init__(self, textPlain):
        self.stage = [[int(x) for x in word.split(",")] for word in textPlain]
        self.stageLetras = [[int(x) for x in word.split(",")] for word in textPlain]
        self.cellsHide = []

    def addCellsHide(self, number, letter):
        if not self.cellsHide.__contains__((number, letter)):
            self.cellsHide.append((number, letter))

    def existsInCellsHide(self, Coords):
        if self.cellsHide.__contains__(giveNumLetter(Coords)):
            return True
        return False

    def hideAllStage(self):
        for x, xcontain in enumerate(self.stage):
            for y, ycontain in enumerate(xcontain):
                self.addCellsHide(giveNumLetter((x, y))[0], giveNumLetter((x, y))[1])

    def unHide(self, Coords=None, num=None, letter=None):  # remove de cellsHide
        if Coords == None:
            if self.existsInCellsHide(giveCords(num, letter)):
                self.cellsHide.remove((num, letter))
        else:
            if self.existsInCellsHide(Coords):
                self.cellsHide.remove(giveNumLetter(Coords))

    def printStage(self):
        for x in self.stage:
            for y in x:
                print(y, end=" ")
            print()

    def cellInfo(self, Coords=None, num=None, letter=None):
        if Coords != None:
            return Terrain(self.stage[Coords[0]][Coords[1]])
        else:
            Coords = giveCords((num, letter))
            return Terrain(self.stage[Coords[0]][Coords[1]])

    def changeTerrain(self, num, letter, terrain):
        self.stage[num - 1][ord(letter) - 65] = terrain.value

    def textToImage(self, x, y, text, path):
        w, h = 750, 750
        wf, hf = w / len(self.stageLetras), h / len(self.stageLetras)
        my_image = Image.open(path)
        image_editable = ImageDraw.Draw(my_image)
        title_font = ImageFont.truetype("Roboto/Roboto-Light.ttf", 25)
        for countx, frameX in enumerate(self.stageLetras):
            for county, frameY in enumerate(frameX):
                if x == countx and y == county:
                    if len(str(self.optionsStage[countx][county])) == 1:
                        self.optionsStage[countx][county] = str(self.optionsStage[countx][county]) + "," + text
                        image_editable.text((int(wf) * x, int(hf) * y), text, (0, 0, 0), font=title_font)
                    elif len(str(self.optionsStage[countx][county])) == 3:
                        self.optionsStage[countx][county] = str(self.optionsStage[countx][county]) + "," + text
                        image_editable.text((int(wf) * x + wf / 2, int(hf) * y), text, (0, 0, 0), font=title_font)
                    elif len(str(self.optionsStage[countx][county])) == 5:
                        self.optionsStage[countx][county] = str(self.optionsStage[countx][county]) + "," + text
                        image_editable.text((int(wf) * x, int(hf) * y + hf / 2), text, (0, 0, 0), font=title_font)
                    elif len(str(self.optionsStage[countx][county])) == 7:
                        self.optionsStage[countx][county] = str(self.optionsStage[countx][county]) + "," + text
                        image_editable.text((int(wf) * x + wf / 2, int(hf) * y + hf / 2), text, (0, 0, 0),
                                            font=title_font)
        my_image.save(path)

    def stageToImage(self, path):
        colors = [
            [128, 128, 128],
            [250, 191, 143],
            [0, 175, 255],
            [255, 192, 0],
            [150, 210, 80],
            [178, 162, 198],
            [242, 242, 242],
        ]
        w, h = 750, 750
        wf, hf = w / len(self.stage), h / len(self.stage)
        data = np.zeros((h, w, 3), dtype=np.uint8)
        for countx, frameX in enumerate(self.stage):
            for county, frameY in enumerate(frameX):
                for countc, color in enumerate(colors):
                    if int(frameY) == countc:
                        if self.existsInCellsHide((countx, county)):
                            data[countx * int(wf):(countx + 1) * int(wf),
                            county * int(hf):(county + 1) * int(hf)] = [0, 0, 0]
                        else:
                            data[countx * int(wf):(countx + 1) * int(wf),
                            county * int(hf):(county + 1) * int(hf)] = color
                        # cuadrado
                        if countx > 0 or countx < 750 and county > 0 or county < 750:
                            data[countx * int(wf):(countx + 1) * int(wf), county * int(hf)] = [0, 0, 0]  # izquierda
                            data[countx * int(wf), county * int(hf):(county + 1) * int(hf)] = [0, 0, 0]  # abajo
                        break
        self.optionsStage = self.stageLetras
        img = Image.fromarray(data, 'RGB')
        img.save(path + '.png')
        # img.show()


class Movement:
    def __init__(self, InitalCords, FinalCords, Hide, DiagonalMovs=False):
        self.DiagonalMovs = DiagonalMovs
        self.Hide = Hide
        self.numMovs = 0
        # Memory
        self.memoryCells = []
        # Memory Decisions
        self.memoryCellsDecisions = []
        self.addToMemory(giveCords(InitalCords))
        self.InitialCords = giveCords(InitalCords)
        self.ActualCords = giveCords(InitalCords)
        self.FinalCords = giveCords(FinalCords)
        if self.Hide:
            self.hideAllStage()
            self.unHideActualPosition()
        self.stageToImage(self.Name)
        self.textToImage(self.InitialCords[1], self.InitialCords[0], " I", self.Name + ".png")
        self.textToImage(self.FinalCords[1], self.FinalCords[0], " F", self.Name + ".png")

    def upLeftCord(self):
        if self.DiagonalMovs:
            return self.ActualCords[0] - 1, self.ActualCords[1] - 1

    def downLeftCord(self):
        if self.DiagonalMovs:
            return self.ActualCords[0] + 1, self.ActualCords[1] - 1

    def upRightCord(self):
        if self.DiagonalMovs:
            return self.ActualCords[0] - 1, self.ActualCords[1] + 1

    def downRightCord(self):
        if self.DiagonalMovs:
            return self.ActualCords[0] + 1, self.ActualCords[1] + 1

    def upCord(self):
        return self.ActualCords[0] - 1, self.ActualCords[1]

    def downCord(self):
        return self.ActualCords[0] + 1, self.ActualCords[1]

    def leftCord(self):
        return self.ActualCords[0], self.ActualCords[1] - 1

    def rightCord(self):
        return self.ActualCords[0], self.ActualCords[1] + 1

    def validRoads(self):
        # Funcion que verifica los caminos posibles sin haber pasado
        arrayValid = []
        if self.isValidPosition(self.leftCord()) and not self.existsInMemory(self.leftCord()):
            arrayValid.append(self.leftCord())
        if self.isValidPosition(self.rightCord()) and not self.existsInMemory(self.rightCord()):
            arrayValid.append(self.rightCord())
        if self.isValidPosition(self.upCord()) and not self.existsInMemory(self.upCord()):
            arrayValid.append(self.upCord())
        if self.isValidPosition(self.downCord()) and not self.existsInMemory(self.downCord()):
            arrayValid.append(self.downCord())
        if self.DiagonalMovs:
            if self.isValidPosition(self.upRightCord()) and not self.existsInMemory(self.upRightCord()):
                arrayValid.append(self.upRightCord())
            if self.isValidPosition(self.upLeftCord()) and not self.existsInMemory(self.upLeftCord()):
                arrayValid.append(self.upLeftCord())
            if self.isValidPosition(self.downRightCord()) and not self.existsInMemory(self.downRightCord()):
                arrayValid.append(self.downRightCord())
            if self.isValidPosition(self.downLeftCord()) and not self.existsInMemory(self.downLeftCord()):
                arrayValid.append(self.downLeftCord())
        return arrayValid

    def movLeft(self):
        self.mov(self.leftCord())

    def movRight(self):
        self.mov(self.rightCord())

    def movUp(self):
        self.mov(self.upCord())

    def movDown(self):
        self.mov(self.downCord())

    def movUpRight(self):
        if self.DiagonalMovs:
            self.mov(self.upRightCord())

    def movUpLeft(self):
        if self.DiagonalMovs:
            self.mov(self.upLeftCord())

    def movDownRight(self):
        if self.DiagonalMovs:
            self.mov(self.downRightCord())

    def movDownLeft(self):
        if self.DiagonalMovs:
            self.mov(self.downLeftCord())


class Agent(MovsTerrainCosts, Stage, Movement):  # Create the class Agent

    def __init__(self, Name, TypeAgent, InitalCords, stageText, FinalCords, AgentSensor=None, AgentMovs=None,
                 Hide=False, DiagonalMovs=False):
        self.Name = Name
        self.TypeAgent = TypeAgent
        MovsTerrainCosts.__init__(self, agent=TypeAgent)
        Stage.__init__(self, textPlain=stageText)
        self.AgentSensor = AgentSensor
        self.AgentMovs = AgentMovs
        if not self.isValidPosition(giveCords(InitalCords)):
            print(f"Error con Cordenadas iniciales")
            exit()
        elif not self.isValidPosition(giveCords(FinalCords)):
            print(f"Error con Cordenadas finales")
            exit()
        else:
            Movement.__init__(self, InitalCords=InitalCords, FinalCords=FinalCords, Hide=Hide,
                              DiagonalMovs=DiagonalMovs)

    def unHideActualPosition(self):
        self.unHide(self.ActualCords)
        self.unHide(self.upCord())
        self.unHide(self.downCord())
        self.unHide(self.leftCord())
        self.unHide(self.rightCord())
        if self.DiagonalMovs:
            self.unHide(self.upRightCord())
            self.unHide(self.upLeftCord())
            self.unHide(self.downLeftCord())
            self.unHide(self.downRightCord())

    def addToMemory(self, coords):
        if not self.existsInMemory(coords):
            self.memoryCells.append(coords)

    def existsInMemory(self, coords):
        return self.memoryCells.__contains__(coords)

    def isValidPosition(self, Coords):
        return self.giveCost(Coords) != 0

    def giveCost(self, Coords):
        return self.movsCost[self.cellInfo(Coords=Coords).value]

    def returnCost(self, typeTerrain):
        return self.movsCost[typeTerrain.value]

    def printAgent(self):
        print(f"~~~~~~~~~~~~\nNombre:{self.Name} \nTipo:{self.TypeAgent.name} \nMovs")
        for num, x in enumerate(self.movsCost):
            print("- {}: {}".format(Terrain(num).name, x))
        print("~~~~~~~~~~~~")

    def GiveColor(self):
        if self.TypeAgent == TypeAgent.pulpo:
            return (70, 0, 130)
        if self.TypeAgent == TypeAgent.humano:
            return (193, 178, 36)
        if self.TypeAgent == TypeAgent.mono:
            return (122, 88, 13)
        if self.TypeAgent == TypeAgent.sasquatch:
            return (3, 184, 159)

    def updateStage(self):
        self.stageToImage(self.Name)

    def mov(self, destiny):
        if self.isValidPosition(destiny):
            self.textToImage(destiny[1], destiny[0], "V", self.Name + ".png")
            self.ActualCords = destiny
            self.unHideActualPosition()
            self.updateStage()
            self.addToMemory(self.ActualCords)
            print(f"{self.ActualCords}.")
            self.numMovs += 1
            print(self.memoryCells)


def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


def giveCords(tuplaNumLetter):
    return (tuplaNumLetter[0] - 1), (ord(tuplaNumLetter[1]) - 65)


def giveNumLetter(Coords):
    return (Coords[0] + 1), chr(Coords[1] + 65)
