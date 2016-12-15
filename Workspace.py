from multiprocessing.dummy import Pool
import SysProgram
import WindowMan
import ConfigCtl
import DrawLib
import pygame

class Workspace:
  def __init__(self, index, userCred, screen):
    self.user = userCred
    self.index = index
    self.shutDown = False
    self.programs = [SysProgram.Homebar((0,720), 1, False, True), SysProgram.Desktop((0,0),15, False, True)]
    for a in self.programs:
      a.initProc()
    self.screen = screen

  def isQuitting(self):
    return False
    ##TODO: check for quit signal

  def shouldShutdown(self):
    return self.shutDown
  
  def updateProc(self, program):
    if program.drawpr < 3 or isinstance(program, SysProgram.Desktop):
      if isinstance(program, SysProgram.Desktop):
        response = program.update(self.events, self.programs)
      else:
        response = program.update(self.events)
      if response == "shutdown":
        self.shutDown = True
      if response == "quit":
        program.quitProc()
        self.programs.remove(program)
        del program
        return
      if response != None and response.startswith("open"):
        r = response[5:]
        r2 = r.split("/")
        p = ConfigCtl.getProgramForFile(r2[-1], len(self.programs))
        sweet = False
        print(type(p).__name__)
        for p2 in self.programs:
          if type(p).__name__ == type(p2).__name__ and type(p).__name__ != "TextEditor":
            p2.setOpen(r)
            sweet = True
        if not sweet:
          p.setOpen(r)
          self.runProgram(p)
      if response != None and response.startswith("run"):
        r = response.split()
        self.runProgram(ConfigCtl.getProgram(r[1], len(self.programs)))
    if program.hasBorder and WindowMan.checkWindowMovement(program, self.events) == False:
      program.quitProc()
      self.programs.remove(program)
      #del program
      return
    if program.hasBorder == True:
      WindowMan.checkWindowPriority(program, self.programs, self.events)
    
  def update(self):
    self.events = pygame.event.get()
    try:
      pool = Pool(len(self.programs))
      pool.map(self.updateProc, self.programs)
      pool.close()
      pool.join()
    except:
      pass
    
  def redraw(self):
    self.screen.fill((255,255,255))
    for a in self.sortProgramsByDrawPriority():
      s = a.draw(a.screen)
      if a.hasBorder:
        a.sysCtls = DrawLib.drawWindowBorder((640,480) if a.max == False else (1024, 720), a)
        DrawLib.drawTitle(a.title, a)
      self.screen.blit(s, a.pos)
    pygame.display.flip()

  def runProgram(self, program):
    self.programs.append(program)
    self.programs[-1].initProc()

  def sortProgramsByDrawPriority(self):
    p2 = [[] for a in range(16)]
    for p in self.programs:
      p2[p.drawpr].append(p)
    p3 = []
    for a in p2:
      for b in a:
        p3.append(b)
    p3.reverse()
    ##sort and return programs
    return p3
