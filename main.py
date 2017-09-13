import sys, json
from time import sleep

Colors = {
  'green': '\033[92m',
  'yellow': '\033[93m',
  'blue': '\033[94m',
  'white': '\033[97m'
}

class Cell:
  def __init__(self, on=0, d=0, color=None, color_code=None):
    self.on = on
    self.d = d
    self.color = color
    self.color_code = color_code or Colors.get(color) or Colors['white']

def time_step(space):
  out = [None] * len(space)
  for i in range(len(out)):
    out[i] = Cell()
  for i,c in enumerate(space):
    if c.on:
      dest = i + c.d
      dest = dest - 20 if dest > len(space) else dest
      out[dest] = Cell(**c.__dict__)
  return out

def print_space(space):
  for i,c in enumerate(space):
    if i and not i%20: print()
    c_out = " O " if c.on else " - "
    print(c.color_code + c_out, end="")
  print()

def animate(space):
  while(True):
    print_space(space)
    space = time_step(space)
    sleep(1)
    print("\033[21A\r")

conf = json.load(open(sys.argv[1]))
space = [None] * 400
for i in range(len(space)):
  c = dict(conf.get(str(i)) or {})
  space[i] = Cell(**c)

animate(space)
