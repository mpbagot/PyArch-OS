import pygame

class Icon():
  def __init__(self, icon, name, isFile, directory):
    self.icon = pygame.transform.scale(pygame.image.load(icon).convert_alpha(), [40,40])
    self.text = name
    self.pos = [0,0]
    self.directory = directory
    self.isFile = isFile
    if not self.isFile:
      self.directory = directory+"/"+name
    self.isText = name.endswith(".pt")
    
  def __str__(self):
    return self.rect
