import pygame

pygame.init()

pygame.display.set_caption("Ship")

class Game:
    def __init__(self):
        self.width = 1300
        self.height = 650
        self.win = pygame.display.set_mode((self.width, self.height))
        self.run = True

Game = Game()

class Ship:
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
        NewPoints = self.Rotate(self.angle)
        print(NewPoints[0][0])
        pygame.draw.polygon(Game.win, self.color, 
                    [[NewPoints[0][0]+self.x, NewPoints[0][1]+self.y], [NewPoints[1][0]+self.x, NewPoints[1][1]+self.y],
                    [NewPoints[2][0]+self.x, NewPoints[2][1]+self.y]])

        # pygame.draw.polygon(Game.win, self.color, 
        #             [[300+self.x, 100+self.y], [300+self.x, 200+self.y],
        #             [200+self.x, 200+self.y]])
    def Rotate(self, angle):
        pp = pygame.math.Vector2(300+self.x, 200+self.y)
        rotated_points = [
            (pygame.math.Vector2(x, y) - pp).rotate(angle) + pp for x, y in self.points]
        return rotated_points


plr = Ship()

while Game.run:
    Game.win.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        plr.angle += 1
    if keys[pygame.K_RIGHT]:
        plr.angle -= 1
    if keys[pygame.K_UP]:
        plr.y -= 1
    if keys[pygame.K_DOWN]:
        plr.y += 1
    plr.draw(Game.win)
    pygame.display.update()
        
        
    

pygame.quit()