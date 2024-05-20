import math
import pygame
from pygame.locals import *

pygame.display.init()

screen = pygame.display.set_mode([1000, 1000])
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

walls = []

bg = Color(26,26,26)

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
                    walls.append([tempwall[0], tempwall[1]])
                    tempwall = []
            
        screen.fill(bg)
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

        for wall in walls:
            pygame.draw.line(screen, "red", wall[0], wall[1],width=3)

        walls_only= screen.copy()


        for deg in range(0,360,3):
            ray_x = math.cos(math.radians(deg))*screen.get_width()
            ray_y = math.sin(math.radians(deg))*screen.get_width()
            # soh cah toa
            hyp = 0
            while True:
                hyp+=1
                ray_x = math.cos(math.radians(deg))*hyp
                ray_y = math.sin(math.radians(deg))*hyp
                if mouse_pos[0]+ray_x >= screen.get_width() or mouse_pos[0]+ray_x<0:
                    break
                if mouse_pos[1]+ray_y >= screen.get_height() or mouse_pos[1]+ray_y < 0:
                    break
                endpoint=((int(mouse_pos[0]+ray_x),int(mouse_pos[1]+ray_y)))
                if walls_only.get_at(endpoint) != bg:
                    break
            pygame.draw.line(screen, "white", mouse_pos, [
                mouse_pos[0]+ray_x,
                mouse_pos[1]+ray_y
            ])

        pygame.draw.circle(screen, "white", mouse_pos, radius=10)
        pygame.display.flip()
        clock.tick(60)

main()
