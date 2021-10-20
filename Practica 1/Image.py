import string

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import enum


class movsTerrain:
    def __init__(self, agent):
        self.movsCost = []
        print(f"Su tipo de agente es, {agent.name}.")
        if agent == TypeAgent.humano:
            self.movsCost[Terrain.Mountain.value].append(0)
            self.movsCost[Terrain.Land.value].append(1)
            self.movsCost[Terrain.Water.value].append(2)
            self.movsCost[Terrain.Sand.value].append(3)
            self.movsCost[Terrain.Forest.value].append(3)
            self.movsCost[Terrain.Swamp.value].append(5)
            self.movsCost[Terrain.Snow.value].append(5)
        elif agent == TypeAgent.mono:
            self.movsCost[Terrain.Mountain.value].append(0)
            self.movsCost[Terrain.Land.value].append(2)
            self.movsCost[Terrain.Water.value].append(4)
            self.movsCost[Terrain.Sand.value].append(3)
            self.movsCost[Terrain.Forest.value].append(1)
            self.movsCost[Terrain.Swamp.value].append(5)
            self.movsCost[Terrain.Snow.value].append(0)
        elif agent == TypeAgent.pulpo:
            self.movsCost[Terrain.Mountain.value].append(0)
            self.movsCost[Terrain.Land.value].append(2)
            self.movsCost[Terrain.Water.value].append(1)
            self.movsCost[Terrain.Sand.value].append(0)
            self.movsCost[Terrain.Forest.value].append(3)
            self.movsCost[Terrain.Swamp.value].append(2)
            self.movsCost[Terrain.Snow.value].append(0)
        elif agent == TypeAgent.sasquatch:
            self.movsCost[Terrain.Mountain.value].append(15)
            self.movsCost[Terrain.Land.value].append(4)
            self.movsCost[Terrain.Water.value].append(0)
            self.movsCost[Terrain.Sand.value].append(0)
            self.movsCost[Terrain.Forest.value].append(4)
            self.movsCost[Terrain.Swamp.value].append(5)
            self.movsCost[Terrain.Snow.value].append(3)


class Agent(movsTerrain):  # Creamos la clase Agente
    def __init__(self, Name, TypeAgent):
        self.Name = Name
        self.TypeAgent = TypeAgent
        self.movs = movsTerrain(TypeAgent)


class posicion():
    def __init__(self, pos_ini):
        self.pos_ini = pos_ini

    def posicionini(self):
        pos_ini = input("cual es la posicion inicial")
        print(f"La posicion inicial es, {pos_ini}.")


class movimiento():
    def __init__(self, pos_new, num_mov):
        self.pos_new = pos_new
        self.num_mov = num_mov

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
    # point Initial
    init = None
    # point
    pointActual = None
    # pont final
    pointFinal = None
    # cells hide
    cellsHide = []

    def __init__(self, stage):
        self.stage = stage

    def addCellsHide(self, number, letter):
        if not self.cellsHide.__contains__((number, letter)):
            self.cellsHide.append((number, letter))

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

    def textToImage(self, x, y, text, path):
        w, h = 750, 750
        wf, hf = w / len(self.stage), h / len(self.stage)
        my_image = Image.open(path)
        image_editable = ImageDraw.Draw(my_image)
        title_font = ImageFont.truetype("Roboto/Roboto-Light.ttf", 25)
        image_editable.text((int(wf) * x, int(hf) * y), text, (0, 0, 0), font=title_font)
        my_image.save(path)

    def escenarioToImage(self, colors, path):
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

        img = Image.fromarray(data, 'RGB')
        img.save(path + '.png')
        img.show()


def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


def textToEscenario(words):
    return Stage([[int(x) for x in word.split(",")] for word in words])


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


stage1 = textToEscenario(readFile("lab1.txt"))
stage1.setValuesStage(initPoint=(7, 'B'), finalPoint=(2, 'B'))
stage1.printStage()
print(stage1.cellInfo(1, 'A'))
stage1.printStage()
print(stage1.cellInfo(2, 'B'))
stage1.escenarioToImage([
    [128, 128, 128],
    [255, 255, 255]
], 'lab1')

stage2 = textToEscenario(readFile("lab2.txt"))
stage2.escenarioToImage([
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
stage2.escenarioToImage([
    [128, 128, 128],
    [250, 191, 143],
    [0, 175, 255],
    [255, 192, 0],
    [150, 210, 80]
], 'lab2')
stage2.textToImage(0, 0, "a", "lab1.png")
stage2.textToImage(0, 1, "b", "lab1.png")
stage2.textToImage(0, 2, "c", "lab2.png")
