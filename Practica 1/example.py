import os
import sys
import pygame
from Image import *

agent1 = Agent("A2", TypeAgent.humano, InitalCords=(2, 'B'), stageText=readFile("lab2.txt"),FinalCords=(3, 'B'))
class Player(object):
 
    def __init__(self):
        self.rect = pygame.Rect(agent1.InitialCords[0]*50, agent1.InitialCords[1]*50, 50, 50)
 
    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
 
    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.collision(dx, dy)
 
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
 
 
pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((750, 750))
 
clock = pygame.time.Clock()
walls = []
player = Player()
 
# Holds the level layout in a list of strings.

level = agent1.Stage.stage
# Parse the level string above. W = wall, E = exit

final = agent1.FinalCords
x = y = 0
for crow, row in enumerate(level):
    for ccol, col in enumerate(row):
        if col == 0:
            Wall((x, y))
        elif crow == final[0] and ccol == final[1]:
            end_rect = pygame.Rect(crow*50, ccol*50, 50, 50)
        x += 50
    y += 50
    x = 0

running = True
back = pygame.image.load(agent1.Name+".png")
while running:
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
        # Move the player if an arrow key is pressed
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                player.move(-50, 0)
            if e.key == pygame.K_RIGHT:
                player.move(50, 0)
            if e.key == pygame.K_UP:
                player.move(0, -50)
            if e.key == pygame.K_DOWN:
                player.move(0, 50)

    if player.rect.colliderect(end_rect):
        pygame.quit()
        sys.exit() 
    
    # Draw the scene
    screen.blit(back, (0, 0))
    pygame.draw.rect(screen, (255, 255, 0), end_rect)
    pygame.draw.rect(screen, (255, 80, 0), player.rect)
    pygame.display.flip()
    #clock.tick(120)
    
pygame.quit()