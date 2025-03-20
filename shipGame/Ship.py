import pygame
import math
import os

pygame.init()

pygame.display.set_caption("Ship")

current_file_path = __file__

# Get the directory containing the current file

class Game:
    def __init__(self):
        self.width = 1300
        self.height = 650
        self.win = pygame.display.set_mode((self.width, self.height))
        self.run = True
        self.current_dir = os.path.dirname(current_file_path)
        print(self.current_dir)

Game = Game()

class Ship:

    originalShipImage = pygame.image.load(Game.current_dir + "\Ship.png").convert_alpha()
    originalScaledShipImage = pygame.transform.scale(originalShipImage, (128, 128))
    shipImage = pygame.image.load(Game.current_dir + "\Ship.png").convert_alpha()
    shipImage = pygame.transform.scale(shipImage, (128, 128))
    
    def __init__(self):
        self.x = 50
        self.y = 50
        self.width = 50
        self.height = 50
        self.vel = 0
        self.color = (0, 255, 0)
        self.angle = 0
        self.points = [(300, 100), (300, 200), (200, 200)]

    def draw(self, win):
        win.blit(Ship.shipImage, (self.x - int(Ship.shipImage.get_width() / 2), self.y - int(Ship.shipImage.get_height() / 2)))

    def Rotate(self, angle):
        Ship.shipImage = pygame.transform.rotate(Ship.originalScaledShipImage, -angle)

    def Move(self,vel): 
        self.vel = vel 
        
        self.x += self.vel * math.cos(math.radians(self.angle))
        self.y += self.vel * math.sin(math.radians(self.angle))


plr = Ship()

while Game.run:
    Game.win.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        plr.angle += 1
        plr.Rotate(plr.angle)
    if keys[pygame.K_RIGHT]:
        plr.angle -= 1
        plr.Rotate(plr.angle)
    if keys[pygame.K_UP]:
        plr.Move(1)
    if keys[pygame.K_DOWN]:
        plr.Move(-1)
    plr.draw(Game.win)
    pygame.display.update()
        
    print(plr.angle)
    

pygame.quit()