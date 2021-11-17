__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 2"
__asginatura__ = "Inteligencia Artificial"

from typing import Dict
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import enum
import array as arr
from queue import PriorityQueue


class MovsTerrainCosts:
    def __init__(self, agent):
        self.movsCost = arr.array('i', 7 * [0])
        if agent == TypeAgent.humano:
            self.movsCost[int(Terrain.Mountain.value)] = 0
            self.movsCost[int(Terrain.Land.value)] = 1
            self.movsCost[int(Terrain.Water.value)] = 2
            self.movsCost[int(Terrain.Sand.value)] = 3
            self.movsCost[int(Terrain.Forest.value)] = 4
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


class Mov(enum.Enum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3
    UpLeft = 4
    UpRight = 5
    DownLeft = 6
    DownRight = 7


class TypeAgent(enum.Enum):
    humano = 0
    mono = 1
    pulpo = 2
    sasquatch = 3


class Stage:
    # cells hide

    def __init__(self, textPlain):
        self.stage = [[int(x) for x in word.split(",")] for word in textPlain]
        self.stageLetras = [["" for x in word.split(",")] for word in textPlain]
        self.cellsHide = []

    def addStageLetras(self, x, y, text):
        if not self.stageLetras[x][y].__contains__(text):
            self.stageLetras[x][y] += str(text + ",")

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

    def printStageLetter(self):
        print("Stage")
        for x in self.stageLetras:
            for y in x:
                print(f"[{y:<8}]", end=' ')
            print()

    def cellInfo(self, Coords=None, num=None, letter=None):
        if Coords != None:
            return Terrain(self.stage[Coords[0]][Coords[1]])
        else:
            Coords = giveCords((num, letter))
            return Terrain(self.stage[Coords[0]][Coords[1]])

    def changeTerrain(self, num, letter, terrain):
        self.stage[num - 1][ord(letter) - 65] = terrain.value

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
        data = np.zeros((h + 50, w + 50, 3), dtype=np.uint8)
        # data = np.zeros((h , w, 3), dtype=np.uint8)
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

                        if (countx == 14):
                            data[(countx+1 ) * int(wf):(countx + 2) * int(wf),
                            (county) * int(hf):(county+1) * int(hf)] = [213, 213, 213]
                        if (county == 14):
                            data[(countx) * int(wf):(countx + 1 + 1) * int(wf),
                            (county + 1) * int(hf):(county + 1 + 1) * int(hf)] = [213, 213, 213]

                        # cuadrado
                        if countx > 0 or countx < 750 and county > 0 or county < 750:
                            data[countx * int(wf):(countx + 1) * int(wf), county * int(hf)] = [0, 0, 0]  # izquierda
                            data[countx * int(wf), county * int(hf):(county + 1) * int(hf)] = [0, 0, 0]  # abajo
                        break
        self.optionsStage = self.stageLetras
        img = Image.fromarray(data, 'RGB')
        img.save(path + '.png')
        # Reopen
        my_image = Image.open(path + '.png')
        image_editable = ImageDraw.Draw(my_image)
        # title_font = ImageFont.truetype("LibsGameV3/Roboto/Roboto-Light.ttf", 15)
        title_font = ImageFont.truetype("Roboto/Roboto-Light.ttf", 15)
        for countx, frameX in enumerate(self.stageLetras):
            for county, frameY in enumerate(frameX):
                if countx == 14:
                    image_editable.text((county * wf, int(hf) * (countx + 1)),
                                        "\n" + str(county), (0, 0, 0),
                                        font=title_font)
                if county == 14:
                    image_editable.text(((county + 1) * wf, int(hf) * (countx)),
                                        str(countx), (0, 0, 0),
                                        font=title_font)
                if len(frameY) > 0:
                    image_editable.text((county * wf, int(hf) * countx),
                                        self.stageLetras[countx][county], (0, 0, 0),
                                        font=title_font)
        my_image.save(path + ".png")
        # img.show()


class Movement:
    def __init__(self, InitalCords, FinalCords, Hide, DiagonalMovs=False):
        self.DiagonalMovs = DiagonalMovs
        self.Hide = Hide
        self.numMovs = 0
        self.InitialCords = giveCords(InitalCords)
        self.ActualCords = giveCords(InitalCords)
        self.FinalCords = giveCords(FinalCords)

        if self.Hide:
            self.hideAllStage()
            self.unHideActualPosition()
        self.stageToImage(self.Name)

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

    def upCord(self, coords=None):
        if coords is None:
            return self.ActualCords[0] - 1, self.ActualCords[1]
        else:
            return coords[0] - 1, coords[1]

    def downCord(self, coords=None):
        if coords is None:
            return self.ActualCords[0] + 1, self.ActualCords[1]
        else:
            return coords[0] + 1, coords[1]

    def leftCord(self, coords=None):
        if coords == None:
            return self.ActualCords[0], self.ActualCords[1] - 1
        else:
            return coords[0], coords[1] - 1

    def rightCord(self, coords=None):
        if coords == None:
            return self.ActualCords[0], self.ActualCords[1] + 1
        else:
            return coords[0], coords[1] + 1

    def validRoads2(self):
        # Funcion que verifica los caminos posibles sin haber pasado
        arrayValid = []
        if self.isValidPosition(self.leftCord()) and not self.existsInMemory(self.leftCord()):
            arrayValid.append(Mov.Left)
        if self.isValidPosition(self.rightCord()) and not self.existsInMemory(self.rightCord()):
            arrayValid.append(Mov.Right)
        if self.isValidPosition(self.upCord()) and not self.existsInMemory(self.upCord()):
            arrayValid.append(Mov.Up)
        if self.isValidPosition(self.downCord()) and not self.existsInMemory(self.downCord()):
            arrayValid.append(Mov.Down)
        if self.DiagonalMovs:
            if self.isValidPosition(self.upRightCord()) and not self.existsInMemory(self.upRightCord()):
                arrayValid.append(Mov.UpRight)
            if self.isValidPosition(self.upLeftCord()) and not self.existsInMemory(self.upLeftCord()):
                arrayValid.append(Mov.UpLeft)
            if self.isValidPosition(self.downRightCord()) and not self.existsInMemory(self.downRightCord()):
                arrayValid.append(Mov.DownRight)
            if self.isValidPosition(self.downLeftCord()) and not self.existsInMemory(self.downLeftCord()):
                arrayValid.append(Mov.DownLeft)
        if (len(arrayValid) > 1):
            self.addToMemoryDecisions(self.ActualCords)
        return arrayValid

    def validRoads3(self, coord):
        # Funcion que verifica los caminos posibles sin haber pasado
        arrayValid = []
        if self.isValidPosition(self.leftCord(coord)) and not self.existsInMemory(self.leftCord(coord)):
            arrayValid.append(Mov.Left)
        if self.isValidPosition(self.rightCord(coord)) and not self.existsInMemory(self.rightCord(coord)):
            arrayValid.append(Mov.Right)
        if self.isValidPosition(self.upCord(coord)) and not self.existsInMemory(self.upCord(coord)):
            arrayValid.append(Mov.Up)
        if self.isValidPosition(self.downCord(coord)) and not self.existsInMemory(self.downCord(coord)):
            arrayValid.append(Mov.Down)
        if self.DiagonalMovs:
            if self.isValidPosition(self.upRightCord(coord)) and not self.existsInMemory(self.upRightCord(coord)):
                arrayValid.append(Mov.UpRight)
            if self.isValidPosition(self.upLeftCord(coord)) and not self.existsInMemory(self.upLeftCord(coord)):
                arrayValid.append(Mov.UpLeft)
            if self.isValidPosition(self.downRightCord(coord)) and not self.existsInMemory(self.downRightCord(coord)):
                arrayValid.append(Mov.DownRight)
            if self.isValidPosition(self.downLeftCord(coord)) and not self.existsInMemory(self.downLeftCord(coord)):
                arrayValid.append(Mov.DownLeft)
        """if (len(arrayValid) > 1):
            self.addToMemoryDecisions(coord)"""
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

    def __init__(self, Name, TypeAgent, InitalCords, FinalCords, PreFinalCords, stageText, AgentSensor=None,
                 AgentMovs=None,
                 Hide=False, DiagonalMovs=False, PriorMovements=[Mov.Left, Mov.Right, Mov.Up, Mov.Down]):
        global a
        self.Name = Name
        self.TypeAgent = TypeAgent
        self.PriorMovements = PriorMovements
        # Memory
        self.memoryCells = []
        # Memory Decisions
        self.memoryCellsDecisions = []
        # Optimal Camino
        self.optimalCamino = []

        MovsTerrainCosts.__init__(self, agent=TypeAgent)
        Stage.__init__(self, textPlain=stageText)
        if not self.isValidPosition(giveCords(InitalCords)):
            print(f"Error con Cordenadas iniciales")
            exit()
        elif not self.isValidPosition(giveCords(FinalCords)):
            print(f"Error con Cordenadas finales")
            exit()
        else:
            Movement.__init__(self, InitalCords=InitalCords, FinalCords=FinalCords, Hide=Hide,
                              DiagonalMovs=DiagonalMovs)
            self.addToMemory(giveCords(InitalCords))
            # if len(self.validRoads2()) > 1:
            #    self.addToMemoryDecisions(self.ActualCords)
            self.addStageLetras(self.InitialCords[0], self.InitialCords[1], "I")
            self.addStageLetras(self.FinalCords[0], self.FinalCords[1], "F")

            for x, preFinal in enumerate(PreFinalCords):
                if not self.isValidPosition(giveCords(preFinal)):
                    print(f"Error con Cordenadas de elementos extras")
                    exit()
                else:
                    tmp = giveCords(preFinal)
                    self.addStageLetras(tmp[0], tmp[1], "F" + str(x))
                    self.PreFinalCords = PreFinalCords

        ##### Auxiliares para algoritmos #######
        self.optiosnMemory = []
        self.auxiliarMemory = []
        self.CostMemory = []
        ############

    ######################

    def addToOptionsMemory(self, optionsPosition):
        if not self.optiosnMemory.__contains__(optionsPosition):
            self.optiosnMemory.append(optionsPosition)

    def deleteToOptionsMemory(self, scaned):
        for x, ContainOption in enumerate(self.optiosnMemory):
            if ContainOption.__contains__(scaned):
                ContainOption.remove(scaned)

    def scanCostAndEvaluation(self, coords, finalCords):
        distance = distanceManhatan(coords, finalCords)
        if not self.isValidPosition(coords):
            cost = None
        else:
            cost = self.giveCost(coords)
        if cost == 0 or cost is None:
            return None
        self.unHide(Coords=coords)
        self.addStageLetras(coords[0], coords[1], f"{distance + cost}")
        return distance + cost

    def giveOptimalOptions(self, options, FinalCords):
        print(f"Llego {options}")
        menorValues = []
        # validate Final
        for ContainOption in options:
            if ContainOption[1] == FinalCords:
                menorValues.append(ContainOption)
                return menorValues
        print("No es final")
        # First Value menor value Hipotesis
        menorValue = options[0]
        print(f"Valor de hipotesis{menorValue}")
        # Obtener el menor costo
        for ContainOption in options:
            if ContainOption[0] < menorValue[0]:
                menorValue = ContainOption
        print(f"Valor menor{menorValue}")
        # Dame los que tienen el menor valor
        for ContainOption in options:
            if ContainOption[0] == menorValue[0]:
                menorValues.append(ContainOption)
        print(f"arreglo de valores menores{menorValues}")
        return menorValues

    # busca coords en la memoria particular
    def existInMemory(self, memoryGeneral, coords):
        for memoryCamino in memoryGeneral:
            for x in memoryCamino:
                if memoryCamino[1] == coords:
                    return True
        return False

    def explorePosition(self, memoria, coords,finalCords):
        scaned = []
        #################################################################################
        x = self.scanCostAndEvaluation(self.upCord(coords),finalCords)
        if not x is None and not self.existInMemory(memoria, self.upCord(coords)):
            scaned.append((x, self.upCord(coords)))
        #################################################################################
        x = self.scanCostAndEvaluation(self.downCord(coords),finalCords)
        if not x is None and not self.existInMemory(memoria, self.downCord(coords)):
            scaned.append((x, self.downCord(coords)))
        #################################################################################
        x = self.scanCostAndEvaluation(self.leftCord(coords),finalCords)
        if not x is None and not self.existInMemory(memoria, self.leftCord(coords)):
            scaned.append((x, self.leftCord(coords)))
        #################################################################################
        x = self.scanCostAndEvaluation(self.rightCord(coords),finalCords)
        if not x is None and not self.existInMemory(memoria, self.rightCord(coords)):
            scaned.append((x, self.rightCord(coords)))
        return scaned

    def aEstrella(self, InicialPoint, FinalPoint):
        # [
        # [(Costo,coord,Acumulado),(Costo,coord,Acumulado)],
        # [(Costo,coord,Acumulado),(Costo,coord,Acumulado)]
        # ]
        memoriasDeCaminoYCostoYAcumulado = [[(0, InicialPoint, 0)]]
        print(memoriasDeCaminoYCostoYAcumulado)
        z = 0
        while True:
            print("=================================================================")
            print(f"j={z}")
            value = len(memoriasDeCaminoYCostoYAcumulado)
            if memoriasDeCaminoYCostoYAcumulado[0][len(memoriasDeCaminoYCostoYAcumulado[0])-1][1] == FinalPoint:
                print("Maze Solved!")
                print(f"Camino:{memoriasDeCaminoYCostoYAcumulado[0]}")
                print(f"Coste:{memoriasDeCaminoYCostoYAcumulado[0][len(memoriasDeCaminoYCostoYAcumulado[0])-1][2]}")
                break
            else:
                for j in range(0, value):
                    print("------------------------------------------------------------")
                    print(f"Explorando en memoria:{memoriasDeCaminoYCostoYAcumulado.__getitem__(j)}")
                    # Exploracion de los caminos en las ultimas coordenadas de cada camino
                    # Ultimo indice de memoeria
                    LastIndex = len(memoriasDeCaminoYCostoYAcumulado.__getitem__(j)) - 1
                    explorados = self.explorePosition(memoriasDeCaminoYCostoYAcumulado.__getitem__(j),
                                                      memoriasDeCaminoYCostoYAcumulado.__getitem__(j).__getitem__(
                                                          LastIndex)[1],
                                                      FinalPoint
                                                      )
                    print(f"Explorados:{explorados} de mem {j}")
                    # Optine los menos costosos
                    validRoads = self.giveOptimalOptions(explorados, FinalPoint)
                    print(f"MenosCostosos de los validos:{validRoads}  de mem {j}")
                    # Crea las copias
                    copyMem = memoriasDeCaminoYCostoYAcumulado.__getitem__(j)[::]  # Copia base
                    x = len(memoriasDeCaminoYCostoYAcumulado.__getitem__(j)) - 1
                    for i, Road in enumerate(validRoads):
                        # Copia del primero elemento
                        var = (Road[0], Road[1], copyMem[x][2] + Road[0])
                        if i == 0:
                            memoriasDeCaminoYCostoYAcumulado.__getitem__(j).append(var)
                        else:
                            copyyMem = copyMem[::]
                            copyyMem.append(var)
                            memoriasDeCaminoYCostoYAcumulado.append(copyyMem)

                # Limpiar los que no tengan el menor costo
                # Obtener el menor
                menorCostoAcumulado = memoriasDeCaminoYCostoYAcumulado[0][len(memoriasDeCaminoYCostoYAcumulado[0])-1][2]
                IndicesAEliminar=[]
                for i, mems in enumerate(memoriasDeCaminoYCostoYAcumulado):
                    if mems[len(mems)-1][2] < menorCostoAcumulado:
                        menorCostoAcumulado=mems[len(mems)-1][2]
                print(menorCostoAcumulado)
                # Obtener indices a eliminar (a escanear)
                for i, mems in enumerate(memoriasDeCaminoYCostoYAcumulado):
                    if mems[len(mems)-1][2] != menorCostoAcumulado:
                        IndicesAEliminar.append(i)
                # Borra de la memoria
                print(IndicesAEliminar)
                if not len(IndicesAEliminar) == 0:
                    indices=IndicesAEliminar.__reversed__()
                    print(f"Voy a borrar{indices}")
                    for i in indices:
                        memoriasDeCaminoYCostoYAcumulado.pop(i)
                    print(IndicesAEliminar)
                print(f"mem={memoriasDeCaminoYCostoYAcumulado}")
                z += 1
                self.updateStage()
            if z == 4:
                break

            # print(validRoads)
            # Creamos los caminos posibles
            # if validRoads != 1:
            #    for i in validRoads:
            #        memoriasDeCaminoYCostoYAcumulado.append(memoriasDeCaminoYCostoYAcumulado[::])

            # for memoriaDeCaminoYCostoYAcumulado in memoriasDeCaminoYCostoYAcumulado:
            #    validRoads = self.giveOptimalOptions(self.explorePosition(memoriaDeCaminoYCostoYAcumulado))

        ############################################################################################

    def depthFirstSearch(self, NodeByNode=False):
        if self.ActualCords == self.FinalCords:
            if NodeByNode:
                self.auxiliarMemory.append(self.ActualCords)
                self.memoryCells = self.auxiliarMemory
            print("Maze solved!")
            self.Optimal()
            return
        else:
            for j, Prior1 in enumerate(self.PriorMovements):
                find = False
                arrayValidRows = self.validRoads2()
                if NodeByNode and len(arrayValidRows) > 1:
                    self.auxiliarMemory.append(self.ActualCords)
                if len(arrayValidRows) == 0:
                    if NodeByNode:
                        self.auxiliarMemory.append(self.ActualCords)
                    # return to the last cell decision
                    LastCellDecision = self.memoryCellsDecisions.pop()
                    self.memoryCells.append(LastCellDecision)
                    self.ActualCords = LastCellDecision
                for i, validRoad in enumerate(arrayValidRows):
                    if Prior1 == validRoad:
                        find = True
                        if Mov.Right == validRoad:
                            self.movRight()
                        elif Mov.Left == validRoad:
                            self.movLeft()
                        elif Mov.Up == validRoad:
                            self.movUp()
                        elif Mov.Down == validRoad:
                            self.movDown()
                        self.depthFirstSearch(NodeByNode)
                        break
                if find:
                    break

    def Optimal(self):
        print("Optimal")
        self.optimalCamino = self.memoryCells[::]
        for i, x in enumerate(self.optimalCamino):
            for j in range(i + 1, len(self.optimalCamino) - 1):
                if self.optimalCamino[i] == self.optimalCamino[j]:
                    for x in range(i, j):
                        self.optimalCamino.pop(i)
                    break
        print(self.optimalCamino)

    def unHideActualPosition(self):
        self.unHide(self.ActualCords)
        self.unHide(self.upCord())
        self.unHide(self.downCord())
        self.unHide(self.leftCord())
        self.unHide(self.rightCord())

    def addToMemory(self, coords):
        if not self.existsInMemory(coords):
            self.memoryCells.append(coords)

    def existsInMemory(self, coords):
        return self.memoryCells.__contains__(coords)

    def addToMemoryDecisions(self, coords):
        if not self.existsInMemoryDecisions(coords):
            self.addStageLetras(coords[0], coords[1], "D")
            self.memoryCellsDecisions.append(coords)

    def existsInMemoryDecisions(self, coords):
        return self.memoryCellsDecisions.__contains__(coords)

    def isValidPosition(self, Coords):
        return 0 <= Coords[0] < len(self.stageLetras) and 0 <= Coords[1] < len(self.stageLetras[0]) \
               and self.giveCost(Coords) != 0

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
            self.ActualCords = destiny
            self.addStageLetras(self.ActualCords[0], self.ActualCords[1], "C")
            self.unHideActualPosition()
            self.updateStage()
            self.addToMemory(self.ActualCords)
            print(f"{self.ActualCords}.")
            self.numMovs += 1


def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words


def distanceManhatan(origen, end):
    return abs(end[0] - origen[0]) + abs(end[1] - origen[1])


def giveCords(tuplaNumLetter):
    return (tuplaNumLetter[0] - 1), (ord(tuplaNumLetter[1]) - 65)


def giveNumLetter(Coords):
    return (Coords[0] + 1), chr(Coords[1] + 65)


# Octopus    10,'B'
# Human      14,'C'
# Monkey     14,'E'
# PortalKey  15,'N'
# DarkTemple 7,'H'
# MagicStone 3,'O'
# Final      13,'D'


a = Stage(textPlain=readFile("../lab5.txt"))
# agent1 = Agent("Humano", TypeAgent.humano, InitalCords=(14, 'C'), FinalCords=(13, 'D'),
#               PreFinalCords=((15, 'N'), (7, 'H'), (3, 'O')), stageText=readFile("../lab5.txt"), Hide=False)
# agent2 = Agent("Mono", TypeAgent.mono, InitalCords=(14, 'E'), FinalCords=(13, 'D'),
#               PreFinalCords=((15, 'N'), (7, 'H'), (3, 'O')), stageText=readFile("../lab5.txt"), Hide=False)
# agent3 = Agent("Pulpo", TypeAgent.pulpo, InitalCords=(10, 'B'), FinalCords=(13, 'D'),
#               PreFinalCords=((15, 'N'), (7, 'H'), (3, 'O')), stageText=readFile("../lab5.txt"), Hide=False)
# CFA1 = agent1.proyecto()
# CFA2 = agent2.proyecto()
# CFA3 = agent3.proyecto()


agent1 = Agent("humano", TypeAgent.humano, InitalCords=(14, 'C'), FinalCords=(7, 'H'),
               PreFinalCords=((15, 'N'), (7, 'H'), (3, 'O')), stageText=readFile("../lab5.txt"), Hide=False)
InitalCords = (14, 'C')
FinalCords = (3, 'O')
agent1.aEstrella(giveCords(InitalCords), giveCords(FinalCords))

# for x in range(3):
#    print(CFA1[x], CFA2[x], CFA3[x])
#    if int(CFA1[x]) < int(CFA2[x]) and int(CFA1[x]) < int(CFA3[x]):

# print('El agente uno hara la mision: ', x)
# elif int(CFA2[x]) < int(CFA1[x]) and int(CFA2[x]) < int(CFA3[x]):

#    print('El agente dos hara la mision: ', x)
# elif int(CFA3[x]) < int(CFA1[x]) and int(CFA3[x]) < int(CFA1[x]):

#     print('El agente tres hara la mision: ', x)
