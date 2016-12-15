import ProgramAPI
import DrawLib
import pygame
import ConfigCtl
import os
import UserCred
from Icon import Icon

##System Programs File, PUT ALL THE DEFAULT SYSTEM
##PROGRAMS IN HERE.

class Login(ProgramAPI.ProgramAPI):
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.drawpr = drawpr
    self.max = True
    self.hasBorder = hasBorder
    self.clicked = False
    self.screen = pygame.surface.Surface((1024,768))

  def initProc(self):
    self.username = ""
    self.password = ""
    self.ebox = 0
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 35)

  def update(self):
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if self.ubox.collidepoint(pos):
          self.ebox = 1
        if self.pbox.collidepoint(pos):
          self.ebox = 2
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          self.shouldUpdate = False
          return
        if event.key == pygame.K_TAB:
          self.ebox = 2
        elif self.ebox != 0:
          if self.ebox == 1:
            self.username = (self.username+event.unicode if event.key != pygame.K_BACKSPACE else self.username[0:-1])
          if self.ebox == 2:
            self.password = (self.password+event.unicode if event.key != pygame.K_BACKSPACE else self.password[0:-1])
  
  
  def draw(self, screen):
    screen.fill((100,152,255))
    #750, 768
    pygame.draw.polygon(screen, (192, 255, 98), [[710, 768],[680, 0],[440, 0]], 0)
    pygame.draw.polygon(screen, (255, 160, 160), [[710, 768], [150, 0], [440, 0]], 0)
    pygame.draw.polygon(screen, (255, 181, 100), [[710, 768], [150, 0], [0, 0], [0, 300]], 0)
##    pygame.draw.polygon(screen, (192, 255, 98), [[710, 768],[680, 0],[440, 0]], 0)
##    pygame.draw.polygon(screen, (255, 255, 0), [[710, 768], [150, 0], [440, 0]], 0)
##    pygame.draw.polygon(screen, (192, 255, 98), [[710, 768], [150, 0], [0, 0], [0, 300]], 0)
    
    img = pygame.transform.scale(pygame.image.load("sysobj/login2.jpg"), [450,250])
    screen.blit(img, [275,275])
    
##    pygame.draw.rect(screen, (100,152,255), [275, 275, 450, 250], 0)
    pygame.draw.rect(screen, (255,255, 152), [275, 275, 450, 250], 2)
    
    self.ubox = DrawLib.inputBox(screen, (255,255,255),(0,0,0), [452, 354, 120, 30], 1)
    self.pbox = DrawLib.inputBox(screen, (255,255,255),(0,0,0), [452, 414, 120, 30], 1)
    text = self.font.render(self.username if len(self.username) < 10 else self.username[-9:], True, (0,0,0))
    if text.get_rect().width > self.ubox.width:
      text = pygame.transform.scale(text, [self.ubox.width, self.ubox.height])
    screen.blit(text, [454, 357])
    text = self.font.render(len(self.password)*"*" if len(self.password) < 10 else "*"*10, True, (0,0,0))
    screen.blit(text, [454, 417])
    text = self.font.render("Username:", True, (0,0,0))
    screen.blit(text, [324, 357])
    text = self.font.render("Password:", True, (0,0,0))
    screen.blit(text, [324, 417])
    
    pygame.display.get_surface().blit(screen, [0,0])
    pygame.display.flip()
    return screen

  def getResult(self, clock, updateScreen = False):
    self.shouldUpdate = updateScreen
    while self.shouldUpdate != False:
      self.update()
      self.draw(self.screen)
      clock.tick(30)
    user = self.getUserCredFromLogin()
    if user != False:
      return user
    self.username = ""
    self.password = ""
    self.shouldUpdate = True
    return self.getResult(clock, True)
    
  def getUserCredFromLogin(self):
    file = []
    udict = {}
    for line in open("user.pt"):
      file.append(line.strip())
    for a in file:
      user = a.split(",")
      if user[0] == self.username and user[1] == self.password:
        return UserCred.UserCred(user[2])
    return False

class Tester(ProgramAPI.ProgramAPI):
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.drawpr = drawpr
    self.max = False
    self.clicked = False
    self.hasBorder = hasBorder
    self.screen = pygame.Surface((665, 490))

  def initProc(self):
    self.title = "Tester"
    print("Initialising")

  def update(self, events):
    print("updating")
  
  def draw(self, screen):
    pygame.draw.rect(screen, (255,255,255), [10, 10, 40, 40], 0)
    return screen

