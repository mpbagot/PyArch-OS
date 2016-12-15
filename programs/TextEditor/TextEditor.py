import pygame
import DrawLib
import os

class TextEditor:
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.pos = pos
    self.drawpr = drawpr
    self.hasBorder = hasBorder
    self.max = isMax
    self.screen = pygame.Surface((640, 480))
    self.title = "Text Editor"
    self.clicked = False

  def initProc(self):
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    self.textpos = [0,0]
    self.saving = False
    self.saveInput = ""
    self.text = "DEFAULT"
    try:
      with open(self.file) as file:
        self.text = file.read()
        file.close()
      towrite = self.text.split("\n")
      self.towrite = [[b for b in a] for a in towrite]
    except:
      self.towrite = [['']]
      pass
    pass

  def update(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        if not self.saving:
          if event.key == pygame.K_LEFT and self.textpos[0] > 0:
            self.textpos[0] -= 1
          elif event.key == pygame.K_RIGHT and self.textpos[0] < len(self.towrite[self.textpos[1]]):
            self.textpos[0] += 1
          elif event.key == pygame.K_UP and self.textpos[1] > 0:
            self.textpos[1] -= 1
            if self.textpos[0] > len(self.towrite[self.textpos[1]]):
              self.textpos[0] = len(self.towrite[self.textpos[1]])
          elif event.key == pygame.K_DOWN and self.textpos[1] < len(self.towrite)-1:
            self.textpos[1] += 1
            if self.textpos[0] > len(self.towrite[self.textpos[1]]):
              self.textpos[0] = len(self.towrite[self.textpos[1]])

          #add any typed characters to the textbox at the correct location
          elif event.key == pygame.K_DELETE:
            if self.textpos[0] == len(self.towrite[self.textpos[1]]) and self.textpos[1] < len(self.towrite)-1:
              self.towrite[self.textpos[1]] += self.towrite[self.textpos[1]+1]
              del self.towrite[self.textpos[1]+1]
            elif len(self.towrite[self.textpos[1]]) > 0:
              self.towrite[self.textpos[1]].pop(self.textpos[0])

          elif event.key == pygame.K_BACKSPACE and self.textpos != [0,0]:
            if self.textpos[0] == 0:
              self.towrite[self.textpos[1]-1] += self.towrite[self.textpos[1]]
              del self.towrite[self.textpos[1]]
            else:
              self.towrite[self.textpos[1]].pop(self.textpos[0]-1)
              self.textpos[0] -= 1
          
          elif event.key == pygame.K_RETURN:
            nline = self.towrite[self.textpos[1]][self.textpos[0]:]
            self.towrite.insert(self.textpos[1]+1, nline)
            self.towrite[self.textpos[1]] = self.towrite[self.textpos[1]][0:self.textpos[0]]
            self.textpos = [0, self.textpos[1]+1]
          
          else:
            self.towrite[self.textpos[1]].insert(self.textpos[0], event.unicode)
            self.textpos[0] += 1
        else:
          if event.key != pygame.K_RETURN:
            self.saveInput = self.saveInput+event.unicode if event.key != pygame.K_BACKSPACE else self.saveInput[0:-1]
          else:
            self.file = os.getcwd()+self.saveInput
            self.saving = False
            self.saveFile()
          
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        pos2 = (pos[0]-self.pos[0], pos[1]-self.pos[1])
        pos3 = (pos2[0]-120, pos2[1]-140)
        if self.saveButton.collidepoint(pos2):
          if self.checkSave():
            self.saveFile()
          else:
            self.saving = True
        elif self.saving:
          if self.dialExit.collidepoint(pos3):
            self.saving = False
          elif self.saveConfirm.collidepoint(pos3):
            self.file = os.getcwd()+self.saveInput
            self.saving = False
            self.saveFile()
          

  def draw(self, screen):
    screen.fill((255,255,255))
    for line in self.towrite:
      line2 = ''.join(line)
      text = self.font.render(line2, True, (0,0,0))
      screen.blit(text, [5, 53+(18*self.towrite.index(line))])
    x = self.font.render(''.join(self.towrite[self.textpos[1]][0:self.textpos[0]]), True, (255,255,255)).get_rect().width+5
    #draw the line here
    pygame.draw.rect(screen, (0,0,0), [x, 53+(18*self.textpos[1])-1, 2, 15], 0)
    pygame.draw.rect(screen, (128,128,128), [2, 20, 640, 30], 0)
    
    #Draw the buttons and stuff here
    self.saveButton = pygame.draw.rect(screen, (32,32,32), [2, 20, 50, 30], 0)
    text = self.font.render("Save", True, (255,255,255))
    screen.blit(text, [10, 28])
    
    #Draw the save dialogue here
    if self.saving:
      dialogue = pygame.Surface((400, 200))
      dialogue.fill((200,200,200))
      self.dialExit = DrawLib.drawWindowBorderSurface((400,200), dialogue)
      text = self.font.render("Save As...", True, (255,255,255))
      dialogue.blit(text, [10, 2])

      DrawLib.inputBox(dialogue, (255,255,255), (0,0,0), [75, 80, 250, 20], 1)
      text = self.font.render(self.saveInput, True, (0,0,0))
      dialogue.blit(text, [78, 82])
      
      self.saveConfirm = pygame.draw.rect(dialogue, (255,255,255), [300, 150, 50, 25], 0)
      text = self.font.render("Save!", True, (0,0,0))
      dialogue.blit(text, [305, 155])

      screen.blit(dialogue, [120, 140])
    
    return screen

  def quitProc(self):
    pass

  def setOpen(self, file):
    file = file[len(os.getcwd())+1:]
    self.file = file

  def saveFile(self):
    write = [''.join(a) for a in self.towrite]
    with open(self.file, "w") as file:
      file.write('\n'.join(write))
      file.close()

  def checkSave(self):
    if self.text == "DEFAULT":
      return False
    return True
      
