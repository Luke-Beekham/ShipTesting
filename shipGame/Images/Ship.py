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
        self.wave = 0
        self.WaveImageTimer = self.CreateTimer(5000)
        self.StopTimer(self.WaveImageTimer)
        self.WaveImage = None
        self.isWaveImage = False
        self.WaveTimer = self.CreateTimer(20000)
        self.StopTimer(self.WaveTimer)
        self.wave1List = ["1","1","1","1","1","1","1","1","1","1"]
        self.wave2List = ["2","1","2","1","2","2","2","2","1","1","2","1","2","1","2","1","2","1","2","1"]
        self.wave3List = ["3","2","1","2","3","2","1","1","1","1","2","1","2","1","2","1","2","1","2","1","1","1","2","1","2","1","2","1","2","1","3","3"]
        self.wave4List = ["4","3","2","1","2","3","4","4","2", "1","4","1","4","3","2","1","2","3","4","4" ,"2", "1","4","1","4","4","2","1","2","3","4","4" ,"2", "1","4","1","4" ,"2", "1","4","1"]
        self.wave5List = ["4","3","2","1","2","3","4","4","2", "1","4","1","4","3","2","1","2","3","4","4" ,"2", "1","4","1","4","4","2","1","2","3","4","4" ,"2", "1","4","1","4" ,"2", "1","4","1","3","3","2","1","4","2","1","2","4","4"]

        self.wave1List = random.sample(self.wave1List, len(self.wave1List))
        self.wave2List = random.sample(self.wave2List, len(self.wave2List))
        self.wave3List = random.sample(self.wave3List, len(self.wave3List))
        self.wave4List = random.sample(self.wave4List, len(self.wave4List))
        self.wave5List = random.sample(self.wave5List, len(self.wave5List))

        self.isMainMenu = True



    def LoadImages(self):
        Ship = pygame.image.load(self.image_Folder + "\Ship.png").convert_alpha()
        MachineSoulEnemy1 = pygame.image.load(self.image_Folder + "\MachineSoulEnemy1.png").convert_alpha()
        MachineSoulEnemy2 = pygame.image.load(self.image_Folder + "\MachineSoulEnemy2.png").convert_alpha()
        MachineSoulEnemy3 = pygame.image.load(self.image_Folder + "\MachineSoulEnemy3.png").convert_alpha()
        MachineSoulEnemy4 = pygame.image.load(self.image_Folder + "\MachineSoulEnemy4.png").convert_alpha()
        ShipLazer = pygame.image.load(self.image_Folder + "\ShipLazer.png").convert_alpha()
        EnemyLazer = pygame.image.load(self.image_Folder + "\EnemyLazer.png").convert_alpha()
        TargetCursor = pygame.image.load(self.image_Folder + "\TargetCursor.png").convert_alpha()
        Map = pygame.image.load(self.image_Folder + "\Map.png").convert()
        Wave1 = pygame.image.load(self.image_Folder + "\WAVEONE.png").convert_alpha()
        Wave2 = pygame.image.load(self.image_Folder + "\WAVETWO.png").convert_alpha()
        Wave3 = pygame.image.load(self.image_Folder + "\WAVETHREE.png").convert_alpha()
        Wave4 = pygame.image.load(self.image_Folder + "\WAVEFOUR.png").convert_alpha()
        Wave5 = pygame.image.load(self.image_Folder + "\WAVEFIVE.png").convert_alpha()
        MissionComplete = pygame.image.load(self.image_Folder + "\MissionComplete.png").convert_alpha()
        MissionFailed = pygame.image.load(self.image_Folder + "\MissionFailed.png").convert_alpha()
        ShipDied = pygame.image.load(self.image_Folder + "\ShipDied.png").convert_alpha()
        Respawn = pygame.image.load(self.image_Folder + "\Respawn.png").convert_alpha()
        MainMenu = pygame.image.load(self.image_Folder + "\MainMenu.png").convert_alpha()

        self.imageList = {
            "Ship" : Ship,
            "MachineSoulEnemy1" : MachineSoulEnemy1,
            "MachineSoulEnemy2" : MachineSoulEnemy2,
            "MachineSoulEnemy3" : MachineSoulEnemy3,
            "MachineSoulEnemy4" : MachineSoulEnemy4,
            "ShipLazer" : ShipLazer,
            "EnemyLazer" : EnemyLazer,
            "TargetCursor" : TargetCursor,
            "Map" : Map,
            "Wave1" : Wave1,
            "Wave2" : Wave2,
            "Wave3" : Wave3,
            "Wave4" : Wave4,
            "Wave5" : Wave5,
            "MissionComplete" : MissionComplete,
            "MissionFailed" : MissionFailed,
            "ShipDied" : ShipDied,
            "Respawn" : Respawn,
            "MainMenu" : MainMenu,

        }
        return self.imageList
    

    @staticmethod
    def CreateTimer(millSeconds):
        Timer = pygame.event.custom_type()
        pygame.time.set_timer(Timer, millSeconds)
        return Timer
    
    @staticmethod
    def StopTimer(Timer):
        pygame.time.set_timer(Timer, 0)

    @staticmethod
    def ReStartTimer(Timer,millSeconds):
        pygame.time.set_timer(Timer, millSeconds)
    
    
    def NewWave(self):
        if self.wave+1 > 5:
            self.EndGame()
            return
        self.isWaveImage = True
        string = "Wave" + str(self.wave+1)  # Use self.wave directly
        self.WaveImage = self.imageList[string].copy()
        
        self.win.blit(self.WaveImage, (Game.width/2 - int(self.WaveImage.get_width() / 2), 50 - int(self.WaveImage.get_height() / 2)))
        self.ReStartTimer(self.WaveImageTimer, 5000)
        
    
    def UpdateWaveImage(self):
        if self.isWaveImage:
            self.win.blit(self.WaveImage, (Game.width/2 - int(self.WaveImage.get_width() / 2), 50 - int(self.WaveImage.get_height() / 2)))
            if plr.health <= 0:
                RespawnImage = self.imageList["Respawn"].copy()
                self.win.blit(RespawnImage, (Game.width/2 - int(RespawnImage.get_width() / 2), 100 - int(RespawnImage.get_height() / 2)))

    def EndGame(self):
        self.isWaveImage = True
        self.WaveImage = self.imageList["MissionComplete"].copy()
        self.win.blit(self.WaveImage, (Game.width/2 - int(self.WaveImage.get_width() / 2), 50 - int(self.WaveImage.get_height() / 2)))

    def MainMenu(self):
        MainMenuImage = self.imageList["MainMenu"].copy()
        self.win.blit(MainMenuImage, (Game.width/2 - int(MainMenuImage.get_width() / 2), 50 - int(MainMenuImage.get_height() / 2)))

    def UpdateMap(self):
        if self.isMainMenu:
            self.win.blit(Game.imageList["MainMenu"], (0,0))
        else:
            self.win.blit(Game.imageList["Map"], (0, 0))
    
    def ClickedButton(self,x,y):
        if not(self.isMainMenu):
            return
        if x >= 992 and x <= Game.width and y >= 304 and y <= 374:
            self.isMainMenu = False
            self.NewWave()
        elif x >= 998 and x <= Game.width and y >= 460 and y <= 526:
            pass # Add tutoral here!
    
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
                offset_x = self.rect.x - int(enemy.rect.x - enemy.image.get_width() / 2)
                offset_y = self.rect.y - int(enemy.rect.y - enemy.image.get_height() / 2)
                if enemy.mask.overlap(self.mask, (offset_x, offset_y)):
                    enemy.ChangeHealth(-1)
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
    makeEnemies = False
    
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
        self.rect = self.image.get_rect()
        

        match type:
            case "MachineSoulEnemy1":
                self.health = 1
            case "MachineSoulEnemy2":
                self.health = 25
            case "MachineSoulEnemy3":
                self.health = 50
                self.vel = 1
            case "MachineSoulEnemy4":
                self.health = 10
                self.vel = 3
            case _:
                print("NO TYPE FOR ENEMY!!")
                self.health = 1
        
        self.maxHealth = self.health
        
        Enemy.EnemyList.append(self)

    @staticmethod
    def createEnemy(type):
        if not(Enemy.makeEnemies):
            return
        TopOrSide = random.randint(0,1)
        if TopOrSide == 0:
            x = random.randint(0,Game.width)
            y = 0
        else:
            x = 0
            y = random.randint(0,Game.height)
        if type == "MachineSoulEnemy3":
            for enemy in Enemy.EnemyList:
                if enemy.type == "MachineSoulEnemy3":
                    type == "MachineSoulEnemy1"
                    break
        Enemy1 = Enemy(x,y,type)
        
    def Draw(self):
        Entity.Draw(self.image,self.x,self.y)
    
    def Move(self):
        self.x,self.y = Entity.Move(self.x,self.y,self.angle,self.vel)
        self.rect.x = self.x 
        self.rect.y = self.y
        
    
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
    
    def ChangeHealth(self,healthValue):
        self.health += healthValue
        if self.health <= 0:
            Enemy.EnemyList.remove(self)
            if hasattr(self, "HealthBar"):
                self.HealthBar.Remove()
            if hasattr(self, "HealthBeam"):
                self.HealthBeam.Remove()
            return 
        if self.health < self.maxHealth and not hasattr(self, "HealthBar"):
            self.HealthBar = Drawing.MakeRect(self.x,self.y,50,5,(0,255,0),(0,255,0),"rect")
        if self.health > self.maxHealth:
            self.health = self.maxHealth

    def Update(self):
        if plr.health <= 0:
            self.Draw()
            return
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
        elif self.type == "MachineSoulEnemy3":
            ClosestDistance = 9999999999
            TargetX = None
            TargetY = None
            SavedEnemy = None
            for enemy in Enemy.EnemyList:
                if enemy == self or enemy.type == "MachineSoulEnemy3":
                    continue
                CurrentDistance = math.dist((self.x,self.y),(enemy.x,enemy.y))
                if CurrentDistance < ClosestDistance:
                    ClosestDistance = CurrentDistance
                    TargetX = enemy.x
                    TargetY = enemy.y
                    SavedEnemy = enemy
            
            if not(TargetX == None or TargetY == None):  
                self.angle = Entity.FollowAngle(self.x,self.y,TargetX,TargetY)
                self.Rotate()
                if not(ClosestDistance <= 25):
                    self.Move()

                if hasattr(self, "HealthBeam"):
                    self.HealthBeam.Remove()
                self.HealthBeam = Drawing.MakeLine((self.x,self.y),(TargetX,TargetY),(0,255,0))
                SavedEnemy.ChangeHealth(0.1)
            else:
                if hasattr(self, "HealthBeam"):
                    self.HealthBeam.Remove()
        elif self.type == "MachineSoulEnemy4":
            self.angle = Entity.FollowAngle(self.x,self.y,plr.x,plr.y)
            self.Rotate()
            distiance = math.dist((self.x,self.y),(plr.x,plr.y))
            transparencyValue = max(0, 255 - int(distiance))
            if transparencyValue > 255:
                transparencyValue = 255
            elif transparencyValue < 50:
                transparencyValue = 50
            self.image.set_alpha(transparencyValue)
            self.Move()
            if self.IsMaskOverlap(plr.mask,plr.rect):
                plr.ChangeHealth(-0.5)

        if hasattr(self, "HealthBar"):
            self.HealthBar.x = self.x - 25
            self.HealthBar.y = self.y - 25

            

            self.HealthBar.width = 50 * (self.health / self.maxHealth)

            self.HealthBar.fillColor = (0,255,0)

            if self.health < self.maxHealth / 2:
                self.HealthBar.fillColor = (255,255,0)
            if self.health < self.maxHealth / 10:
                self.HealthBar.fillColor = (255,0,0)

            self.HealthBar.draw()
        self.rect.x = self.x 
        self.rect.y = self.y
  
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

    shipDiedImage = Game.imageList["ShipDied"].copy()
    shipDiedImage = pygame.transform.scale(shipDiedImage,(32,32))

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
        self.LazerHeatBackground = Drawing.MakeRect(25,25,120,50,(0,0,0),(130, 127, 128),"rect")
        self.LazerHeatBar = Drawing.MakeRect(37.5,37.5,100,25,(0,255,0),(0,255,0),"rect")
        self.LazersFired = 0
        self.LazerCooldown = False
        self.health = 100
        self.direction = 0
        
        self.healthBarBackground = Drawing.MakeRect(25,100,50,120,(0,0,0),(130, 127, 128),"rect")
        self.healthBar = Drawing.MakeRect(37.5,112.5,25,100,(130,127,255),(255,0,0),"rect")
        self.mask = pygame.mask.from_surface(self.shipImage)
        self.rect = self.shipImage.get_rect()
        self.rect.center = (self.x, self.y)  
        self.maxVel = 7
    def Draw(self):
        if Game.isMainMenu:
            return
        Entity.Draw(Ship.shipImage, self.x, self.y)
        self.rect.center = (self.x, self.y)

    def Rotate(self, angle):
        if self.health <= 0:
            return
        Ship.shipImage = Entity.Rotate(Ship.originalScaledShipImage, angle)

    def Move(self):
        vel = self.direction * self.vel 
        self.x,self.y = Entity.Move(self.x,self.y,self.angle,vel)
        if self.x < 0:
            self.x = 0
        if self.x > Game.width:
            self.x = Game.width
        if self.y < 0:
            self.y = 0
        if self.y > Game.height:
            self.y = Game.height
    
    def IncreaseVelocity(self,vel,direction):
        if self.health <= 0:
            return
        if self.vel <= 0:
            self.vel = 0
            self.direction = direction
        

        if self.direction == direction:    
            self.vel += vel
        else:
            self.vel -= vel
        if self.vel > self.maxVel:
            self.vel = self.maxVel
         
    
    def DecreaseVelocity(self,vel):
        self.vel -= vel
        if self.vel < 0:
            self.vel = 0
        if self.vel > self.maxVel:
            self.vel = self.maxVel
    
    def ShootLazer(self):
        if Game.isMainMenu:
            return
        if self.health <= 0:
            return
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
        elif self.health <= 0:
            self.health = 0
            Game.StopTimer(Enemy.EnemyTimer)
            Game.StopTimer(Ship.shipLazerSoundTimer)
            Game.isWaveImage = True
            Game.WaveImage = Game.imageList["MissionFailed"].copy()
            Game.win.blit(Game.WaveImage, (Game.width/2 - int(Game.WaveImage.get_width() / 2), 50 - int(Game.WaveImage.get_height() / 2)))
            
            Ship.shipImage = Entity.Rotate(Ship.shipDiedImage, self.angle)
            return
        self.healthBar.height = self.health 
        self.healthBar.draw()
        self.healthBarBackground.draw()
    

    def Update(self):
        if self.health <= 0:
            self.Draw()
            return
        if self.vel > 0:
            self.Move()
        self.DecreaseVelocity(0.1)
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


    @classmethod
    def MakeRect(cls,x,y,width,height,color,fillcolor,type):

        NewDrawing = Drawing()
        NewDrawing.x = x
        NewDrawing.y = y
        NewDrawing.width = width
        NewDrawing.height = height
        NewDrawing.color = color
        if fillcolor == None:
            NewDrawing.fillColor = None
        NewDrawing.fillColor = fillcolor
        NewDrawing.type = type

        Drawing.drawingList.append(NewDrawing)

        return NewDrawing
    
    @classmethod
    def MakeLine(cls,startPoint,endPoint,color):

        NewDrawing = Drawing()
        NewDrawing.startPoint = startPoint
        NewDrawing.endPoint = endPoint
        NewDrawing.color = color
        NewDrawing.type = "line"

        Drawing.drawingList.append(NewDrawing)

        return NewDrawing

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
        elif self.type == "line":
            pygame.draw.line(Game.win, self.color, self.startPoint, self.endPoint, 2)

    
    def Remove(self):
        if self in Drawing.drawingList:
            Drawing.drawingList.remove(self)

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
clock = pygame.time.Clock()

