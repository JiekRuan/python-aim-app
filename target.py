import pygame
import time, random, math 
# fichier qui contient la class pour les cibles

class Target:
    MAX_SIZE = 30
    growth_rate = 0.5
    color = "red"
    second_color = "white"

    def __init__(self,x,y,lifespan):
        self.x = x
        self.y = y
        self.size = self.MAX_SIZE
        self.lifespan = lifespan  
        self.creation_time = time.time()
    
    def is_expired(self):
        return time.time() - self.creation_time > self.lifespan

    def update(self):
        if self.size + self.growth_rate >= self.MAX_SIZE:
            self.grow = False
        if self.grow:
            self.size += self.growth_rate
        else:
            self.size -= self.growth_rate
    
    def draw(self,window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(window, self.second_color, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(window, self.second_color, (self.x, self.y), self.size * 0.4)
    def collide(self,x,y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size