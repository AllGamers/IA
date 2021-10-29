__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 1"
__asginatura__ = "Inteligencia Artificial"

import os, sys, pygame, pygame_menu
from typing import Tuple

from LibsGameV3.MazeAgentV3 import *

import LibsGameV3.MazeAgentV3 as MA


class Player(object):
    global agent1, width, height, walls

    def __init__(self):
        self.rect = pygame.Rect(agent1.InitialCords[1] * 50, agent1.InitialCords[0] * 50, 50, 50)

    def move(self, dx, dy):
        if dx != 0 and dy == 0:
            return self.move_single_axis(dx, 0)
        if dy != 0 and dx == 0:
            return self.move_single_axis(0, dy)
        return self.move_diagonal_axis(dx, dy)

    def setPosition(self, x, y):
        self.rect.x = x
        self.rect.y = y
        pygame.image.load(agent1.Name + ".png")

    def move_single_axis(self, dx, dy):
        if 0 <= (self.rect.x + dx) <= (width - 50):
            if dx > 0:
                agent1.movRight()
            elif dx < 0:
                agent1.movLeft()
            self.rect.x += dx
        if 0 <= (self.rect.y + dy) <= (height - 50):
            if dy > 0:
                agent1.movDown()
            elif dy < 0:
                agent1.movUp()
            self.rect.y += dy
        self.collision(dx, dy)
        return pygame.image.load(agent1.Name + ".png")

    def move_diagonal_axis(self, dx, dy):
        if 0 <= (self.rect.x + dx) <= (width - 50) and 0 <= (self.rect.y + dy) <= (height - 50):
            if dx > 0 and dy > 0:
                agent1.movDownRight()
            elif 0 > dx and dy < 0:
                agent1.movUpLeft()
            elif dx > 0 > dy:
                agent1.movUpRight()
            elif dx < 0 < dy:
                agent1.movDownLeft()
            self.rect.x += dx
            self.rect.y += dy
        self.collision(dx, dy)
        return pygame.image.load(agent1.Name + ".png")

    def collision(self, dx, dy):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom


class Wall(object):
    global walls

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)


def initGame():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    global agent1, colorrgb, width, height, walls
    global IA
    global Name
    global TypeAgent
    global stageText
    global InitialCoord
    global FinalCords
    global Hide
    global PriorMovements
    global Algorithm
    global NodeByNode

    agent1 = Agent(Name, TypeAgent, InitalCords=InitialCoord, stageText=stageText, FinalCords=FinalCords, Hide=Hide,
                   PriorMovements=PriorMovements)

    if IA:
        if Algorithm == "DepthFirstSearch":
            agent1.depthFirstSearch(NodeByNode=NodeByNode)
        if Algorithm == "BreadthFirstSearch":
            agent1.breadthFirstSearch()

    colorrgb = agent1.GiveColor()

    pygame.display.set_caption("Laberinto - David Lopez Hernandez, Alejandro Escamilla Sanchez, Uriel Onofre Resendiz")
    width = len(agent1.stage) * 50
    height = len(agent1.stage[0]) * 50
    screen = pygame.display.set_mode((width, height))

    clock = pygame.time.Clock()
    walls = []
    player = Player()
    # Holds the level layout in a list of strings.
    level = agent1.stage
    # Parse the level string above. W = wall, E = exit
    final = agent1.FinalCords
    x = y = 0

    # Initialize
    for crow, row in enumerate(level):  # x
        for ccol, col in enumerate(row):  # y
            if not agent1.isValidPosition((ccol, crow)):
                Wall((crow * 50, ccol * 50))
            if crow == final[0] and ccol == final[1]:
                end_rect = pygame.Rect(ccol * 50, crow * 50, 50, 50)

    running = True
    back = pygame.image.load(agent1.Name + ".png")

    while running:

        # Here Selector IA OR HUMAN
        # Memoria del agente
        # Camino Optimo en base a la memoria
        if IA:
            for i, x in enumerate(agent1.memoryCells):
                clock.tick(3)
                print(x)
                player.setPosition(50 * x[1], 50 * x[0])
                # Draw the scene
                screen.blit(back, (0, 0))
                # for wall in walls:
                # pygame.draw.ellipse(screen, (255, 128, 64), wall.rect)
                pygame.draw.rect(screen, (255, 0, 0), end_rect)
                pygame.draw.rect(screen, colorrgb, player.rect)
                pygame.display.flip()
                pygame.display.update()
        else:

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False

                # Move the player if an KEYPAD key is pressed
                if e.type == pygame.KEYDOWN:
                    # valid out of bounds
                    if e.key == pygame.K_KP4:
                        back = player.move(-50, 0)
                    if e.key == pygame.K_KP6:
                        back = player.move(50, 0)
                    if e.key == pygame.K_KP2:
                        back = player.move(0, 50)
                    if e.key == pygame.K_KP8:
                        back = player.move(0, -50)
                    if agent1.DiagonalMovs:
                        if e.key == pygame.K_KP7:
                            back = player.move(-50, -50)
                        if e.key == pygame.K_KP9:
                            back = player.move(50, -50)
                        if e.key == pygame.K_KP3:
                            back = player.move(50, 50)
                        if e.key == pygame.K_KP1:
                            back = player.move(-50, 50)

        # Just added this to make it slightly fun ;)

        if player.rect.colliderect(end_rect):
            screen = pygame.display.set_mode((1200, 700))
            return

        # Draw the scene
        screen.blit(back, (0, 0))
        # for wall in walls:
        # pygame.draw.ellipse(screen, (255, 128, 64), wall.rect)
        pygame.draw.rect(screen, (255, 0, 0), end_rect)
        pygame.draw.rect(screen, colorrgb, player.rect)
        # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,128))
        pygame.display.flip()