class Homebar(ProgramAPI.ProgramAPI):
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.drawpr = drawpr
    self.max = True
    self.pos = pos
    self.hasBorder = hasBorder
    self.clicked = False
    self.screen = pygame.surface.Surface((1024,48))

  def initProc(self):
    self.homeOpen = False
    self.homebar = pygame.transform.scale(pygame.image.load("sysobj/homebar.png").convert_alpha(), [1024, 48])
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 35)
    self.home = pygame.transform.scale(pygame.image.load("sysobj/logo.png").convert_alpha(), [48,48])
    self.dockedprogs = ConfigCtl.getDockedPrograms()
    self.allprogs = ConfigCtl.getInstalledPrograms()
    self.dockButtons = []
    self.menuButtons = []

  def update(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        pos = (pos[0], pos[1]-self.pos[1])
        if self.homebutton.collidepoint(pos):
          self.homeOpen = not self.homeOpen
        else:
          self.homeOpen = False
        if self.shutbutton.collidepoint(pos):
          return "shutdown"
        for a in range(len(self.dockButtons)):
          if self.dockButtons[a].collidepoint(pos):
            print("Launching "+self.dockedprogs[a])
            return "run "+self.dockedprogs[a]
        for a in range(len(self.menuButtons)):
          if self.menuButtons[a].collidepoint(pygame.mouse.get_pos()):
            print("Launching "+self.allprogs[a])
            return "run "+self.allprogs[a]
        ##if we collide with a home menu button then
        ##return "run "+buttontext        

  def draw(self, screen):
    screen.blit(self.homebar, [0,2])
    self.shutbutton = pygame.draw.rect(screen, (255, 64, 64), [7, 7, 30, 30], 0)
    self.homebutton = screen.blit(self.home, [973, 3])
    self.dockButtons = []
    self.menuButtons = []
    for index in range(len(self.dockedprogs)):
      a = self.dockedprogs[index]
      self.dockButtons.append(screen.blit(pygame.image.load("programs/"+a+"/icon.png").convert_alpha(), [917-(55*index), 3]))
    if self.homeOpen:
      for a in range(len(self.allprogs)):
        self.menuButtons.append(pygame.draw.rect(pygame.display.get_surface(), (6,77,132), [824,680-(40*a),200,40], 0))
        text = self.font.render(self.allprogs[a], True, (232,226,0))
        pygame.display.get_surface().blit(text, [835,683-(40*a)])

    return screen

#the homebar+home menu of the desktop

class Desktop(ProgramAPI.ProgramAPI):
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.drawpr = drawpr
    self.max = True
    self.pos = pos
    self.hasBorder = hasBorder
    self.clicked = False
    self.screen = pygame.surface.Surface((1024,768))

  def initProc(self):
    self.wallpaper = pygame.transform.scale(ConfigCtl.getWallpaper(), (1024, 768))
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 15)
    self.dir = os.getcwd()+"/users/"+str(ConfigCtl.getCurrentUser())+"/Desktop"
    self.files = os.listdir(self.dir)
    self.icons = self.getIconsFromFileList(self.files)
    self.clicked = False

  def update(self, events, progs):
    if pygame.mouse.get_pressed()[0]:
      if not self.clicked:
        pos = pygame.mouse.get_pos()
        if self.onlyCollidesHere(progs):
          for i in range(len(self.icons)):
            if self.icons[i].rect.collidepoint(pos):
              return "open "+self.dir+"/"+self.files[i]
      self.clicked = True
    elif pygame.mouse.get_pressed()[1]:
      print("right click")
    else:
      self.clicked = False
    files = os.listdir(os.getcwd()+"/users/"+str(ConfigCtl.getCurrentUser())+"/Desktop")
    if files != self.files:
      self.files = files
      self.icons = self.getIconsFromFileList(self.files)
    

  def draw(self, screen):
    screen.blit(pygame.transform.scale(ConfigCtl.getWallpaper(), (1024, 768)), [0,0])
    for a in range(len(self.icons)):
      self.icons[a].pos = [20+(50*int(a/12)), 20+(60*(a%12))]
      self.icons[a].rect = screen.blit(self.icons[a].icon, self.icons[a].pos)
      text = self.font.render(self.icons[a].text, True, (255,255,255))
      pos = [self.icons[a].pos[0]-5, self.icons[a].pos[1]+45]
      screen.blit(text, pos)
    return screen

  def getIconsFromFileList(self, files):
    icons = []
    for f in files:
      if f.endswith(".pt") or f.endswith(".txt"):
        #Add plaintext icon
        icons.append(Icon("sysobj/textdoc.png", f, True, self.dir))
      elif "." not in f:
        #add a folder icon
        icons.append(Icon("sysobj/folder.png", f, False, self.dir))
      else:
        #add generic icon (Temporary Until after due)
        icons.append(Icon("sysobj/generic.png", f, True, self.dir))
    return icons

  def onlyCollidesHere(self, programs):
    pos = pygame.mouse.get_pos()
    for p in programs:
      pos2 = (pos[0]-p.pos[0], pos[1]-p.pos[1])
      if p.screen.get_rect().collidepoint(pos2) and p != self:
        return False
    return True
  
