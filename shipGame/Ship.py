import pygame
import math
import os
import random

pygame.init()

pygame.display.set_caption("Ship")

current_file_path = __file__

pygame.mixer.init()

pygame.mixer.set_num_channels(8) 




# Get the directory containing the current file

class BackEnd:
    def __init__(self):
        self.width: int = 1300
        self.height = 650
        self.win = pygame.display.set_mode((self.width, self.height))
        self.run = True
        self.current_dir = os.path.dirname(current_file_path)
        self.image_Folder = self.current_dir + "\Images"
        self.sound_Folder = self.current_dir + "\Sounds"
        print(self.sound_Folder)
        self.music_Folder = self.current_dir + "\Music"
        self.imageList = []
    def LoadImages(self):
        Ship = pygame.image.load(self.image_Folder + "\Ship.png").convert_alpha()
        MachineSoulEnemy1 = pygame.image.load(self.image_Folder + "\MachineSoulEnemy1.png").convert_alpha()
        ShipLazer = pygame.image.load(self.image_Folder + "\ShipLazer.png").convert_alpha()
        EnemyLazer = pygame.image.load(self.image_Folder + "\EnemyLazer.png").convert_alpha()
        TargetCursor = pygame.image.load(self.image_Folder + "\TargetCursor.png").convert_alpha()
        self.imageList = {
            "Ship" : Ship,
            "MachineSoulEnemy1" : MachineSoulEnemy1,
            "ShipLazer" : ShipLazer,
            "EnemyLazer" : EnemyLazer,
            "TargetCursor" : TargetCursor
            
            
        }
        return self.imageList
    def CreateTimer(self,millSeconds):
        Timer = pygame.event.custom_type()
        pygame.time.set_timer(Timer, millSeconds)
        return Timer
    def StopTimer(self,Timer):
        pygame.time.set_timer(Timer, 0)
    def ReStartTimer(self,Timer,millSeconds):
        pygame.time.set_timer(Timer, millSeconds)

Game = BackEnd()

Game.LoadImages()

Game.imageList = Game.LoadImages()

class Music:
    def __init__(self, music,vol):
        self.music = music
        self.vol = vol
        self.played = False
        self.lastPlayedTime = 0

    def play(self,currentTime):    
        if not self.played or (currentTime - self.lastPlayedTime > self.playedTime):
            pygame.mixer.init()
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.set_volume(self.vol)
            pygame.mixer.music.play()

            self.played = True
            self.lastPlayedTime = currentTime
    def stop(self):
        if self.played:
            pygame.mixer.music.stop() 
            self.played = False

class Sound:
    Channel = -1
    def __init__(self, sound,vol):
        self.sound = pygame.mixer.Sound(sound)
        self.vol = self.sound.set_volume(vol)
        self.length = self.sound.get_length()
        self.played = False
        self.lastPlayedTime = 0
        if Sound.Channel >= 8:
            print("Sound Channel Limit Reached")
            Sound.Channel = 0
        else:
            Sound.Channel += 1

        self.Channel = pygame.mixer.Channel(Sound.Channel)
        

    def play(self):
        currentTime = pygame.time.get_ticks()
        # if not self.played or (currentTime - self.lastPlayedTime > self.playedTime):
        self.Channel.play(self.sound)
        self.played = True
        self.lastPlayedTime = currentTime
    def stop(self):
        if self.played:
            self.sound.stop()
            self.played = False

class Entity:

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
    
    def ShootLazers(self, x, y, angle, vel, img):
        rect = img.get_rect()
        rect.center = (x, y)  # Set the center of the rect to the initial position of the laser

        mask = pygame.mask.from_surface(img)

        self.Draw(img, rect.x, rect.y)
        return rect, mask
    
    def UpdateLazers(self, vel, img, angle, rect):
        rect.x += vel * math.cos(math.radians(angle))
        rect.y += vel * math.sin(math.radians(angle))

        if rect.right < 0 or rect.left > Game.width or rect.bottom < 0 or rect.top > Game.height:
            return False
        else:
            self.Draw(img, rect.centerx, rect.centery)  # Use the center of the rect for drawing
            return True

    
    
    
