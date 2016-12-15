import pygame
import SysProgram

def checkWindowMovement(program, events):
  for event in events:
    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      pos2 = (pos[0]-program.pos[0], pos[1]-program.pos[1])
      if program.sysCtls[1].collidepoint(pos2):
        return False
      elif program.sysCtls[0].collidepoint(pos2):
        if program.clicked == False:
          program.clicked = True
          program.drawpr = 2
          program.ipos = pos
  if pygame.mouse.get_pressed()[0]:
    pos = pygame.mouse.get_pos()
    if program.clicked:
      xch = pos[0]-program.ipos[0]
      ych = pos[1]-program.ipos[1]
      program.pos = (program.pos[0]+xch, program.pos[1]+ych)
      program.ipos = pos
  else:
    program.clicked = False
    program.ipos = (0,0)

def checkWindowPriority(program, programs, events):
  for event in events:
    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      pos2 = (pos[0]-program.pos[0], pos[1]-program.pos[1])
      rect = program.screen.get_rect()
      if rect.collidepoint(pos2) and onlyCollidesHere(programs, pos, program):
        program.drawpr = 2
        if not onlyProgramOnLayer(programs, program):
          for p in programs:
            if p != program and not isinstance(p, SysProgram.Homebar) and not isinstance(p, SysProgram.Desktop) and p.drawpr < 13:
              p.drawpr += 1

def onlyCollidesHere(programs, pos, p):
  checkers = []
  for a in programs:
    if a.drawpr <= p.drawpr and a != p:
      checkers.append(a)
  for a in checkers:
    pos2 = (pos[0]-a.pos[0],pos[1]-a.pos[1])
    if a.screen.get_rect().collidepoint(pos2):
      return False
  return True

def onlyProgramOnLayer(progs, p):
  layer = p.drawpr
  for a in progs:
    if a.drawpr == layer:
      return False
  return True
