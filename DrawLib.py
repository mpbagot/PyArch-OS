import pygame
import ConfigCtl

def drawWindowBorder(size, prog):
    pygame.draw.rect(prog.screen, (64,64,64), [0,0,size[0],size[1]], 5)
    return (pygame.draw.rect(prog.screen, (64,64,64), [0,0,size[0],20], 0), 
    pygame.draw.rect(prog.screen, (255,0,0), [size[0]-40, 0, 30, 18], 0))

def inputBox(screen, c1, c2, rect, width):
    pygame.draw.rect(screen, c1, rect, 0)
    return pygame.draw.rect(screen, c2, rect, width)

def drawTitle(title, prog):
    text = ConfigCtl.getSysTitleFont().render(prog.title, True, (255,255,255))
    x = prog.screen.get_rect().width/2-(text.get_rect().width/2)
    prog.screen.blit(text, [x, 3])

def drawWindowBorderSurface(size, screen):
    pygame.draw.rect(screen, (64,64,64), [0,0,size[0],size[1]], 5)
    pygame.draw.rect(screen, (64,64,64), [0,0,size[0],20], 0)
    return pygame.draw.rect(screen, (255,0,0), [size[0]-40, 0, 30, 18], 0)
