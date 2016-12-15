import sys
import os
import platform
import urllib.request
import urllib.error
import UserCred
from UserCred import UserLog
import importlib

#Define Functions
def addUser():
    while 1:
        name = input("New Username: ")
        if name == "": return
        passn = input("New Password: ")
        if passn == "": print("Account must have a password!")
        elif passn != "" and name not in up:
            up[name] = passn
            print("New User Added!")
            return
        else: print("Username already in use, please choose another.")

def runProgram2(comm):
    ls = comm.split()
    if len(ls) == 2:
        filename = ls[1]
        try:
            with open(filename) as f:
                towrite = f.read()
                f.close()
            with open("temp.py", "w") as file:
                file.write(towrite)
                file.close()
            try:
                importlib.reload(temp)
            except NameError:
                import temp
            if filename not in programs:
                programs.append(filename)
        except IOError: print("Program doesn't exist.")
        clearTempCache()
    else:
        print("No program input!")

def clearTempCache():
    with open("temp.py", "w") as f2:
        f2.write("")
        f2.close()

def removeUser():
    utr = input("Username of account to remove: ")
    ptr = input("Confirmation password: ")
    if up[utr] == ptr:
        del up[utr]
    print("User Deleted\n" + "You must login again.")
    print("==========================Login Screen========================")

def readFile(comm):
    list1 = comm.split(" ")
    if len(list1) == 2:
        filename = list1[1]
        try:
            for lines in open(filename):
                print(lines.strip())
        except IOError: print("File does not exist!")
        except UnicodeDecodeError: print("File Type Incompatible.")
    else: print("File name must not contain spaces!")
def showHelp():
    print("=================Help==================")
    print("adduser - Add a new user.\n" + "rmuser - Remove a user, requires user's permission\n" + "lsusers - List the usernames of all users")
    print("nettest - Test your internet connection\n" + "logout - Logout to login screen\n" + "exit or shutdown - Shutdown the computer, saving users\n" + "run - Run another python script\n" + "read - Display the contents of a text file\n" + "startgui - Start the graphical user interface")
    print("settings - Adjust settings for PyCom OS")
    print("=======================================")
def testNetwork():
    site = "http://www.duckduckgo.com"
    try:
        response=urllib.request.urlopen(site,data=None, timeout=1)
        print("Internet connection established and working!")
    except urllib.error.URLError:
        print("Unable to establish internet connection.\n" + "Is there a proxy on this network?")
def saveAndShutdown():
    print("Shutting Down...")
    towrite = []
    for m in up:
        towrite.append(m+","+up[m]+","+UserLog().getUserIDFromName(m))
    with open ("user.pt","w") as file:
        file.write('\n'.join(towrite))
        file.close()
    with open('proglist.txt',"w") as file:
        file.write('\n'.join(programs))
        file.close()
    sys.exit()
def consoleCommands(comm):
    if comm == "adduser":
        addUser()
        return False
    elif comm.startswith("run") and comm.endswith(".py"):
        runProgram2(comm)
        return False
    elif comm == "rmuser":
        removeUser()
        return True
    elif comm == "lsusers":
        for i in up: print(i)
        return False
    elif comm.startswith("read"):
        readFile(comm)
        return False
    elif comm == "startgui":
        try:
            import EventSystem
            EventSystem(4, UserLog().getUserFromUP(username, password))
        except ImportError: print("Pygame not installed, unable to launch Graphical Interface.")
        return False
    elif comm == "help":
        showHelp()
        return False
    elif comm == "nettest":
        testNetwork()
        return False
    elif comm == "exit" or comm == "shutdown": saveAndShutdown()
    elif comm == "logout":
        print("Logging Out...\n" + "==================================")
        return True
    else:
        print("Error! Invalid command.")
        return False

def settings(sett):
    print("=====================================")
    print("      Settings Application")
    print("=====================================")
    choice = ""
    while choice != "quit":
        print("Choose a setting to change:")
        print("1: Hostname")
        print("2: GUI on startup (Require restart)")
        print("3: Home folder")
        print("quit: Save settings and return to console")
        choice = input("> ")
        if choice == "1":
            hostname = input("New Hostname: ")
            sett[0] = hostname
        elif choice == "2":
            if sett[1] == True:
                sett[1] = False
                print("PyCom OS will boot to shell on next startup")
            else:
                sett[1] = True
                print("PyCom OS will boot graphically on next startup")
        elif choice == "3":
            sett[2] = input("Path to Folder (from HDD root directory): ")
        elif choice != "quit": print("Invalid setting!")
    with open("config.txt", "w") as file:
        sett2 = []
        for i in sett:
            sett2.append(str(i))
        file.write('\n'.join(sett2))
        file.close()
    return sett

#Operating System Beginning
print("PyCom OS v0.35, 2016\n" + "Created by Mitchell Bagot, Written in Python")
print("===============Login Screen==============")
login = False
shut = False
gui = False
up = {}
sett = []
programs = []
usernames = [u.split(",")[0] for u in open("user.pt")]
passwords = [u.split(",")[1] for u in open("user.pt")]
for u in range(0, len(usernames)):
    up[usernames[u]] = passwords[u]
i = 0
for line in open("config.txt"):
    if i == 0: sett.append(line.strip())
    if i == 1:
        if line.startswith("True"): sett.append(True)
        else: sett.append(False)
    if i == 2: sett.append(line.strip())
    i += 1
for line in open("proglist.txt"):
    if line != "": programs.append(line.strip())
if sett[1] == True:
    try:
        import EventSystem
        ev = EventSystem.EventSystem()
    except ImportError:
        print("Pygame not installed, unable to launch Graphical Interface, returning to Command Line.")
        sett[1] = False
if sett[1] == False:
    while login == False:
        username = input("Username: ")
        password = input("Password: ")
        
        if up[username] == password:
            print("Login Success!\n" + "Setting up Desktop Environment...\n" + "Desktop Environment Set!")
            print("=================================================")
            shut = False
            while shut == False:
                command = input(username+"@"+sett[0]+" ~/: ")
                if command == "settings": sett = settings(sett)
                else: shut = consoleCommands(command)
            login = False
        else:
            print("Login Failed!")
consoleCommands("exit")