##displays icons + wallpaper
#checks for change in wallpaper or in desktop folder

class FileExplorer(ProgramAPI.ProgramAPI):
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.drawpr = drawpr
    self.max = False
    self.pos = pos
    self.hasBorder = hasBorder
    self.clicked = False
    self.screen = pygame.surface.Surface((640,480))
    self.icons = []
    self.workingFolder = os.getcwd()+"/users/"+str(ConfigCtl.getCurrentUser())
    self.title = "File Explorer - "+ConfigCtl.getCurrentUser()
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 15)

  def initProc(self):
    self.icons = self.getIconsFromFileList(os.listdir(os.getcwd()+"/users/"+str(ConfigCtl.getCurrentUser())))
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 15)
    self.title = "File Explorer - "+ConfigCtl.getCurrentUser()
    self.shortButtons = {}
    self.shortcuts = ["Desktop","Documents","Music","Pictures","Videos"]
    self.rightClick = self.getting = self.cp = self.rname = False
    self.r = self.o = self.cd = ""
    self.file = -1
    if self.workingFolder.endswith(str(ConfigCtl.getCurrentUser())):
      self.workingFolder = os.getcwd()+"/users/"+str(ConfigCtl.getCurrentUser())
    
  def update(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        pos2 = (pos[0]-self.pos[0], pos[1]-self.pos[1])
        for icon in self.icons:
          if icon.rect.collidepoint(pos2) and event.button == 1:
            #when You click on an icon, WHAT DO WE DO????
            self.workingFolder = icon.directory
            if icon.isFile:
              if not icon.text.endswith(".py"):
                return "open "+self.workingFolder+"/"+icon.text
              #Run/Open the file however neccesary
          if icon.rect.collidepoint(pos2) and event.button == 3:
            self.file = self.icons.index(icon)
            self.rightClick = True
        if self.rightClick:
          for a in self.rButtons:
            if a.collidepoint(pos2):
              if self.rButtons.index(a) == 0:
                self.rightClick = False
              if self.rButtons.index(a) == 1:
                if "." in self.icons[self.file].text:
                  self.getting = True
                  self.cp = True
                self.rightClick = False
              if self.rButtons.index(a) == 2:
                self.getting = True
                self.rname = True
                self.o = self.icons[self.file].text
                self.rightClick = False
              if self.rButtons.index(a) == 3:
                if "." not in self.icons[self.file].text:
                  self.removeDir(self.workingFolder+"/"+self.icons[self.file].text)
                  return
                os.remove(self.workingFolder+"/"+self.icons[self.file].text)
                self.rightClick = False
            
        for b in self.shortButtons:
          if self.shortButtons[b][0].collidepoint(pos2):
            self.workingFolder = self.shortButtons[b][1]
        if self.backButton.collidepoint(pos2):
          a = self.workingFolder.split("/")
          a = a[0:-1]
          self.workingFolder = "/".join(a)
      if event.type == pygame.KEYDOWN:
        if self.getting:
          if self.cp:
            if event.key == pygame.K_RETURN:
              self.copyFile()
              self.cd = ""
              self.cp = False
              self.getting = False
              return
            self.cd = self.cd + event.unicode if event.key != pygame.K_BACKSPACE else self.cd[0:-1]
          if self.rname:
            if event.key == pygame.K_RETURN:
              os.rename(self.workingFolder+"/"+self.o, self.workingFolder+"/"+self.r)
              self.r = ""
              self.rname = False
              self.getting = False
              return
            self.r = self.r + event.unicode if event.key != pygame.K_BACKSPACE else self.r[0:-1]
            
    self.icons = self.getIconsFromFileList(os.listdir(self.workingFolder))
    if self.file != -1 and self.rname:
      self.icons[self.file].text = self.r
  
  def draw(self, screen):
    screen.fill((255,255,255))
    self.shortButtons = {}
    for a in range(len(self.icons)):
      self.icons[a].pos = [120+(90*(a%6)), 35+(75*((a-(a%6))/6))]
      self.icons[a].rect = screen.blit(self.icons[a].icon, self.icons[a].pos)
      text = self.font.render(self.icons[a].text, True, (0,0,0))
      xoff = (text.get_rect().width-40)/2
      pos = [self.icons[a].pos[0]-xoff, self.icons[a].pos[1]+45]
      screen.blit(text, pos)
    pygame.draw.rect(screen, (128,128,128), [0, 20, 100, 465], 0)
    for a in range(len(self.shortcuts)):
      #start at 60px down
      text = self.font.render(self.shortcuts[a], True, (255,255,255))
      self.shortButtons[self.shortcuts[a]] = [screen.blit(text, [5, 60+(20*a)]), os.getcwd()+"/users/"+ConfigCtl.getCurrentUser()+"/"+self.shortcuts[a]]

    self.rButtons = []
    lFont = pygame.font.SysFont(pygame.font.get_default_font(), 30)

    if self.rightClick:
      pygame.draw.rect(screen, (255,255,255), [250,150,130,135], 0)
      pygame.draw.rect(screen, (0,0,0), [250,150,130,135], 2)

      t = ["Back", "Copy", "Rename", "Delete"]
      for b in t:
        text = lFont.render(b, True, (0,0,0))
        self.rButtons.append(screen.blit(text, [260, 165+30*t.index(b)]))

    if self.getting and self.cp:
      dial = pygame.Surface((200,150))
      dial.fill((128,128,128))
      pygame.draw.rect(dial, (0,0,0), [0,0,199,149], 2)
      DrawLib.inputBox(dial, (255,255,255), (0,0,0), [20, 30, 160, 30], 2)
      text = lFont.render(self.cd, True, (0,0,0))
      if text.get_rect().width > 160:
        text = self.getShorterText(self.cd, lFont, 150)
      dial.blit(text, [25, 32])
      screen.blit(dial, [260, 150])
    
    self.backButton = pygame.draw.rect(screen, (90,90,90), [5, 25, 90, 25], 0)
    text = self.font.render("Back", True, (255,255,255))
    screen.blit(text, [35, 32])
    screen.blit(pygame.image.load("sysobj/back.png").convert_alpha(), [8, 27])
    return screen

  def getIconsFromFileList(self, files):
    icons = []
    for f in files:
      if f.endswith(".pt") or f.endswith(".txt"):
        #Add plaintext icon
        icons.append(Icon("sysobj/textdoc.png", f, True, self.workingFolder))
      elif "." not in f:
        #add a folder icon
        icons.append(Icon("sysobj/folder.png", f, False, self.workingFolder))
      else:
        #add generic icon (Temporary Until after due)
        icons.append(Icon("sysobj/generic.png", f, True, self.workingFolder))
    return icons

  def setOpen(self, file):
    self.workingFolder = file
    pass

  def removeDir(self, dire):
    for a in os.listdir(dire):
      if "." not in a:
        self.removeDir(dire+a)
      else:
        os.remove(dire+a)
    os.rmdir(dire)

  def getShorterText(self, text, font, w):
    for a in range(len(text)):
      if font.render(text[a:], True, (0,0,0)).get_rect().width <= w:
        return font.render(text[a:], True, (0,0,0))
  
  def copyFile(self):
    with open(os.getcwd()+self.cd, "wb") as f:
      with open(self.workingFolder+"/"+self.icons[self.file].text, "rb") as f2:
        t = f2.read()
      f.write(t)
    
