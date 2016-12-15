import pygame
import random

class RaceGame:
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.pos = pos
    self.drawpr = drawpr
    self.hasBorder = hasBorder
    self.max = isMax
    self.screen = pygame.Surface((640, 480))
    self.title = "Generic Car Arcade Game"
    self.clicked = False

  def initProc(self):
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
    self.yoffset = self.page = 0
    self.back = pygame.image.load("programs/RaceGame/menu.png").convert_alpha()
    self.track = pygame.image.load("programs/RaceGame/track.png").convert_alpha()
    self.lane = 1
    self.obstacles = []
    self.carimg = pygame.transform.scale(pygame.image.load("programs/RaceGame/car.png").convert_alpha(), [70,70])
    self.jtime = 0
    self.jumping = False
    self.startticks = pygame.time.get_ticks()

  def update(self, events):
    cticks = pygame.time.get_ticks()-self.startticks
    if self.page == 1:
      self.yoffset += 8+int(cticks/15000)
      if self.yoffset >= 200:
        self.yoffset = -40
      for a in self.obstacles:
        a.offset += 8+int(cticks/15000)
        a.rect[1] = a.offset
        if not self.jumping and self.willCollide(self.car, a.rect):
          self.page = 2
        if a.rect[1] > 480:
          del self.obstacles[self.obstacles.index(a)]
      if self.jumping:
        if cticks-self.jtime >= 2500:
          self.jumping = False
      if cticks%5000 <= 150:
        self.spawnObstacles(int(random.randint(100,300)/100))
      #check for obstacle spawning here


    for event in events:
      if event.type == pygame.KEYDOWN:
        if self.page == 1:
          if event.key == pygame.K_LEFT and self.lane > 0:
            self.lane -= 1
          elif event.key == pygame.K_RIGHT and self.lane < 2:
            self.lane += 1
          if event.key == pygame.K_SPACE and self.jumping == False:
            self.jumping = True
            self.jtime = cticks

      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        pos = (pos[0]-self.pos[0], pos[1]-self.pos[1])
        if self.page == 0:
          if self.playButton.collidepoint(pos):
            self.page = 1
          elif self.quitButton.collidepoint(pos):
            return "quit"
##            pygame.quit()

        elif self.page == 2:
          if self.restart.collidepoint(pos):
            self.initProc()
            self.page = 1
          elif self.quitButton.collidepoint(pos):
            return "quit"
##            pygame.quit()

  def draw(self, screen):
    screen.fill((255,255,255))

    if self.page == 0:
      screen.blit(self.back, [0,0])

      text = self.font.render("Generic Car Arcade Game", True, (0,0,0))
      screen.blit(text, [120, 80])

      self.playButton = pygame.draw.rect(screen, (255,255,255), [200,150,80,40], 0)
      pygame.draw.rect(screen, (0,0,0), [200,150,80,40], 1)

      text = self.font.render("Play!", True, (0,0,0))
      screen.blit(text, [207, 155])

      self.quitButton = pygame.draw.rect(screen, (255,255,255), [200,220,80,40], 0)
      pygame.draw.rect(screen, (0,0,0), [200,220,80,40], 1)

      text = self.font.render("Quit", True, (0,0,0))
      screen.blit(text, [210, 225])

      font = pygame.font.SysFont(pygame.font.get_default_font(), 15)
      text = font.render("Game Idea by Kirsty Polson, 10F", True, (255,255,255))
      screen.blit(text, [470, 465])

    if self.page == 2:
      screen.blit(self.back, [0,0])

      text = self.font.render("You Crashed!", True, (0,0,0))
      screen.blit(text, [120, 80])

      self.restart = pygame.draw.rect(screen, (255,255,255), [200,150,120,40], 0)
      pygame.draw.rect(screen, (0,0,0), [200,150,120,40], 1)

      text = self.font.render("Restart", True, (0,0,0))
      screen.blit(text, [210, 155])

      self.quitButton = pygame.draw.rect(screen, (255,255,255), [200,220,80,40], 0)
      pygame.draw.rect(screen, (0,0,0), [200,220,80,40], 1)

      text = self.font.render("Quit", True, (0,0,0))
      screen.blit(text, [210, 225])

    if self.page == 1:
      screen.blit(self.track, [0, -200+self.yoffset])

      for a in self.obstacles:
        screen.blit(a.img, a.rect)
      
      if self.jumping:
        self.carimg = pygame.transform.scale(self.carimg, [90,90])
      else:
        self.carimg = pygame.transform.scale(self.carimg, [70,70])
      self.car = screen.blit(self.carimg, [200+80*self.lane-(10 if self.jumping else 0), 380])

    return screen

  def quitProc(self):
    pass

  def spawnObstacles(self, num):
    obst = []
    for a in range(num):
      obst.append(Obstacle(a))
    if num < 3:
      if num == 1:
        obst[0].lane = random.randint(0,2)
      else:
        obst[0].lane = 2
        obst[1].lane = random.randint(0,1)
    for a in obst:
      a.setRect()
    self.obstacles += obst

  def willCollide(self, r1, r2):
    if r1.left >= r2[0]-3 and r1.right <= r2[0]+73:
      if r1.top <= r2[1]+22 and r1.bottom >= r2[1]:
        return True
    return False

class Obstacle:
  def __init__(self, lane):
    self.rect = [200+lane*80, -50]
    self.img = pygame.image.load("programs/RaceGame/obs.png").convert_alpha()
    self.lane = lane
    self.offset = 0

  def setRect(self):
    self.rect[0] = 200+self.lane*80
    
