import string

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
    # memory of cells (Tree)
    memory = None
    # pont final
    pointFinal = None
    # ActualPoint
    pointActual = None
    # cells hide
    cellsHide = []
    # options
    optionsStage = [[]]

    def __init__(self, textPlain, initPoint, finalPoint):
        self.init = initPoint
        self.pointActual = initPoint
        self.pointFinal = finalPoint
        self.stage = [[int(x) for x in word.split(",")] for word in textPlain]

    def addCellsHide(self, number, letter):
        if not self.cellsHide.__contains__((number, letter)):
            self.cellsHide.append((number, letter))

    def setValuesStageActual(self, pointActual):
        self.pointActual = pointActual

    def printStage(self):
        for x in self.stage:
            for y in x:
                print(y, end=" ")
            print()

    def cellInfo(self, num, letter):
        return num, letter, Terrain(self.stage[num - 1][ord(letter) - 65])

    def changeTerrain(self, num, letter, terrain):
        self.stage[num - 1][ord(letter) - 65] = terrain.value

    def textToImage(self, x, y, text, path):
        w, h = 750, 750
        wf, hf = w / len(self.stage), h / len(self.stage)
        my_image = Image.open(path)
        image_editable = ImageDraw.Draw(my_image)
        title_font = ImageFont.truetype("Roboto/Roboto-Light.ttf", 25)
        for countx, frameX in enumerate(self.stage):
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

    def stageToImage(self, colors, path):
        w, h = 750, 750
        wf, hf = w / len(self.stage), h / len(self.stage)
        data = np.zeros((h, w, 3), dtype=np.uint8)
        for countx, frameX in enumerate(self.stage):
            for county, frameY in enumerate(frameX):
                for countc, color in enumerate(colors):
                    if int(frameY) == countc:
                        data[countx * int(wf):(countx + 1) * int(wf), county * int(hf):(county + 1) * int(hf)] = color
                        # cuadrado
                        if countx > 0 or countx < 750 and county > 0 or county < 750:
                            data[countx * int(wf):(countx + 1) * int(wf), county * int(hf)] = [0, 0, 0]  # izquierda
                            data[countx * int(wf), county * int(hf):(county + 1) * int(hf)] = [0, 0, 0]  # abajo
                        break
        self.optionsStage = self.stage
        img = Image.fromarray(data, 'RGB')
        img.save(path + '.png')
        img.show()



class Agent(MovsTerrainCosts, Stage):  # Create the class Agent
    def __init__(self, Name, TypeAgent, InitalCords, stage, FinalCords, AgentSensor=None, AgentMovs=None):
        self.Name = Name
        self.TypeAgent = TypeAgent
        self.movsCosts = MovsTerrainCosts(TypeAgent)
        self.AgentSensor = AgentSensor
        self.AgentMovs = AgentMovs
        self.numMovs = 0
        self.InitialCords = InitalCords
        self.ActualCords = InitalCords
        self.Stage = Stage(stage, InitalCords, FinalCords)

    def returnCost(self, typeTerrain):
        return self.movsCosts.movsCost[typeTerrain.value]

    def printAgent(self):
        print(f"~~~~~~~~~~~~\nNombre:{self.Name} \nTipo:{self.TypeAgent.name} \nMovs")
        for num, x in enumerate(self.movsCosts.movsCost):
            print("- {}: {}".format(Terrain(num).name, x))
        print("~~~~~~~~~~~~")

    def movimientoizquierda(self):
        print(f"Usted de encuentra en la posicion:, {self.pos_ini}.")
        self.pos_ini = self.pos_new
        print("Su movimiento es a la izquierda.")
        print(f"Su nueva posicion es:, {self.pos_new}.")
        self.num_mov += 1

    def movimientoderecha(self):
        print(f"Usted de encuentra en la posicion:, {self.pos_ini}.")
        self.pos_ini = self.pos_new
        print("Su movimiento es a la derecha.")
        print(f"Su nueva posicion es:, {self.pos_new}.")
        self.num_mov += 1

    def movimientoarriba(self):
        print(f"Usted de encuentra en la posicion:, {self.pos_ini}.")
        self.pos_ini = self.pos_new
        print("Su movimiento es a la arriba.")
        print(f"Su nueva posicion es:, {self.pos_new}.")
        self.num_mov += 1

    def movimientoabajo(self):
        print(f"Usted de encuentra en la posicion:, {self.pos_ini}.")
        self.pos_ini = self.pos_new
        print("Su movimiento es a la abajo.")
        print(f"Su nueva posicion es:, {self.pos_new}.")
        self.num_mov += 1


def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


def tipoagente(self, personaje):
    self.personaje = personaje
    personaje = input("Que personaje desea seleccionar: h. Humano m. Mono p. Pulpo s. Sasquatch")
    if personaje == "h":
        print("Ha seleccionado el agente Humano.")
        self.tipo_agente = "humano"
    elif personaje == "m":
        print("Ha seleccionado el agente Mono.")
        self.tipo_agente = "mono"
    elif personaje == "p":
        print("Ha seleccionado el agente Pulpo.")
        self.tipo_agente = "pulpo"
    elif personaje == "s":
        print("Ha seleccionado el agente Sasquatch.")
        self.tipo_agente = "sasquatch"


def giveCords(tuplaNumLetter):
    return tuplaNumLetter[0]-1,(ord(tuplaNumLetter[1])-65)



stage1 = Stage(readFile("lab1.txt"))
stage1.setValuesStage(initPoint=(7, 'B'), finalPoint=(2, 'B'))
stage1.printStage()
print(stage1.cellInfo(1, 'A'))
stage1.printStage()
print(stage1.cellInfo(2, 'B'))
stage1.stageToImage([
    [128, 128, 128],
    [255, 255, 255]
], 'lab1')

stage2 = Stage(readFile("lab2.txt"))
stage2.stageToImage([
    [128, 128, 128],
    [250, 191, 143],
    [0, 175, 255],
    [255, 192, 0],
    [150, 210, 80]
], 'lab2')

stage2.addCellsHide(1, 'A')
print(stage2.cellsHide)
stage2.addCellsHide(1, 'A')
print(stage2.cellsHide)
stage2.addCellsHide(1, 'B')
print(stage2.cellsHide)
# stage2.textToImage(0,0,"a","lab1.png")
# stage2.textToImage(0,1,"b","lab1.png")
stage2.textToImage(0, 2, "c", "lab2.png")
stage2.textToImage(0, 2, "b", "lab2.png")
stage2.textToImage(0, 2, "a", "lab2.png")
stage2.textToImage(0, 2, "d", "lab2.png")

agent1 = Agent("A2", TypeAgent.humano, InitalCords=giveCords((2, 'A')), stage=stage1, FinalCords=giveCords((2, 'A')))

agent1.printAgent()
print(f"Costo snow {agent1.returnCost(typeTerrain=Terrain.Snow)}")
