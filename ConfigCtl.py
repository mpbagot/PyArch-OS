import pygame
import os
import EventSystem
import SysProgram
from programs import ProgramCache

def getWallpaper():
  lines = [a.strip() for a in open("config/config.pt")]
  return pygame.image.load(lines[3]).convert_alpha()

def getInstalledPrograms():
  with open("config/programs.pt") as file:
    text = file.read()
    file.close()
  lines = text.split("\n")
  p1 = lines[0].split(",")
  p2 = lines[1].split(",")
  return p1+p2

def getDockedPrograms():
  with open("config/programs.pt") as file:
    text = file.read()
    file.close()
  lines = text.split("\n")
  p2 = lines[1].split(",")
  return p2

def installProgram(program):
  with open("config/programs.pt", "w") as file:
    text = file.read()
    lines = text.split("\n")
    lines[0][0] += ","+program
    file.write("\n".join(lines))
    file.close()

def dockProgram(program):
  with open("config/programs.pt", "w") as file:
    text = file.read()
    text += ","+program
    file.write(text)
    file.close()

def getCurrentUser():
  with open("config/tempLogin.pt") as file:
    text = file.read()
    file.close()
  return text

def setupLogin(user):
  with open("config/tempLogin.pt", "w") as file:
    file.write(str(user))
    file.close()
  #make a file, add logged in user to it.

def cleanConfig():
  os.remove("config/tempLogin.pt")
  #Remove any temporary config files at shutdown

def getProgramForFile(name, length):
  if name.endswith(".pt"):
    prog = getattr(ProgramCache, "TextEditor")
    return getattr(prog, "TextEditor")((15*(length-2), 15*(length-2)), 2, True, False)
  elif name.endswith(".mp3") or name.endswith(".ogg"):
    prog = getattr(ProgramCache, "BoomBox")
    return getattr(prog, "BoomBox")((15*(length-2), 15*(length-2)), 2, True, False)
  return SysProgram.FileExplorer((15*(length-2), 15*(length-2)), 2, True, False)

def getSysTitleFont():
  return pygame.font.SysFont(pygame.font.get_default_font(), 18)

def getProgram(name, length):
  if name == "FileExplorer":
    return SysProgram.FileExplorer((15*(length-2), 15*(length-2)), 2, True, False) 
##  try:
  prog = getattr(ProgramCache, name)
  return getattr(prog, name)((15*(length-2), 15*(length-2)), 2, True, False)
##  except:
##    pass

def getAllUsers():
  up = {}
  with open("user.pt") as f:
    t = f.read().split("\n")
  for a in t:
    a = a.split(",")
    up[a[0]] = a[1]
  return up

def rmUser(uname):
  with open("user.pt") as f:
    t = f.read().split("\n")
  with open("user.pt", "w") as f:
    for a in t:
      if a.startswith(uname):
        del t[t.index(a)]
    f.write("\n".join(t))
  removeUserDirs(uname)

def addUser(uname):
  with open("user.pt") as f:
    t = f.read().split("\n")
  with open("user.pt", "w") as f:
    t.append(uname+",,"+str(len(t)))
    f.write("\n".join(t))
  makeDirs(uname)

def makeDirs(uname):
  try:
    os.mkdir(os.getcwd()+"/users/"+uname)
    os.mkdir(os.getcwd()+"/users/"+uname+"/Desktop")
    os.mkdir(os.getcwd()+"/users/"+uname+"/Documents")
    os.mkdir(os.getcwd()+"/users/"+uname+"/Music")
    os.mkdir(os.getcwd()+"/users/"+uname+"/Pictures")
    os.mkdir(os.getcwd()+"/users/"+uname+"/Videos")
  except:
    pass

def removeUserDirs(uname, dire="/"):
  for a in os.listdir(os.getcwd()+"/users/"+uname+dire):
    try:
      if "." in a:
        os.remove(os.getcwd()+"/users/"+uname+dire+a)
        #remove file
      else:
        removeUserDirs(uname, dire+"/"+a)
        os.rmdir(os.getcwd()+"/users/"+uname+dire+a)
        #recurse into folder then remove
    except:
      pass
  os.rmdir(os.getcwd()+"/users/"+uname)