Target = TargetCursor(0,0)
pygame.mouse.set_visible(False)




while Game.run:
    Game.UpdateMap()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.run = False
        if event.type == Enemy.EnemyTimer and not Game.isWaveImage and not Game.wave > 5 and not Game.wave == 0 and not Game.isMainMenu:
            waveList = []
            match Game.wave:
                case 1:
                    waveList = Game.wave1List
                case 2:
                    waveList = Game.wave2List
                case 3:
                    waveList = Game.wave3List
                case 4:
                    waveList = Game.wave4List
                case 5:
                    waveList = Game.wave5List
                case _:
                    print("NO WAVE")
            if not(len(waveList) == 0):
                num = waveList.pop(0)
                enemyType = "MachineSoulEnemy" + str(num)
                Enemy.createEnemy(enemyType)
        if event.type == Ship.shipLazerSoundTimer:
            Ship.shipLazerSound.play()
            Game.StopTimer(Ship.shipLazerSoundTimer)
        if event.type == Enemy.EnemyFireTimer:
            for enemy in Enemy.EnemyList:
                if enemy.type == "MachineSoulEnemy2":
                    enemy.ShootLazers()
        if event.type == Game.WaveImageTimer:
            Game.wave += 1
            Game.StopTimer(Game.WaveImageTimer)
            waveList = []
            match Game.wave:
                case 1:
                    waveList = Game.wave1List
                case 2:
                    waveList = Game.wave2List
                case 3:
                    waveList = Game.wave3List
                case 4:
                    waveList = Game.wave4List
                case 5:
                    waveList = Game.wave5List
            if waveList:
                Game.ReStartTimer(Enemy.EnemyTimer, 20000 // len(waveList))  # Adjust EnemyTimer dynamically
                Game.isWaveImage = False
                Game.ReStartTimer(Game.WaveTimer, 20000)
                Enemy.makeEnemies = True
        if event.type == Game.WaveTimer:
            Enemy.makeEnemies = False
            if len(Enemy.EnemyList) > 0:
                Game.ReStartTimer(Enemy.EnemyTimer,1000)
            else:
                Game.NewWave()
                if not(Game.wave >= 5):
                    Game.NewWave()
                    Game.StopTimer(Game.WaveTimer)
                    Game.ReStartTimer(Enemy.EnemyTimer,5000 - Game.wave * 500)
                
    keys = pygame.key.get_pressed()

    if not(Game.isMainMenu): 
        if keys[pygame.K_a]:
            plr.angle -= 5
            plr.Rotate(plr.angle)
        if keys[pygame.K_d]:
            plr.angle += 5
            plr.Rotate(plr.angle)
        if keys[pygame.K_w]:
            plr.IncreaseVelocity(1,1)
            
        if keys[pygame.K_s]:
            plr.IncreaseVelocity(1,-1)
        
        if keys[pygame.K_r]:
            if plr.health <= 0:
                Enemy.EnemyList.clear()
                print(Enemy.EnemyList)
                plr.ChangeHealth(100) 
                plr.shipImage = Ship.originalScaledShipImage.copy()
                Ship.shipImage = plr.shipImage
                plr.Rotate(plr.angle)
                Game.isWaveImage = False
                Game.wave = 0


    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        Game.ClickedButton(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        
        plr.ShootLazer()

    Enemy.UpdateEnemies()
    plr.Update()
    Drawing.UpdateDrawings()
    Target.Update()
    Lazer.UpdateLazers()
    Game.UpdateWaveImage()
    pygame.display.update()
        
    clock.tick(60)
    

pygame.quit()