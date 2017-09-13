import sys, json
from time import sleep

Colors = {
  'green': '\033[92m',
  'yellow': '\033[93m',
  'blue': '\033[94m',
  'white': '\033[97m'
}

class Cell:
  def __init__(self, on=0, dx=0, dy=0,
    color=None, color_code=None):
    self.on = on
    self.dx = dx
    self.dy = dy
    self.color = color
    self.color_code = color_code or Colors.get(color) or Colors['white']

def time_step(space):
  out = [[Cell() for _ in range(20)] for _ in range(20)]

  for i,l in enumerate(space):
    for j,c in enumerate(l):
      if c.on:
        dest_x = min(i + c.dx, len(out) - 1)
        dest_y = min(j + c.dy, len(out) - 1)
        out[dest_x][dest_y] = Cell(**c.__dict__)
  return out

def print_space(space):
  for l in space:
    for c in l:
      c_out = " O " if c.on else " - "
      print(c.color_code + c_out, end="")
    print(Colors['white'])

def animate(space):
  while(True):
    print_space(space)
    space = time_step(space)
    sleep(1)
    print("\033[21A\r")

conf = json.load(open(sys.argv[1]))
space = [[Cell() for _ in range(20)] for _ in range(20)]
for key, val in conf.items():
  i, j = [int(x) for x in key.split(", ")]
  space[i][j] = Cell(**val)

animate(space)
