import sys, json

class Cell:
  def __init__(self, on=0, d=0):
    self.on = on
    self.d = d

def print_space(space):
  for i,c in enumerate(space):
    if i and not i%20: print()
    c_out = " O " if c.on else " - "
    print(c_out, end="")
  print()

conf = json.load(open(sys.argv[1]))
space = [None] * 400
for i in range(len(space)):
  c = dict(conf.get(str(i)) or {})
  space[i] = Cell(**c)

print_space(space)
