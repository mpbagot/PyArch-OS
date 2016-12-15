class UserCred:
  def __init__(self, uid):
    ##Get username and password + home directory from user list##
    self.id = uid
    self.username = self.getUsername()
    self.password = ""
  ##This is a user file. Fill it out!!

  def __str__(self):
    return self.username

  def getUsername(self):
    for a in open("user.pt"):
      ab = a.strip().split(",")
      if ab[2] == self.id:
        return ab[0]

class UserLog():
  def getUserFromUP(self, u, p):
    for a in open("user.pt"):
      ab = a.split(",")
      if ab[0] == u and ab[1] == p:
        return UserCred(ab[2])
  def getUserIDFromName(self, u):
    for a in open("user.pt"):
      ab = a.strip().split(",")
      if ab[0] == u:
        return str(ab[2])
