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
        self.music_Folder = self.current_dir + "\Music"
        self.imageList = []
    def LoadImages(self):
        Ship = pygame.image.load(self.image_Folder + "\Ship.png").convert_alpha()
        MachineSoulEnemy1 = pygame.image.load(self.image_Folder + "\MachineSoulEnemy1.png").convert_alpha()
        MachineSoulEnemy2 = pygame.image.load(self.image_Folder + "\MachineSoulEnemy2.png").convert_alpha()
        ShipLazer = pygame.image.load(self.image_Folder + "\ShipLazer.png").convert_alpha()
        EnemyLazer = pygame.image.load(self.image_Folder + "\EnemyLazer.png").convert_alpha()
        TargetCursor = pygame.image.load(self.image_Folder + "\TargetCursor.png").convert_alpha()
        self.imageList = {
            "Ship" : Ship,
            "MachineSoulEnemy1" : MachineSoulEnemy1,
            "MachineSoulEnemy2" : MachineSoulEnemy2,
            "ShipLazer" : ShipLazer,
            "EnemyLazer" : EnemyLazer,
            "TargetCursor" : TargetCursor,
            
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
    @staticmethod
    def Draw(image,x,y):
        Game.win.blit(image, (x - int(image.get_width() / 2), y - int(image.get_height() / 2)))

    @staticmethod
    def Move(x,y,angle,vel): 
        
        x += vel * math.cos(math.radians(angle))
        y += vel * math.sin(math.radians(angle))

        return x,y
    
    @staticmethod
    def Rotate(orginalImage,angle):
        newImage = pygame.transform.rotate(orginalImage, -angle)
        return newImage
    
    @staticmethod
    def FollowAngle(x,y,targetX,targetY):
        angle = math.atan2(targetY - y, targetX - x)
        angle = math.degrees(angle)
        return angle
    


    
    
Entity = Entity()


class Lazer:
    EnemyLazerImg = Game.imageList["EnemyLazer"].copy()
    EnemyLazerImg = pygame.transform.scale(EnemyLazerImg, (10, 10))

    ShipLazerImg = Game.imageList["ShipLazer"].copy()
    ShipLazerImg = pygame.transform.scale(ShipLazerImg, (10, 10))

    LazerList = []

    def __init__(self,x,y,angle,vel,type):
        self.Initalx = x
        self.Intialy = y
        self.angle = angle
        self.vel = vel

        if type == "Enemy":
            img = Lazer.EnemyLazerImg.copy()
        elif type == "Ship":
            img = Lazer.ShipLazerImg.copy()
        else:
            print("NO TYPE FOR LAZER!!")
        self.image = img
        self.rect = img.get_rect()
        self.rect.center = (x, y)  # Set the center of the rect to the initial position of the laser
        self.mask = pygame.mask.from_surface(img)
        self.type = type
        Lazer.LazerList.append(self)

    def Draw(self):
        Entity.Draw(self.image,self.rect.x,self.rect.y)
    
    def Move(self):
        self.rect.x,self.rect.y = Entity.Move(self.rect.x,self.rect.y,self.angle,self.vel)
    
    def Remove(self):
        Lazer.LazerList.remove(self)
    
    def IsMaskOverlap(self,mask,rect):
        x = rect.x
        y = rect.y

        # Correct the offset calculation for mask overlap

        offset_x = x - int(self.rect.x - self.image.get_width() / 2)
        offset_y = y - int(self.rect.y - self.image.get_height() / 2)
        if self.mask.overlap(mask, (offset_x, offset_y)):
            return True
        return False
    
    def Update(self):
        self.Move()
        self.Draw()
        if self.rect.x < 0 or self.rect.x > Game.width or self.rect.y < 0 or self.rect.y > Game.height:
            self.Remove()
            return
        
        if self.type == "Ship":
            for enemy in Enemy.EnemyList:
                # Correct the offset calculation for mask overlap
                offset_x = self.rect.x - int(enemy.x - enemy.image.get_width() / 2)
                offset_y = self.rect.y - int(enemy.y - enemy.image.get_height() / 2)
                if enemy.mask.overlap(self.mask, (offset_x, offset_y)):
                    Enemy.EnemyList.remove(enemy)
                    self.Remove()
                    break
        elif self.type == "Enemy":
            if self.IsMaskOverlap(plr.mask,plr.rect):
                plr.ChangeHealth(-10)
                self.Remove()
    
    @classmethod
    def UpdateLazers(cls):
        for Lazer in cls.LazerList:
            Lazer.Update()

class Enemy:
    EnemyList = []
    EnemyTimer = Game.CreateTimer(5000)
    EnemyFireTimer = Game.CreateTimer(3000)

    Lazer = Game.imageList["EnemyLazer"].copy()
    Lazer = pygame.transform.scale(Lazer, (10, 10))
    
    
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.vel = 2
        self.angle = 0
        self.type = type
        self.orginalImage = Game.imageList[type]
        self.image = Game.imageList[type]
        self.mask = pygame.mask.from_surface(self.image)
        self.LazerList = []
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
    
    def IsMaskOverlap(self,mask,rect):        
        x = rect.x
        y = rect.y

        # Correct the offset calculation for mask overlap

        offset_x = x - int(self.x - self.image.get_width() / 2)
        offset_y = y - int(self.y - self.image.get_height() / 2)
        if self.mask.overlap(mask, (offset_x, offset_y)):
            return True
        return False
    
    def ShootLazers(self):
        NewLazer = Lazer(self.x,self.y,self.angle,5,"Enemy")
    def Update(self):
        if self.type == "MachineSoulEnemy1":
            self.angle = Entity.FollowAngle(self.x,self.y,plr.x,plr.y)
            self.Rotate()
            self.Move()
            if self.IsMaskOverlap(plr.mask,plr.rect):
                plr.ChangeHealth(-1)
        elif self.type == "MachineSoulEnemy2":
            self.angle = Entity.FollowAngle(self.x,self.y,plr.x,plr.y)
            self.Rotate()
            if math.dist((self.x,self.y),(plr.x,plr.y)) >= 300:
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
        self.health = 100
        self.healthBarBackground = Drawing(25,100,50,120,(0,0,0),(130, 127, 128),"rect")
        self.healthBar = Drawing(37.5,112.5,25,100,(255,255,255),(255,0,0),"rect")
        self.mask = pygame.mask.from_surface(self.shipImage)
        self.rect = self.shipImage.get_rect()
        self.rect.center = (self.x, self.y)  
    def Draw(self):
        Entity.Draw(Ship.shipImage, self.x, self.y)
        self.rect.center = (self.x, self.y)

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
        
        angle = Entity.FollowAngle(self.x,self.y,Target.x,Target.y)
        NewLazer = Lazer(self.x,self.y,angle,20,"Ship")

        self.LazersFired += 1
        self.LazerHeatBar.width = 100 - (self.LazersFired) 
        
        self.LazerHeatBar.draw()
        if not Ship.shipLazerSound.Channel.get_busy():
            Ship.shipLazerSound.play()
        else:
            Game.ReStartTimer(Ship.shipLazerSoundTimer,50)
    
    def ChangeHealth(self,health):
        self.health += health
        if self.health <= 0:
            print("You Died")
        if self.health > 100:
            self.health = 100
        self.healthBar.height = self.health 
        self.healthBar.draw()
        self.healthBarBackground.draw()
    def Update(self):
        self.Draw()
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
            randomNum = random.randint(0,1)
            if randomNum == 0:
                Enemy.createEnemy("MachineSoulEnemy2")
            else:
                Enemy.createEnemy("MachineSoulEnemy1")
        if event.type == Ship.shipLazerSoundTimer:
            Ship.shipLazerSound.play()
            Game.StopTimer(Ship.shipLazerSoundTimer)
        if event.type == Enemy.EnemyFireTimer:
            for enemy in Enemy.EnemyList:
                if enemy.type == "MachineSoulEnemy2":
                    enemy.ShootLazers()

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
    Lazer.UpdateLazers()
    pygame.display.update()
        
    clock.tick(60)

pygame.quit()