def setAgent(value, NumValue):
    global TypeAgent
    assert isinstance(value, tuple)
    TypeAgent = MA.TypeAgent(NumValue)
    print(TypeAgent)
    pass


def disableButtons(value: Tuple, enabled: bool) -> None:
    global IA
    selectorAlgorithm = menu.get_widget('idAlgorithm')
    selectorMode = menu.get_widget('idMode')
    priorEntry = menu.get_widget('idPrior')
    assert isinstance(value, tuple)
    if enabled:
        IA = True
        selectorAlgorithm.show()
        selectorMode.show()
        priorEntry.show()
    else:
        IA = False
        selectorAlgorithm.hide()
        selectorMode.hide()
        priorEntry.hide()



def setHide(value: Tuple, enabled: bool) -> None:
    global Hide
    assert isinstance(value, tuple)
    if enabled:
        Hide = True
    else:
        Hide = False
    print(Hide)


def setAlgorithm(value: Tuple, enabled: bool) -> None:
    global Algorithm
    assert isinstance(value, tuple)
    if enabled:
        Hide = True
    else:
        Hide = False
    print(Hide)


def setMode(value: Tuple, enabled: bool) -> None:
    global NodeByNode
    assert isinstance(value, tuple)
    if enabled:
        NodeByNode = True
    else:
        NodeByNode = False
    print(Hide)


def MyTextValue(name):
    # on input change your value is returned here
    print('Player name is', name)
    if len(name) > 1:
        print(name[-1])
    return


def CastToCoordsInital(coords):
    # on input change your value is returned here
    print('Coords:', coords)
    Number = coords.split(",")[0]
    Letra = coords.split(",")[1]
    print(f"({Number},{Letra})")
    return


def CastToCoordsFinal(coords):
    # on input change your value is returned here
    print('Coords:', coords)
    Number = coords.split(",")[0]
    Letra = coords.split(",")[1]
    print(f"({Number},{Letra})")
    return Number, Letra


def start_the_game():
    user_agent = agent_name.get_value()
    if len(user_agent) > 10:
        agent_name.set_background_color((255, 0, 0))
        Error.set_title("Error: Longitud AgentName")
        Error.show()

    # rest of the game code


########### DEFAULT ######################
agent1 = None  # DEFAULT
IA = True  # DEFAULT
Name = "Name"  # DEFAULT
TypeAgent = TypeAgent.humano  # DEFAULT
stageText = readFile("lab1.txt")  # DEFAULT
InitialCoord = (10, 'A')
FinalCords = (2, 'O')
PriorMovements = [Mov.Up, Mov.Down, Mov.Left, Mov.Right]
Hide = True  # DEFAULT
Algorithm = "BreadthFirstSearch"  # DEFAULT
NodeByNode = True  # DEFAULT
########### DEFAULT ######################


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
surface = pygame.display.set_mode((1200, 700))

menu = pygame_menu.Menu('Welcome',
                        1200, 700,
                        theme=pygame_menu.themes.THEME_DARK)

# COMPONENTES #
############################################### GENERAL ##############################################
agent_name = menu.add.text_input('Agent Name :', default='Name', onchange=MyTextValue)
AgentType = menu.add.selector('AgentType', [('humano', 0), ('mono', 1), ('pulpo', 2), ('sasquatch', 3)],
                              onchange=setAgent)  #########
IA = menu.add.selector('IA:', [('IA', True), ('HUMAN', False)], onchange=disableButtons)  #########
menu.full_reset()
hide = menu.add.selector('Hide :', [('True', True), ('False', False)], onchange=setHide)  #########
file = menu.add.text_input('File:', default='lab1.txt')
InitialCoord = menu.add.text_input('InitialCoords:', default='10,A', onchange=CastToCoordsInital)
FinalCords = menu.add.text_input('FinalCoords:', default='2,O', onchange=CastToCoordsFinal)
############################################### IA ##############################################
Alogorithm = menu.add.selector('Algorithm :', [('BreadthFirstSearch', 1), ('DepthFirstSearch', 2)],
                               onchange=setAlgorithm, selector_id="idAlgorithm")
print(Alogorithm.get_id())
nodeOrStep = menu.add.selector('Node or Step :', [('NodeByNode', True), ('StepByStep', False)],
                               onchange=setMode, selector_id="idMode")  #########
Prior = menu.add.text_input('Prior:', default='xxx', textinput_id="idPrior")
############################################### IA ##############################################
Error = menu.add.label('Error', font_color=(255, 0, 0))
Error.hide()
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface, disable_loop=False, clear_surface=True)

"""
events = pygame.event.get()
# menu.render()
menu.update(events)
menu.draw(surface)

pygame.display.update()"""
