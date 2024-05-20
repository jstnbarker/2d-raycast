import math
import pygame
from pygame.locals import *

pygame.display.init()

screen = pygame.display.set_mode([1000, 1000])
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

walls = []

class LineSpecs:
    xy1: pygame.Vector2
    xy2: pygame.Vector2
    m: float
    b: float
    domain = list[int]

    def __init__(self, xy1: pygame.Vector2, xy2: pygame.Vector2):
        x1 = xy1[0]
        y1 = xy1[1]
        x2 = xy2[0]
        y2 = xy2[1]

        self.xy1 = xy1
        self.xy2 = xy2
        self.m = (y2 - y1) / (x2 - x1)
        self.b = y1 - (x1*self.m)
        self.domain = [x1, x2]
        self.domain.sort()
        
def main():
    tempwall = []
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                val = event.dict["key"]
                if val == 127 or val == 120:
                    try:
                        walls.pop(len(walls)-1)
                    except:
                        continue
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.dict["pos"]
                tempwall.append(pygame.Vector2(mouse_pos))
                if len(tempwall) == 2:
                    walls.append(LineSpecs(tempwall[0], tempwall[1]))
                    print(walls[len(walls)-1].domain)
                    tempwall = []
            print(event)
            
        screen.fill("gray")
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        for wall in walls:
            pygame.draw.line(screen, "red", wall.xy1, wall.xy2,width=3)

        for deg in range(360):
            ray_x = math.cos(math.radians(deg))*screen.get_width()
            ray_y = math.sin(math.radians(deg))*screen.get_height()
            m = ray_y/ray_x
            b = ray_y-(ray_x*m)

            for wall in walls:
                x1 = wall.xy1[0] - mouse_pos[0]
                y1 = wall.xy1[1] - mouse_pos[1]
                x2 = wall.xy2[0]- mouse_pos[0]
                y2 = wall.xy2[1]- mouse_pos[1]

                wm = (y2 - y1) / (x2 - x1)
                wb = (y1-(x1*wm))
                
                mouse_rel_intercept = (b - wb)/(wm - m)
                intercept = mouse_pos[0] + mouse_rel_intercept
                if( wall.domain[0] <= intercept and intercept <= wall.domain[1]):
                    #sohcahtoa
                    ray_x = mouse_rel_intercept
                    ray_y = mouse_rel_intercept * math.tan(math.radians(deg))
            pygame.draw.line(screen, "white", mouse_pos,[
                ray_x+mouse_pos[0], 
                ray_y+mouse_pos[1] 
            ])

        pygame.draw.circle(screen, "white", mouse_pos, radius=10)
        pygame.display.flip()
        clock.tick(60)

main()
