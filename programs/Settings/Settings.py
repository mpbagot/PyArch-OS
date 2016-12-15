import pygame
import ConfigCtl
import DrawLib
import os

class Settings:
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.pos = pos
    self.drawpr = drawpr
    self.hasBorder = hasBorder
    self.max = isMax
    self.screen = pygame.Surface((640, 480))
    self.title = "Settings"
    self.clicked = False

  def initProc(self):
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    self.fontSmall = pygame.font.SysFont(pygame.font.get_default_font(), 25)
    self.page = 0
    self.button1 = self.button2 = False
    self.buttonB = self.buttonA = None
    self.newWallpaper = "config/wallpaper.jpg"
    self.loc = "/users/"+ConfigCtl.getCurrentUser()+"/"
    self.up = ConfigCtl.getAllUsers()
    self.getting = self.getting3 = self.getting2 = False
    self.selIndex = 200
    self.passw = ""
    self.un = ""

  def update(self, events):
    self.up = ConfigCtl.getAllUsers()
    pos = pygame.mouse.get_pos()
    pos2 = (pos[0]-self.pos[0], pos[1]-self.pos[1])
    
    if self.page == 0:
      if self.buttonB != None:
        if self.buttonA.collidepoint(pos2):
          self.button1 = True
        else:
          self.button1 = False

        if self.buttonB.collidepoint(pos2):
          self.button2 = True
        else:
          self.button2 = False
    
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN and (not self.getting or self.getting2):
        if self.page == 0:
          if self.buttonA.collidepoint(pos2):
            self.page = 1
          elif self.buttonB.collidepoint(pos2):
            self.page = 2
        elif self.page == 1:
          if self.imgButton.collidepoint(pos2):
            self.getting = True
          if self.confirm.collidepoint(pos2):
            self.setWallpaper(self.loc)
            self.page = 0

        elif self.page == 2:
          if self.plusButton.collidepoint(pos2):
            ConfigCtl.addUser("NewUser")
          if self.minusButton.collidepoint(pos2):
            uname = ""
            i = 0
            for a in self.up:
              if i == self.selIndex:
                uname = a
              i += 1
            ConfigCtl.rmUser(uname)
          if self.selIndex < len(self.users) and self.pChange.collidepoint(pos2):
            self.getting2 = True
          if self.selIndex < len(self.users) and self.uChange.collidepoint(pos2):
            self.getting3 = True

          if self.box.collidepoint(pos2):
            pos3 = (pos2[0]-30, pos2[1]-50)
            x = (pos3[1]-(pos3[1]%22))/22
            self.selIndex = int(x)

      if self.getting and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          self.newWallpaper = self.loc[1:]
          self.getting = False          
          return
        self.loc  = self.loc + event.unicode if event.key != pygame.K_BACKSPACE else self.loc[0:-1]

      if self.getting2 and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          self.setPassword(self.passw)
          self.getting2 = False          
          return
        self.passw  = self.passw + event.unicode if event.key != pygame.K_BACKSPACE else self.passw[0:-1]

      if self.getting3 and event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          self.setUsername(self.un)
          self.getting3 = False          
          return
        self.un  = self.un + event.unicode if event.key != pygame.K_BACKSPACE else self.un[0:-1]

  def draw(self, screen):
    screen.fill((255,255,255))

    if self.page == 0:
      if not self.button1:
        self.buttonA = pygame.draw.rect(screen, (192,192,192), [0,20,320, 480], 0)
      else:
        self.buttonA = pygame.draw.rect(screen, (128,128,128), [0,20,320,480], 0)
      text = self.font.render("Wallpaper", True, (0,0,0))
      screen.blit(text, [100, 380])

      img = pygame.transform.scale(pygame.image.load("config/wallpaper.jpg").convert_alpha(), [250,200])
      screen.blit(img, [35, 125])
        
      if not self.button2:
        self.buttonB = pygame.draw.rect(screen, (192,192,192), [320,20,320, 480], 0)
      else:
        self.buttonB = pygame.draw.rect(screen, (128,128,128), [320,20,320,480], 0)
      text = self.font.render("Users", True, (0,0,0))
      screen.blit(text, [450, 380])

      img = pygame.transform.scale(pygame.image.load("programs/Settings/users.png").convert_alpha(), [250,250])
      screen.blit(img, [355, 100])

      pygame.draw.rect(screen, (0,0,0), [319, 0, 2, 480], 0)

    if self.page == 1:
      #Wallpaper settings
      screen.fill((192,192,192))

      img = pygame.transform.scale(pygame.image.load("config/wallpaper.jpg").convert_alpha(), [200,160])
      screen.blit(img, [220, 25])

      text = self.font.render("Current", True, (0,0,0))
      screen.blit(text, [280, 200])

      img = pygame.transform.scale(pygame.image.load(self.newWallpaper).convert_alpha(), [200,160])
      self.imgButton = screen.blit(img, [220, 250])

      text = self.font.render("New", True, (0,0,0))
      screen.blit(text, [320-(text.get_rect().width/2), 420])

      self.confirm = pygame.draw.rect(screen, (128,128,128), [550, 380, 60, 30], 0)
      text = self.font.render("Save", True, (0,0,0))
      screen.blit(text, [555, 385])
      
      pygame.draw.rect(screen, (0,0,0), [0, 239, 640, 2], 0)

    if self.page == 2:
      #User Controls
      screen.fill((192,192,192))

      self.box = pygame.draw.rect(screen, (232,232,232), [30, 50, 180, 350], 0)

      self.users = []

      i = 0
      for a in self.up:
        if i == self.selIndex:
          pygame.draw.rect(screen, (192,192,192), [30, 50+25*self.selIndex, 180, 25], 0)
          #Draw user info
          text = self.fontSmall.render("Username: "+a, True, (0,0,0))
          self.uChange = screen.blit(text, [250, 100])
          text = self.fontSmall.render("Password: "+"*"*len(self.up[a]), True, (0,0,0))
          self.pChange = screen.blit(text, [250, 150])
        text = self.fontSmall.render(a, True, (0,0,0))
        screen.blit(text, [35, 55+22*i])
        self.users.append(a)
        i += 1

      #Plus/Minus Buttons
      pygame.draw.rect(screen, (128,128,128), [30, 370, 180, 30], 0)
      self.minusButton = pygame.draw.rect(screen, (125,125,125), [150, 370, 30, 30], 0)
      pygame.draw.line(screen, (0,0,0), [155, 385], [175, 385], 2)
      self.plusButton = pygame.draw.rect(screen, (125,125,125), [180, 370, 30, 30], 0)
      pygame.draw.line(screen, (0,0,0), [185, 385], [205, 385], 2)
      pygame.draw.line(screen, (0,0,0), [195, 375], [195, 395], 2)
      
      #User list border
      pygame.draw.rect(screen, (0,0,0), [30, 50, 180, 350], 1)

    if self.getting or self.getting2 or self.getting3:
      dial = pygame.Surface((200, 100))
      dial.fill((192,192,192))
      
      DrawLib.inputBox(dial, (255,255,255), (0,0,0), [45, 45, 110, 30], 1)

      if self.getting2:
        text = self.font.render(self.passw, True, (0,0,0))
      elif self.getting3:
        text = self.font.render(self.un, True, (0,0,0))
      else:
        text = self.font.render(self.loc, True, (0,0,0))
      if text.get_rect().width > 100:
        text = self.getShorterText()
      dial.blit(text, [50, 50])

      DrawLib.drawWindowBorderSurface((200,100), dial)
      
      screen.blit(dial, [200, 200])
      
    return screen

  def quitProc(self):
    pass

  def setWallpaper(self, file):
    file = file[1:]
    try:
      with open(file, "rb") as f:
        t = f.read()
      with open ("config/wallpaper.jpg", "wb") as f2:
        f2.write(t)
      self.getting = False
    except:
      return
    return

  def getShorterText(self):
    for i in range(len(self.loc)):
      text = self.font.render(self.loc[i:], True, (0,0,0))
      if text.get_rect().width <= 100:
        return text
    return ""

  def setPassword(self, passw):
    self.up[self.users[self.selIndex]] = passw
    with open("user.pt", "r") as f:
      t = f.read().split("\n")
    for a in range(len(t)):
      t[a] = t[a].split(",")
      if t[a][0] == self.users[self.selIndex]:
        t[a][1] = passw
      t[a] = ",".join(t[a])
    with open("user.pt", "w") as f2:
      f2.write("\n".join(t))

  def setUsername(self, uname):
    if uname in self.users:
      return
    try:
      with open("user.pt", "r") as f:
        t = f.read().split("\n")
      for a in range(len(t)):
        t[a] = t[a].split(",")
        if t[a][0] == self.users[self.selIndex]:
          t[a][0] = uname
        t[a] = ",".join(t[a])
      with open("user.pt", "w") as f2:
        f2.write("\n".join(t))
      os.rename(os.getcwd()+"/users/"+self.users[self.selIndex], os.getcwd()+"/users/"+uname)
    except:
      pass
