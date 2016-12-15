import pygame

##The API class for all programs, methods can be added and extended
#TODO: add function descriptions
class ProgramAPI:
    def __init__(self, pos, drawpr, hasBorder, isMax):
        print("this shouldnt be run, only overridden")

    def initProc(self):
        print("ERROR: No initProc() function overridden!")

    def update(self):
        print("ERROR: No update() function overridden!")

    def draw(self, screen):
        print("ERROR: No draw() function overridden!")

    #Use this for window movement in each program
    def checkWindowMovement(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.sysCtls[1].collidepoint(pos):
                    return False
                elif self.sysCtls[0].collidepoint(pos):
                    if self.clicked == False:
                        self.mpos = pos
                        self.ipos = self.pos
                    xch = self.mpos[0]+pos[0]
                    ych = self.mpos[1]+pos[1]
                    self.pos = (self.ipos[0]+xch, self.ipos[1]+ych)
                    self.clicked = True
                    self.drawpr = 2
                else:
                    self.clicked = False
                    self.mpos, self.ipos = (0,0)
              
    def quitProc(self):
        pass

    def install(self):
        pass
