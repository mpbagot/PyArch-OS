import pygame
import ConfigCtl
import random
try:
  from mutagen.id3 import ID3
  from mutagen.mp3 import MP3
  from mutagen.oggvorbis import OggVorbis
except:
  pass
import os

class BoomBox:
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.pos = pos
    self.drawpr = drawpr
    self.hasBorder = hasBorder
    self.max = isMax
    self.screen = pygame.Surface((640, 480))
    self.controlBar = pygame.Surface((640, 100))
    self.musicList = pygame.Surface((340, 360))
    self.albumInfo = pygame.Surface((300, 360))
    self.playingFile = ""
    self.title = "BoomBox Music Player"
    self.clicked = False

  def initProc(self):
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
    self.folder = os.getcwd()+"/users/"+ConfigCtl.getCurrentUser()+"/Music/"
    self.files = self.getFileDictionary()
    self.sortedFiles = []
    for a in os.listdir(self.folder):
      if a.endswith(".mp3") or a.endswith(".ogg"):
        self.sortedFiles.append(a)
    self.selectedIndex = 0
    self.playing = False
    self.paused = False
    self.yOffset = 0
    pygame.mixer.music.set_endevent(pygame.VIDEOEXPOSE)

  def update(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        pos2 = (pos[0]-self.pos[0], pos[1]-self.pos[1])
        pos3 = (pos2[0], pos2[1]-380)
        pos4 = (pos2[0], pos2[1]-20-self.yOffset)
        if event.button not in (4,5):
          if self.playButton.collidepoint(pos3):
            if not self.playing:
              self.playSong()
            elif self.paused:
              pygame.mixer.music.unpause()
              self.paused = False
            else:
              pygame.mixer.music.pause()
              self.paused = True

          if self.forwardButton.collidepoint(pos3) and self.selectedIndex < len(self.files)-1:
            self.selectedIndex += 1
            self.playSong()
            self.paused = False
          if self.backButton.collidepoint(pos3):
            if pygame.mixer.music.get_pos() < 5000 and self.selectedIndex > 0:
              self.selectedIndex -= 1
              self.playSong()
              self.paused = False
            else:
              self.playSong()
          for b in self.listButtons:
            if b.collidepoint(pos4):
              y = (pos4[1]+(18-pos4[1]%18))/18
              if int(y-1) == self.selectedIndex:
                self.playSong()
              self.selectedIndex = int(y)-1
        if len(self.files) > 20 and self.musicList.get_rect().collidepoint(pos4):
          h = len(self.files)*20
          if event.button == 4 and self.yOffset < 0:
            self.yOffset += 8
          elif event.button == 5 and h+self.yOffset > 405:
            self.yOffset -= 8
      if event.type == pygame.VIDEOEXPOSE:
        self.selectedIndex = random.randint(0, len(self.files)-1)
        self.playSong()
        self.paused = False    

  def draw(self, screen):
    self.listButtons = []
    screen.fill((255,255,255))
    self.controlBar.fill((223,223,255))
    self.musicList.fill((223,223,192))
    self.albumInfo.fill((172,172,192))

    pygame.draw.polygon(self.albumInfo, (192,192, 172), [[150, 0], [300, 0], [300, 150], [150, 360], [0, 360], [0, 210], [150, 0]], 0)
    pygame.draw.polygon(self.controlBar, (223,223,192), [[445, 0], [250, 0], [250, 50], [275, 100], [500, 100], [445,0]], 0)

    length = 0
    if self.playingFile != "":
      if self.playingFile not in self.files:
        tags = self.getTags()
      else:
        tags = self.files[self.playingFile]
      try:
        text = self.font.render(tags["Title"], True, (0,0,0))
      except:
        text = self.font.render(self.playingFile.split("/")[-1], True, (0,0,0))
      self.controlBar.blit(text, [260, 15])
      try:
        text = self.font.render("By "+tags["Artist"], True, (0,0,0))
      except:
        text = self.font.render("By Unknown", True, (0,0,0))
      self.controlBar.blit(text, [264, 35])
      t = pygame.mixer.music.get_pos()/1000
      s = str(int(t%60)) if len(str(int(t%60))) == 2 else "0"+str(int(t%60))
      ms = ((t-t%60)/60, s)
      text = self.font.render(str(int(ms[0]))+":"+s, True, (0,0,0))
      self.controlBar.blit(text, [595, 70])
      try:
        length = t/(self.files[self.sortedFiles[self.selectedIndex]]["Length"])
      except:
        length = 0
      pygame.draw.rect(self.controlBar, (255,255,64), [280, 70, 300*length, 8], 0)
    pygame.draw.rect(self.controlBar, (0,0,0), [280, 70, 300, 8], 1)
    pygame.draw.rect(self.controlBar, (0,52,255), [280+(300*length)-2, 65, 4, 18], 0)

    if len(self.files) > 0:
      tags = self.files[self.sortedFiles[self.selectedIndex]]
      try:
        text = self.font.render("Title: "+tags["Title"], True, (0,0,0))
      except:
        text = self.font.render("Title: Unknown", True, (0,0,0))
      self.albumInfo.blit(text, [15, 10])
      
      #self.albumInfo.blit(cover, [15,30])
      #Blit the album cover here
      pygame.draw.rect(self.albumInfo, (0,0,0), [15, 30, 180, 180], 2)
      try:
        text = self.font.render("Album: "+tags["Album"], True, (0,0,0))
      except:
        text = self.font.render("Album: Unknown", True, (0,0,0))
      self.albumInfo.blit(text, [15, 225])
      try:
        text = self.font.render("Artist: "+tags["Artist"], True, (0,0,0))
      except:
        text = self.font.render("Artist: Unknown", True, (0,0,0))
      self.albumInfo.blit(text, [15, 250])
      try:
        text = self.font.render("Track No: "+tags["Track"], True, (0,0,0))
      except:
        text = self.font.render("Track No: Unknown", True, (0,0,0))
      self.albumInfo.blit(text, [15, 275])
      try:
        text = self.font.render("Genre: "+tags["Genre"], True, (0,0,0))
      except:
        text = self.font.render("Genre: Unknown", True, (0,0,0))
      self.albumInfo.blit(text, [15, 300])

      #Display the song list on the left
      for song in self.sortedFiles:
        if self.sortedFiles.index(song)%2 == 1:
          pygame.draw.rect(self.musicList, (192,192,223), [5, 18*self.sortedFiles.index(song)+self.yOffset, 340, 20], 0)
        if self.sortedFiles.index(song) == self.selectedIndex:
          pygame.draw.rect(self.musicList, (192,192,192), [5, 18*self.sortedFiles.index(song)+self.yOffset, 340, 20], 0)
        try:
          text = self.font.render(self.files[song]["Artist"]+" - "+self.files[song]["Title"], True, (0,0,0))
        except:
          text = self.font.render("Unknown - "+self.playingFile.split("/")[-1], True, (0,0,0))
        self.listButtons.append(self.musicList.blit(text, [5, 3+18*self.sortedFiles.index(song)+self.yOffset]))

    back = pygame.Surface((80, 100))
    back.fill((255,255,192))
    pygame.draw.rect(back, (0,0,0), [0,0,80,100], 2)

    play = pygame.Surface((90, 100))
    play.fill((255,255,192))
    pygame.draw.rect(play, (0,0,0), [0,0,90,100], 1)
    
    forward = pygame.Surface((80, 100))
    forward.fill((255,255,192))
    pygame.draw.rect(forward, (0,0,0), [0,0,80,100], 1)

    #TODO: Fill in the designs on these buttons!!!
    #(98,98,255)
    pygame.draw.lines(back, (128,128,128), False, [[20,25],[20,75],[20, 50],[40, 25], [40, 75], [20, 50], [40,75], [40,50], [60,25], [60, 75], [40, 50]], 5)
    pygame.draw.lines(play, (128,128,128), False, [[20, 25],[20, 75],[45, 50],[20,25]], 5)
    pygame.draw.lines(play, (128,128,128), False, [[50, 25], [50, 75]], 8)
    pygame.draw.lines(play, (128,128,128), False, [[65, 25], [65, 75]], 8)
    pygame.draw.lines(forward, (128,128,128), False, [[60,25],[60,75],[60, 50],[40, 25], [40, 75], [60, 50], [40,75], [40,50], [20,25], [20, 75], [40, 50]], 5)

    self.backButton = self.controlBar.blit(back, [0, 0])
    self.playButton = self.controlBar.blit(play, [80, 0])
    self.forwardButton = self.controlBar.blit(forward, [170, 0])
    
    pygame.draw.rect(self.musicList, (0,0,0), [0, -3, 340, 600], 2)
    pygame.draw.rect(self.controlBar, (0,0,0), [-5, 0, 1000, 110], 2)

    screen.blit(self.controlBar, [0, 380])
    screen.blit(self.musicList, [0, 20])
    screen.blit(self.albumInfo, [340, 20])
    return screen

  def quitProc(self):
    pygame.mixer.music.stop()
    pass

  def setOpen(self, file):
    self.playSong(file)

  def playSong(self, file=""):
    if file == "":
      file = self.folder+self.sortedFiles[self.selectedIndex]
      self.playingFile = self.sortedFiles[self.selectedIndex]
    else:
      self.playingFile = file
    try:
      pygame.mixer.music.load(file)
      pygame.mixer.music.play()
      self.playing = True
    except:
      print("An Error Occured when Playing that file.")
      
  def getFileDictionary(self):
    f = {}
    for audio in os.listdir(self.folder):
      tags = {}
      if audio.endswith(".mp3"):
        try:
          a = ID3(self.folder+audio)
          a2 = MP3(self.folder+audio)
        except:
          pass
        try:
          tags["Length"] = int(a2.info.length)
        except:
          pass
        try:
          tags["Artist"] = a["TPE1"].text[0]
        except:
          tags["Artist"] = "Unknown"
        try:
          tags["Album"] = a["TALB"].text[0]
        except:
          tags["Album"] = "Unknown"
        try:
          tags["Title"] = a["TIT2"].text[0]
        except:
          tags["Title"] = audio.split(".")[0]
        try:
          tags["Track"] = a["TRCK"].text[0]
        except:
          tags["Track"] = "Unknown"
        try:
          tags["Genre"] = a["TCON"].text[0]
        except:
          tags["Genre"] = "Unknown"
        try:
          tags["Year"] = a["TDRC"].text[0]
        except:
          tags["Year"] = "Unknown"

      if audio.endswith(".ogg"):
        try:
          a = OggVorbis(self.folder+audio)
          tags["Length"] = int(a.info.length)
          for t in a.tags:
            if t[0] == "ARTIST":
              tags["Artist"] = t[1]
            if t[0] == "ALBUM":
              tags["Album"] = t[1]
            if t[0] == "TRACKNUMBER":
              tags["Track"] = t[1]
            if t[0] == "TITLE":
              tags["Title"] = t[1]
            if t[0] == "GENRE":
              tags["Genre"] = t[1]
            if t[0] == "DATE":
              tags["Year"] = t[1]
        except:
          pass

      f[audio] = tags
    return f

  def getTags(self):
    tags = {}
    audio = self.playingFile.split("/")[-1]
    try:
      a = ID3(self.playingFile)
      a2 = MP3(self.playingFile)
      tags["Length"] = int(a2.info.length)
      try:
        tags["Artist"] = a["TPE1"].text[0]
      except:
        tags["Artist"] = "Unknown"
      try:
        tags["Album"] = a["TALB"].text[0]
      except:
        tags["Album"] = "Unknown"
      try:
        tags["Title"] = a["TIT2"].text[0]
      except:
        tags["Title"] = audio.split(".")[0]
      try:
        tags["Track"] = a["TRCK"].text[0]
      except:
        tags["Track"] = "Unknown"
      try:
        tags["Genre"] = a["TCON"].text[0]
      except:
        tags["Genre"] = "Unknown"
      try:
        tags["Year"] = a["TDRC"].text[0]
      except:
        tags["Year"] = "Unknown"
    except:
      try:
        a = OggVorbis(self.playingFile)
        tags["Length"] = int(a.info.length)
        for t in a.tags:
          if t[0] == "ARTIST":
            tags["Artist"] = t[1]
          if t[0] == "ALBUM":
            tags["Album"] = t[1]
          if t[0] == "TRACKNUMBER":
            tags["Track"] = t[1]
          if t[0] == "TITLE":
            tags["Title"] = t[1]
          if t[0] == "GENRE":
            tags["Genre"] = t[1]
          if t[0] == "DATE":
            tags["Year"] = t[1]
      except:
        pass
    
    return tags
