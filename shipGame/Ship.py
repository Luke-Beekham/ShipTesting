import pygame
import math
import os

pygame.init()

pygame.display.set_caption("Ship")

current_file_path = __file__

# Get the directory containing the current file

class BackEnd:
    def __init__(self):
        self.width: int = 1300
        self.height = 650
        self.win = pygame.display.set_mode((self.width, self.height))
        self.run = True
        self.current_dir = os.path.dirname(current_file_path)
        self.image_Folder = self.current_dir + "\Images"
        self.imageList = []
    def LoadImages(self):
        Ship = pygame.image.load(self.image_Folder + "\Ship.png").convert_alpha()
        MachineSoulEnemy1 = pygame.image.load(self.image_Folder + "\MachineSoulEnemy1.png").convert_alpha()
        self.imageList = {
            "Ship" : Ship,
            "MachineSoulEnemy1" : MachineSoulEnemy1
        }
        return self.imageList

Game = BackEnd()

Game.LoadImages()

Game.imageList = Game.LoadImages()


class Entity():

    def Draw(self,image,x,y):
        Game.win.blit(image, (x - int(image.get_width() / 2), y - int(image.get_height() / 2)))

    def Move(self,x,y,angle,vel): 
        
        x += vel * math.cos(math.radians(angle))
        y += vel * math.sin(math.radians(angle))

        return x,y
    
    def Rotate(self,orginalImage,angle):
        newImage = pygame.transform.rotate(orginalImage, -angle)
        return newImage
    
    def FollowAngle(self,x,y,targetX,targetY):
        angle = math.atan2(targetY - y, targetX - x)
        angle = math.degrees(angle)
        return angle
    

    

    
Entity = Entity()



class Enemy:
    def __init__(self,x,y,width,height,type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 0.1
        self.angle = 0
        self.type = type
        self.orginalImage = Game.imageList[type]
        self.image = Game.imageList[type]
    
    def Draw(self):
        Entity.Draw(self.image,self.x,self.y)
    
    def Move(self):
        self.x,self.y = Entity.Move(self.x,self.y,self.angle,self.vel)
    
    def Rotate(self):
        self.image = Entity.Rotate(self.orginalImage,self.angle)
    
    def Update(self):
        
        self.angle = Entity.FollowAngle(self.x,self.y,plr.x,plr.y)
        self.Rotate()
        self.Move()

class Ship:
    originalShipImage = Game.imageList["Ship"]
    shipImage = originalShipImage.copy()
    shipImage = pygame.transform.scale(shipImage, (128, 128))
    originalScaledShipImage = shipImage.copy()
    
    def __init__(self):
        self.x = 50
        self.y = 50
        self.width = 50
        self.height = 50
        self.vel = 0
        self.color = (0, 255, 0)
        self.angle = 0

    def Draw(self, win):
        Entity.Draw(Ship.shipImage, self.x, self.y)

    def Rotate(self, angle):
        Ship.shipImage = Entity.Rotate(Ship.originalScaledShipImage, angle)

    def Move(self,vel): 
        self.x,self.y = Entity.Move(self.x,self.y,self.angle,vel)


plr = Ship()
Enemy1 = Enemy(100,100,50,50,"MachineSoulEnemy1")
while Game.run:
    Game.win.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        plr.angle -= 0.5
        plr.Rotate(plr.angle)
    if keys[pygame.K_d]:
        plr.angle += 0.5
        plr.Rotate(plr.angle)
    if keys[pygame.K_w]:
        plr.Move(0.75)
    if keys[pygame.K_s]:
        plr.Move(-0.75)

    Enemy1.Update()
    Enemy1.Draw()
    plr.Draw(Game.win)
    pygame.display.update()
        
    

pygame.quit()