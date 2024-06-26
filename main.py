from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import threading

SAND = (255, 255, 0, 255)
AIR  = (0,   0,   0, 255)

WIDTH, HEIGHT = 300, 300
RAD = 5

FRAMERATE = 60
THREAD_COUNT = 1

def apply_gravity(surface,pixels, bottomRow):
    allSand = 1
    for y in range(bottomRow-2, -1, -1): # start at one from the bottom
        x = 0
        while x < WIDTH:
            if pixels[x,y] == surface.map_rgb(SAND):
                if pixels[x,y+1] == surface.map_rgb(AIR): # drop down if theres space
                    pixels[x,y+1] = surface.map_rgb(SAND) 
                    pixels[x,y] = surface.map_rgb(AIR) 
                elif x > 0 and pixels[x-1,y+1] == surface.map_rgb(AIR): # drop down-right if theres space
                    pixels[x-1,y+1] = surface.map_rgb(SAND)
                    pixels[x,y] = surface.map_rgb(AIR)
                elif x < WIDTH-1 and pixels[x+1, y+1] == surface.map_rgb(AIR): # drop down-left if theres space
                    pixels[x+1,y+1] = surface.map_rgb(SAND)
                    pixels[x,y] = surface.map_rgb(AIR)
            else:
                allSand = 0 
            x += 1
    return allSand

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface((WIDTH, HEIGHT))
surface.fill(AIR)

screen = pygame.display.get_surface()
screen.blit(surface, (0,0))
pygame.display.flip()

bottomRow = HEIGHT

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            
            pygame.draw.circle(surface, SAND, (x,y), RAD)
    pxarrray = pygame.PixelArray(surface)

    bottomRow -= apply_gravity(surface, pxarrray, bottomRow)
    del pxarrray
    screen.blit(surface, (0,0))
    pygame.display.flip()

    clock.tick(FRAMERATE)
    print(clock.get_fps())