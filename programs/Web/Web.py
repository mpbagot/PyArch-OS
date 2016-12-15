import pygame
import threading
import os
import urllib.request
from urllib.error import HTTPError, URLError
from html.parser import HTMLParser
from html.entities import name2codepoint

class Web:
  def __init__(self, pos, drawpr, hasBorder, isMax):
    self.pos = pos
    self.drawpr = drawpr
    self.hasBorder = hasBorder
    self.max = True
    self.title = "Archon Web Browser"
    self.screen = pygame.Surface((1024, 720))
    self.pageScreen = pygame.Surface((1014, 595))

  def initProc(self):
    self.clearTemp()
    try:
      os.rmdir(os.getcwd()+"/programs/Web/temp/")
      
    except:
      pass
    os.mkdir(os.getcwd()+"/programs/Web/temp/")
    self.parser = MyHTMLParser()
    self.parser.setWebObject(self)
    self.parser.preTag = "html"
    self.yOffset = 0
    self.input = 0
    self.url = ""
    self.history = []
    self.noNetwork = False
    self.newTab = True
    self.needProxy = False
    self.tabTitle = "New Tab"
    self.font = pygame.font.SysFont(pygame.font.get_default_font(), 30)
    self.document = HTMLDocument(self)
    self.document.head = HTMLHead()
    self.document.body = HTMLBody()

  def update(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        pos2 = (pos[0]-self.pos[0], pos[1]-self.pos[1])
        if self.reloadButton.collidepoint(pos2):
          if len(self.history) >= 1:
            self.url = self.history[-1]
          self.loadPage()
        if self.urlBox.collidepoint(pos2):
          self.input = 1
        if self.backButton.collidepoint(pos2):
          if len(self.history) >= 2:
            self.url = self.history[-2]
            self.loadPage()
        if self.homeButton.collidepoint(pos2):
          self.url = "http://www.duckduckgo.com"
          self.loadPage()

      if event.type == pygame.KEYDOWN and self.input != 0:
        if self.input == 1 and event.key == pygame.K_RETURN:
          self.input = 0
          self.loadPage()
        if self.input == 1:
          self.url = self.url+event.unicode if event.key != pygame.K_BACKSPACE else self.url[0:-1]
    pass

  def draw(self, screen):
    screen.fill((255,255,255))
    self.pageScreen.fill((255,255,255))

    pygame.draw.rect(screen, (0,0,0), [3, 25, 150, 45], 0)
    pygame.draw.rect(screen, (0,0,0), [3, 70, 1024, 50], 0)
    pygame.draw.rect(screen, (255,255,255), [4, 26, 148, 45], 0)
    pygame.draw.rect(screen, (255,255,255), [3, 71, 1024, 49], 0)

    text = self.font.render(self.tabTitle, True, (0,0,0))
    if text.get_rect().width > 124:
      text = self.getShorterTitle()
    screen.blit(text, [12, 36])

    urlbar = pygame.image.load("programs/Web/urlbar.png").convert_alpha()
    self.urlBox = screen.blit(urlbar, [55, 80])

    if self.input == 1 and pygame.time.get_ticks()%10 < 5:
      pygame.draw.rect(screen, (0,0,0), [880, 84, 2, 28], 0)

    text = self.font.render(self.url, True, (0,0,0))
    if text.get_rect().width > 810:
      text = self.getShorterURL()
    screen.blit(text, [880-text.get_rect().width, 88])

    reload = pygame.Surface((45,45))
    reload.fill((255,255,255))
    pygame.draw.circle(reload, (96,96,96), (22,22), 17, 3)
    pygame.draw.lines(reload, (96,96,96), False, [[30, 18], [37, 26], [44, 18]], 4)
    self.reloadButton = screen.blit(reload, [967, 76])

    home = pygame.Surface((45,45))
    home.fill((255,255,255))
    pygame.draw.lines(home, (96,96,96), False, [[10, 35],[10, 20],[4, 20], [23, 1], [41, 20], [35, 20], [35, 35], [10,35]], 4)
    self.homeButton = screen.blit(home, [907, 79])

    if self.noNetwork:
      text = pygame.font.SysFont(pygame.font.get_default_font(), 50).render("Network Error!", True, (0,0,0))
      self.pageScreen.blit(text, [50, 50])
      text = self.font.render("Please check your network configuration and try again.", True, (0,0,0))
      self.pageScreen.blit(text, [55, 90])
    elif self.newTab:
      text = self.font.render("Welcome to the Archon Web Browser!", True, (0,0,0))
      x = (self.pageScreen.get_rect().width-1)/2-int(text.get_rect().width/2)
      self.pageScreen.blit(text, [x, 400])
      image = pygame.image.load("programs/Web/image.png").convert_alpha()
      x = (self.pageScreen.get_rect().width-1)/2-int(image.get_rect().width/2)
      self.pageScreen.blit(image, [x, 25])

    if self.needProxy:
      pygame.draw.rect(self.pageScreen, (0,0,0), [407, 0, 200, 175], 1)
    
    self.backButton = pygame.draw.lines(screen, (128,128,128), False, [[30, 80], [20, 97], [30, 114]], 3)

    #Display the webpage here
    self.displayWebpage()
    
    screen.blit(self.pageScreen, [5, 120])
    return screen

  def loadPage(self):
    self.document = HTMLDocument(self)
    self.history.append(self.url)
    self.newTab = False
    self.clearTemp()
    if not self.url.startswith("http://"):
      self.url = "http://"+self.url
    try:
      thread = threading.Thread(target=self.downloadPage)
      thread.start()
      self.noNetwork = False
    except urllib.error.HTTPError as e:
      if e.code == 407:
        self.needProxy = True
        return
      print(e.code)
      self.parser.feed(str(e.read()))
    except urllib.error.URLError:
      self.noNetwork = True
      self.tabTitle = "Network Error!"

  def displayWebpage(self, obj=""):
    if obj == "":
      obj = self.document.body

    if obj != None:
      if not isinstance(obj, HTMLBody) and not isinstance(obj, HTMLHead) and len(obj.objects) == 0:
        obj.render(self.pageScreen)
        #Display the individual object here

      try:
        for o in obj.objects:
          displayWebpage(o)
      except:
        pass
    pass
    #Recursively display all HTML objects here

  def quitProc(self):
    self.clearTemp()
    try:
      os.rmdir(os.getcwd()+"/programs/Web/temp/")
    except:
      pass

  def clearTemp(self):
    try:
      for file in os.listdir(os.getcwd()+"/programs/Web/temp/"):
        os.remove(os.getcwd()+"/programs/Web/temp/"+file)
    except:
      pass


  def downloadPage(self):
    self.html = ""
    try:
      self.html = urllib.request.urlopen(self.url).read()
    except urllib.error.HTTPError as e:
      if e.code == 407:
        self.needProxy = True
        return
      print(e.code)
      self.parser.feed(str(e.read()))
    except urllib.error.URLError:
      self.noNetwork = True
      self.tabTitle = "Network Error!"
    self.html = str(self.html)
    self.parser.feed(self.html)

  def getShorterTitle(self):
    for i in range(1, len(self.tabTitle)):
      text = self.font.render(self.tabTitle[0:-i]+"..", True, (0,0,0))
      if text.get_rect().width <= 124:
        return text

  def getShorterURL(self):
    for i in range(len(self.url)):
      text = self.font.render(self.url[i:], True, (0,0,0))
      if text.get_rect().width <= 810:
        return text

  def getResource(self, file):
    if not file.startswith("http://"):
      file = self.url+file
    try:
      urllib.request.urlretrieve(file, os.getcwd()+"/programs/Web/temp/"+file.split("/")[-1])
    except:
      try:
        urllib.request.urlretrieve(file, os.getcwd()+"/programs/Web/temp/"+file.split("/")[-1])
      except:
        pass

class MyHTMLParser(HTMLParser):
  def handle_starttag(self, tag, attrs):
    if tag == "script" or tag == "link":
      for a in attrs:
        if a[0] == "href":
          thread2 = threading.Thread(target=self.web.getResource, args=[a[1]])
          thread2.start()
        if a[0] == "src":
          thread2 = threading.Thread(target=self.web.getResource, args=[a[1]])
          thread2.start()
    if tag == "meta":
      self.web.document.meta.addMetadata(attrs)
    if tag == "head":
      self.web.document.head = HTMLHead(attrs)
    if tag == "body":
      self.web.document.body = HTMLBody(attrs)
      self.web.document.isBody = True
    if tag == "script":
      self.web.document.scripts.append(HTMLJavaScript(attrs))

    if tag == "a":
      if self.web.document.currentDiv != None:
        self.web.document.currentDiv.objects.append(HTMLA(attrs))
        return
      if self.web.document.isBody:
        self.web.document.body.objects.append(HTMLA(attrs))
      else:
        self.web.document.head.objects.append(HTMLA(attrs))

    if tag == "p":
      if self.web.document.currentDiv != None:
        self.web.document.currentDiv.objects.append(HTMLP(attrs))
        return
      if self.web.document.isBody:
        self.web.document.body.objects.append(HTMLP(attrs))
      else:
        self.web.document.head.objects.append(HTMLP(attrs))

    if tag == "style":
      if self.web.document.currentDiv != None:
        self.web.document.currentDiv.objects.append(HTMLStyle())
        return
      if self.web.document.isBody:
        self.web.document.body.objects.append(HTMLStyle())
      else:
        self.web.document.head.objects.append(HTMLStyle())

    if tag == "div":
      d = HTMLDiv(attrs)
      if self.web.document.currentDiv != None:
        self.web.document.currentDiv.objects.append(d)
        return
      self.web.document.currentDiv = d
      self.web.document.body.objects.append(d)
      
    if tag == "span":
      d = HTMLSpan(attrs)
      if self.web.document.currentSpan != None:
        self.web.document.currentSpan.objects.append(d)
        return
      self.web.document.currentSpan = d
      self.web.document.body.objects.append(d)

    if tag == "img":
      for a in attrs:
        if a[0] == "src":
          thread2 = threading.Thread(target=self.web.getResource, args=[a[1]])
          thread2.start()

      i = HTMLImg(attrs)
      if self.web.document.currentDiv != None:
        self.web.document.currentDiv.objects.append(i)
        return
      if self.web.document.isBody:
        self.web.document.body.objects.append(i)
      else:
        self.web.document.head.objects.append(i)

##    print(tag)
    self.preTag = tag
    #Attrs is all variables in the tag
    #tag is the tag name

  def handle_endtag(self, tag):
    if tag == "div":
      for o in self.web.document.body.objects:
        if isinstance(o, HTMLDiv) and self.web.document.currentDiv in o.objects:
          self.web.document.currentDiv = o
    if tag == "span":
      for o in self.web.document.body.objects:
        if isinstance(o, HTMLSpan) and self.web.document.currentSpan in o.objects:
          self.web.document.currentSpan = o
    pass
    #tag is the tag name

  def handle_data(self, data):
    data = str(data)
    if r"\n" in data or r"\t" in data:
      return
    if self.preTag == "script":
      self.web.document.scripts[-1].data = data
      return
    if self.preTag == "title":
      self.web.document.title = data
      self.web.tabTitle = data
      return

    if self.web.document.isBody and self.web.document.body.objects != []:
      self.web.document.body.objects[-1].data = data
    elif self.web.document.head != None and self.web.document.head.objects != []:
      self.web.document.head.objects[-1].data = data
    
    #data is text between a start and end tag

  def handle_comment(self, data):
    pass
    #Just HTML Comments, can probably leave this as-is

  def handle_entityref(self, name):
    pass
    #Converts name entities???

  def handle_charref(self, name):
    pass
    #Converts num entities???

  def handle_decl(self, data):
    pass
    #handles declarations, again probably leave as-is

  def setWebObject(self, web):
    self.web = web

class HTMLMeta:
  def __init__(self, web):
    self.data = {}
    self.web = web
    
  def addMetadata(self, attrs):
    if attrs[0][0] == "name":
      self.data[attrs[0][1]] = attrs[1][1]
    if attrs[0][0] == "http-equiv":
      self.data[attrs[0][1]] = attrs[1][1]
    if attrs[0][0] == "scheme":
      self.data[attrs[0][0]] = attrs[0][1]
    if attrs[0][0] == "charset":
      self.data[attrs[0][0]] = attrs[0][1]
    
    if attrs[1][0] == "name":
      self.data[attrs[1][1]] = attrs[0][1]
    if attrs[1][0] == "http-equiv":
      self.data[attrs[1][1]] = attrs[0][1]
    if attrs[1][0] == "scheme":
      self.data[attrs[1][0]] = attrs[1][1]
    if attrs[1][0] == "charset":
      self.data[attrs[1][0]] = attrs[1][1]
    if attrs[1][0] == "property":
      self.data[attrs[1][1]] = attrs[0][1]

    if attrs[0][1].endswith(".png") or attrs[0][1].endswith(".jpg"):
      if attrs[0][1].startswith("http://"):
        thread2 = threading.Thread(target=self.web.getResource, args=[attrs[0][1]])
        thread2.start()
      else:
        thread2 = threading.Thread(target=self.web.getResource, args=[self.web.url+attrs[0][1]])
        thread2.start()
      

class HTMLHead:
  def __init__(self, attrs=[]):
    self.objects = []
    self.attrs = attrs

class HTMLBody:
  def __init__(self, attrs=[]):
    self.objects = []
    self.attrs = attrs

class HTMLDocument:
  def __init__(self, web):
    self.meta = HTMLMeta(web)
    self.currentDiv = None
    self.currentSpan = None
    self.scripts = []
    self.isBody = False
    self.title = ""
    self.body = None
    self.head = None

class HTMLJavaScript:
  def __init__(self, attrs):
    self.data = ""
    self.attrs = self.getAttrs(attrs)

  def getAttrs(self, attrs):
    a2 = {}
    for a in attrs:
      a2[a[0]] = a[1]
    return a2

class HTMLA:
  def __init__(self, attrs):
    self.data = ""
    self.attrs = self.getAttrs(attrs)

  def render(self, screen):
    t = self.font.render(self.data, True, (0,0,0))
    screen.blit(t, [20, 100])
    print(self.attrs)

  def getAttrs(self, attrs):
    a2 = {}
    for a in attrs:
      a2[a[0]] = a[1]
    return a2

class HTMLP:
  def __init__(self, attrs):
    self.data = ""
    self.attrs = self.getAttrs(attrs)

  def render(self):
    print(self.attrs)

  def getAttrs(self, attrs):
    a2 = {}
    for a in attrs:
      a2[a[0]] = a[1]
    return a2

class HTMLStyle:
  def __init__(self):
    self.data = ""

  def render(self):
    self.parseData()

  def parseData(self):
    pass

class HTMLDiv:
  def __init__(self, attrs):
    self.data = ""
    self.objects = []
    self.attrs = self.getAttrs(attrs)

  def render(self):
    print(self.attrs)

  def getAttrs(self, attrs):
    a2 = {}
    for a in attrs:
      a2[a[0]] = a[1]
    return a2

class HTMLSpan:
  def __init__(self, attrs):
    self.data = ""
    self.objects = []
    self.attrs = self.getAttrs(attrs)

  def render(self):
    print(self.attrs)

  def getAttrs(self, attrs):
    a2 = {}
    for a in attrs:
      a2[a[0]] = a[1]
    return a2

class HTMLImg:
  def __init__(self, attrs):
    self.data = ""
    self.attrs = self.getAttrs(attrs)

  def render(self):
    print(self.attrs)

  def getAttrs(self, attrs):
    a2 = {}
    for a in attrs:
      a2[a[0]] = a[1]
    return a2
