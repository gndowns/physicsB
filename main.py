import sys, json
from time import sleep

Colors = {
  'red': '\033[91m',
  'green': '\033[92m',
  'yellow': '\033[93m',
  'blue': '\033[94m',
  'white': '\033[97m'
}

class Cell:
  def __init__(self, on=0, dx=0, dy=0,
    color=None, color_code=None, nbhds=None):
    self.on = on
    self.dx = dx
    self.dy = dy
    self.color = color
    self.color_code = color_code or Colors.get(color) or Colors['white']
    self.nbhds = nbhds if nbhds else []

def time_step(space):
  make_nbhds(space)
  detect_collisions(space)

  return fulfill_nbhds(space)

def fulfill_nbhds(space):
  out = [[Cell() for _ in range(20)] for _ in range(20)]
  for i,l in enumerate(space):
    for j,c in enumerate(l):
      if c.on:
        dest_x = max(min(i + c.dx, len(out) - 1), 0)
        dest_y = max(min(j + c.dy, len(out) - 1), 0)
        c.nbhds = []
        out[dest_x][dest_y] = Cell(**c.__dict__)
  return out


def detect_collisions(space):
  for i,l in enumerate(space):
    for j,c in enumerate(l):
      if len(c.nbhds) >= 2:
        detect_collision(space, c.nbhds)

def detect_collision(space, nbhds):
  particles = [space[nbhds[i][0]][nbhds[i][1]] for i in range(len(nbhds))]
  for p in particles:
    p.dx = 0
    p.dy = 0
    for q in particles:
      p.dx = p.dx + q.dx
      p.dy = p.dy + q.dy


def make_nbhds(space):
  for i,l in enumerate(space):
    for j,c in enumerate(l):
      if c.on:
        dest_x = max(min(i + c.dx, len(space) - 1), 0)
        dest_y = max(min(j + c.dy, len(space) - 1), 0)
        space[dest_x][dest_y].nbhds.append([dest_x, dest_y])

def flush_space(particles, n):
  for i in range(n):
    for j in range(n):
      print(" - ", end="")
    print()

def animate(particles, n):
  while(True):
    flush_space(particles, n)
    sleep(0.5)
    print("\033[21A\r")

conf = json.load(open(sys.argv[1]))
particles = {}
for key, val in conf.items():
  i, j = [int(x) for x in key.split(", ")]
  particles[' '.join([str(i), str(j)])] = Cell(**val)

animate(particles, 20)
