import sys
import json

class Cell:
  def __init__(self, _on=None):
    self.on = 0 if _on==None else _on 

def print_space(space):
  for i,c in enumerate(space):
    if i and not i%20: print()
    c_out = " O " if c.on else " - "
    print(c_out, end="")
  print()

conf = json.load(open(sys.argv[1]))
space = [None] * 400
for i in range(len(space)):
  space[i] = Cell(conf.get(str(i)))

print_space(space)