Entity = Entity()



class Enemy:
    EnemyList = []
    EnemyTimer = Game.CreateTimer(5000)
    
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.vel = 2
        self.angle = 0
        self.type = type
        self.orginalImage = Game.imageList[type]
        self.image = Game.imageList[type]
        self.mask = pygame.mask.from_surface(self.image)
        Enemy.EnemyList.append(self)

    def createEnemy(type):
        TopOrSide = random.randint(0,1)
        if TopOrSide == 0:
            x = random.randint(0,Game.width)
            y = 0
        else:
            x = 0
            y = random.randint(0,Game.height)
        Enemy1 = Enemy(x,y,type)
        
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
        self.Draw()
    
    @classmethod
    def UpdateEnemies(cls):
        for enemy in cls.EnemyList:
            enemy.Update()


class Ship:
    originalShipImage = Game.imageList["Ship"]
    shipImage = originalShipImage.copy()
    shipImage = pygame.transform.scale(shipImage, (128, 128))
    originalScaledShipImage = shipImage.copy()

    shipLazer = Game.imageList["ShipLazer"]
    shipLazer = pygame.transform.scale(shipLazer, (10, 10))

    shipLazerSound = Sound(Game.sound_Folder + "/ShipLazerSound.wav",0.5)

    shipLazerSoundTimer = Game.CreateTimer(100)
    Game.StopTimer(shipLazerSoundTimer)    
    
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
        angle = Entity.FollowAngle(self.x,self.y,Target.x,Target.y)
        rect,mask = Entity.ShootLazers(self.x,self.y,angle,10,NewLazer)
        self.LazerList.append((NewLazer,angle,rect,mask))

        self.LazersFired += 1
        self.LazerHeatBar.width = 100 - (self.LazersFired) 
        
        self.LazerHeatBar.draw()
        if not Ship.shipLazerSound.Channel.get_busy():
            Ship.shipLazerSound.play()
        else:
            Game.ReStartTimer(Ship.shipLazerSoundTimer,50)
    def Update(self):
        self.Draw()
        for tuple in self.LazerList:
            lazer = tuple[0]
            angle = tuple[1]
            rect = tuple[2]
            mask = tuple[3]


            # Access the coordinates
            x = rect.x
            y = rect.y

            for enemy in Enemy.EnemyList:
                # Correct the offset calculation for mask overlap
                offset_x = x - int(enemy.x - enemy.image.get_width() / 2)
                offset_y = y - int(enemy.y - enemy.image.get_height() / 2)
                if enemy.mask.overlap(mask, (offset_x, offset_y)):
                    Enemy.EnemyList.remove(enemy)
                    self.LazerList.remove(tuple)
                    break
            if not(Entity.UpdateLazers(20,lazer,angle,rect)):
                if tuple in self.LazerList:
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
        

class TargetCursor:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = Game.imageList["TargetCursor"]
        self.mask = pygame.mask.from_surface(self.image)

    def Draw(self):
        Entity.Draw(self.image,self.x,self.y)

    def Update(self):
        self.x = pygame.mouse.get_pos()[0] 
        self.y = pygame.mouse.get_pos()[1] 
        self.Draw()

plr = Ship()
Enemy1 = Enemy(100,100,"MachineSoulEnemy1")
clock = pygame.time.Clock()

Target = TargetCursor(0,0)
pygame.mouse.set_visible(False)

while Game.run:
    Game.win.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == Enemy.EnemyTimer:
            Enemy.createEnemy("MachineSoulEnemy1")
        if event.type == Ship.shipLazerSoundTimer:
            Ship.shipLazerSound.play()
            Game.StopTimer(Ship.shipLazerSoundTimer)

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
    
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        plr.ShootLazer()

    Enemy.UpdateEnemies()
    plr.Update()
    Drawing.UpdateDrawings()
    Target.Update()
    pygame.display.update()
        
    clock.tick(60)

pygame.quit()