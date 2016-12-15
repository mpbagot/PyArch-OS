import SysProgram

class LoginWorkspace:
  def __init__(self, screen):
    self.runningPrograms = {}
    ##Run the login 'program' and pass the return value to the getLogin()##
    self.addProgramToWorkspace(SysProgram.Login((0,0), 1, False, True))

  def getLogin(self, clock):
    return self.runningPrograms[0].getResult(clock, True)

  def addProgramToWorkspace(self, program):
    program.initProc()
    ##Get id for process##
    procid = self.getNewProcID()
    self.runningPrograms[procid] = program

  def getNewProcID(self):
    return len(self.runningPrograms)
