import Workspace
import UserCred
import LoginWorkspace
import ConfigCtl
import os
import pygame

class EventSystem:
  def __init__(self, windows = 4, logIn = False):
    self.screen = self.initGUI()
    ##If no login instance passed to EventSystem
    if logIn == False:
      ##Run a temp workspace for logging in
      ConfigCtl.setupLogin(self.desktopInit(self.screen))
    self.workspaces = [Workspace.Workspace(a, logIn, self.screen) for a in range(windows)]
    self.activeWS = 0
    while self.onTickUpdate() != False:
      self.onTickUpdate()
    ConfigCtl.cleanConfig()

  def onTickUpdate(self):
    ##Update each workspace and redraw the active workspace
    a = 0
    while a < len(self.workspaces):
      if self.workspaces[a].isQuitting():
        del self.workspaces[a]
        self.activeWS = 0
      if self.workspaces[a].shouldShutdown():
        pygame.quit()
        return False
      a += 1
    self.workspaces[self.activeWS].update()
    self.workspaces[self.activeWS].redraw()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and (keys[pygame.K_RALT] or keys[pygame.K_LALT]):
      if keys[pygame.K_RIGHT] and self.activeWS < len(self.workspaces)-1:
        self.activeWS += 1
      elif keys[pygame.K_LEFT] and self.activeWS > 0:
        self.activeWS -= 1
    if len(self.workspaces) == 0:
      return False
    self.clock.tick(30)
##    self.onTickUpdate()

  def initGUI(self):
    ##initialise the gui engine / Pygame
    pygame.init()
    self.clock = pygame.time.Clock()
    pygame.display.set_caption("PyArch V0.35")
    return pygame.display.set_mode((1024, 768))#, pygame.FULLSCREEN)

  def desktopInit(self, screen):
    ##get login credentials with a login screen
    tempws = LoginWorkspace.LoginWorkspace(screen)
    return tempws.getLogin(self.clock)
