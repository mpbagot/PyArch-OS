import os

def addCount(dire):
  count = 0
  for file in os.listdir(dire):
    if file.endswith(".py"):
      with open(dire+"/"+file) as f:
        ls = f.read().split("\n")
      count += len(ls)
    elif "." not in file:
      count += addCount(dire+"/"+file)
  return count

print(addCount(os.getcwd()))
