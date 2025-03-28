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
        ShipLazer = pygame.image.load(self.image_Folder + "\ShipLazer.png").convert_alpha()
        EnemyLazer = pygame.image.load(self.image_Folder + "\EnemyLazer.png").convert_alpha()
        self.imageList = {
            "Ship" : Ship,
            "MachineSoulEnemy1" : MachineSoulEnemy1,
            "ShipLazer" : ShipLazer,
            "EnemyLazer" : EnemyLazer
            
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
    
    def ShootLazers(self,x,y,angle,vel,img):
        rect = img.get_rect()

        

        rect.x = x
        rect.y = y



        img_x = rect.x
        img_y = rect.y
        img_x += vel * math.cos(math.radians(angle))
        img_y += vel * math.sin(math.radians(angle))

        img_x = rect.x
        img_y = rect.y

        self.Draw(img,img_x,img_y)
        return rect
    
    def UpdateLazers(self,vel,img,angle,rect):
        
        rect.x += vel * math.cos(math.radians(angle))
        rect.y += vel * math.sin(math.radians(angle))

        if rect.x > Game.width or rect.x < 0 or rect.y > Game.height or rect.y < 0:
            return False
        else:
            self.Draw(img,rect.x,rect.y)
            return True

    
    
    

    
Entity = Entity()



class Enemy:
    def __init__(self,x,y,width,height,type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 2
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

    shipLazer = Game.imageList["ShipLazer"]
    shipLazer = pygame.transform.scale(shipLazer, (10, 10))
    
    
    def __init__(self):
        self.x = Game.width / 2
        self.y = Game.height / 2
        self.width = 50
        self.height = 50
        self.vel = 5
        self.color = (0, 255, 0)
        self.angle = 0
        self.LazerList = []
        self.LazerHeatBackground = Drawing(25,25,120,50,(0,0,0),(0,0,0),"rect")
        self.LazerHeatBar = Drawing(37.5,37.5,100,25,(0,255,0),(0,255,0),"rect")
        self.LazersFired = 0
        self.LazerCooldown = False


    def Draw(self):
        Entity.Draw(Ship.shipImage, self.x, self.y)

    def Rotate(self, angle):
        Ship.shipImage = Entity.Rotate(Ship.originalScaledShipImage, angle)

    def Move(self,direction):
        vel = direction * self.vel 
        self.x,self.y = Entity.Move(self.x,self.y,self.angle,vel)
    
    def ShootLazer(self):
        if self.LazersFired >= 100:
            self.LazerCooldown = True
        
        if self.LazerCooldown:
            self.LazerHeatBar.color = (255,0,0)
            self.LazerHeatBar.fillColor = (255,0,0)

            return
        
        NewLazer = self.shipLazer.copy()

        rect = Entity.ShootLazers(self.x,self.y,self.angle,10,NewLazer)
        self.LazerList.append((NewLazer,self.angle,rect))

        self.LazersFired += 1
        self.LazerHeatBar.width = 100 - (self.LazersFired) 
        
        self.LazerHeatBar.draw()
    
    def Update(self):
        self.Draw()
        for tuple in self.LazerList:
            lazer = tuple[0]
            angle = tuple[1]
            rect = tuple[2]


            # Access the coordinates
            x = rect.x
            y = rect.y

            if not(Entity.UpdateLazers(20,lazer,angle,rect)):
                self.LazerList.remove(tuple)
        if self.LazersFired > 0:
            self.LazersFired -= 0.1
            self.LazerHeatBar.width = 100 - (self.LazersFired) 
            self.LazerHeatBar.draw()
        
        if self.LazersFired <= 0 and self.LazerCooldown:
                self.LazerCooldown = False
                self.LazersFired = 0
                self.LazerHeatBar.color = (0,255,0)
                self.LazerHeatBar.fillColor = (0,255,0)
                self.LazerHeatBar.draw()


class Drawing:
    drawingList = []
    def __init__(self,x,y,width,height,color,fillcolor,type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        if fillcolor == None:
            self.fillColor = None
        self.fillColor = fillcolor
        self.type = type



        Drawing.drawingList.append(self)

    def MakeSurface(self):
        if self.type == "rect":
            rect_surface = pygame.Surface((self.width, self.height)) 
            if self.fillColor != None:
                rect_surface.fill(self.fillColor) 
        self.surface = rect_surface

    def draw(self):
        if self.type == "rect":
            self.MakeSurface()
            Game.win.blit(self.surface, (self.x, self.y))

    @classmethod
    def UpdateDrawings(cls):
        for drawing in cls.drawingList:
            drawing.draw()    
        

plr = Ship()
Enemy1 = Enemy(100,100,50,50,"MachineSoulEnemy1")
clock = pygame.time.Clock()
while Game.run:
    Game.win.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        plr.angle -= 5
        plr.Rotate(plr.angle)
    if keys[pygame.K_d]:
        plr.angle += 5
        plr.Rotate(plr.angle)
    if keys[pygame.K_w]:
        plr.Move(1)
    if keys[pygame.K_s]:
        plr.Move(-1)
    if keys[pygame.K_SPACE]:
        plr.ShootLazer()

    Enemy1.Update()
    Enemy1.Draw()
    plr.Update()
    Drawing.UpdateDrawings()
    pygame.display.update()
        
    clock.tick(60)

pygame.quit()