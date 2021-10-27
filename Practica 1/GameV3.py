__author__ = "David Lopez Hernandez"
__author__ = "Uriel Onofre Resendiz"
__author__ = "Alejandro Escamilla Sánchez"
__name__ = "Practica de laboratorio 1"
__asginatura__ = "Inteligencia Artificial"

import os, sys, pygame
import threading
import time

from LibsGameV3.MazeAgentV3 import *


class Player(object):

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

    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

agent1 = Agent("Human", TypeAgent.humano, InitalCords=(2, 'B'), stageText=readFile("lab1.txt"),
               FinalCords=(2, 'E'),
               Hide=True, PriorMovements=[Mov.Up, Mov.Down, Mov.Left, Mov.Right])

# agent1 = Agent("pulpo", TypeAgent.pulpo, InitalCords=(1, 'B'), stageText=readFile("lab2.txt"), FinalCords=(15, 'A'))
# agent1 = Agent("mono", TypeAgent.mono, InitalCords=(1, 'B'), stageText=readFile("lab2.txt"), FinalCords=(15, 'A'))
# agent1 = Agent("sasquatch", TypeAgent.sasquatch, InitalCords=(1, 'B'), stageText=readFile("lab2.txt"), FinalCords=(15, 'A'))

IA = True
if IA:
    agent1.depthFirstSearch()

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


def IAControl(x):
    player.setPosition(50 * x[1], 50 * x[0])
    time.sleep(500)


# Here Selector IA OR HUMAN
# Memoria del agente
# Camino Optimo en base a la memoria
if IA:
    for i, x in enumerate(agent1.memoryCells):
        clock.tick(1)
        print(x)
        player.setPosition(50 * x[1], 50 * x[0])
        # Draw the scene
        screen.blit(back, (0, 0))
        # for wall in walls:
        pygame.draw.rect(screen, (255, 0, 0), end_rect)
        pygame.draw.rect(screen, colorrgb, player.rect)
        pygame.display.flip()
        pygame.display.update()
else:
    while running:

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
            pygame.quit()
            sys.exit()

        # Draw the scene
        screen.blit(back, (0, 0))
        # for wall in walls:
        # pygame.draw.ellipse(screen, (255, 128, 64), wall.rect)
        pygame.draw.rect(screen, (255, 0, 0), end_rect)
        pygame.draw.rect(screen, colorrgb, player.rect)
        # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,128))
        pygame.display.flip()

pygame.quit()
