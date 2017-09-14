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
  def __init__(self, x, y, dx=0, dy=0,
    color=None, nbhds=None):
    self.x = x
    self.y = y
    self.dx = dx
    self.dy = dy
    self.color = color
    self.nbhds = nbhds if nbhds else []

def flush_space(particles, n):
  for i in range(n):
    for j in range(n):
      print(" - ", end="")
    print()

def move_cursor(x, d):
  if x: print('\033[{}{}'.format(x, d), end='')

def printc(x, y, char, color, offset=0):
  move_cursor((3*x) + 1 + offset, 'C')
  move_cursor(y + 1, 'A')
  print(Colors[color] + char, end='')
  # reset cursor
  move_cursor(y, 'B')
  print(Colors['white'])

def publish_particles(particles):
  for p in particles.values():
    printc(p.x, p.y, 'O', p.color)

def publish_nbhd(x, y):
  # unicode box
  # offest so not directly on top of particles
  printc(x, y, '\u25A1', 'red', offset=-1)

def make_nbhds(particles, n):
  nbhds = {}
  for coords,p in particles.items():
    i,j = [int(x) for x in coords.split(' ')]
    x = str(max(min(i + p.dx, n - 1), 0))
    y = str(max(min(j + p.dy, n - 1), 0))
    key = ' '.join([x, y])

    if not nbhds.get(key):
      nbhds[key] = []
    nbhds[key].append(coords)
    publish_nbhd(int(x), int(y))

def time_step(particles, n):
  # generates and publishes nbhds
  nbhds = make_nbhds(particles, n)

  #  detect_collisions(particles, nbhds, n)

  # clear nbhds from board
  #  flush_nbhds(nbhds, n)

  #  return fulfill_nbhds(space)
  return True

def animate(particles, n):
  flush_space(particles, n)
  publish_particles(particles)
  while(True):
    sleep(0.5)
    time_step(particles, n)

conf = json.load(open(sys.argv[1]))
particles = {}
for key, val in conf.items():
  particles[key] = Cell(**val)

animate(particles, 20)
