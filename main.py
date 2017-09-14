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
    color=None, color_code=None, nbhds=None):
    self.x = x
    self.y = y
    self.dx = dx
    self.dy = dy
    self.color = color
    self.color_code = color_code or Colors.get(color) or Colors['white']
    self.nbhds = nbhds if nbhds else []

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

def flush_space(particles, n):
  for i in range(n):
    for j in range(n):
      print(" - ", end="")
    print()

def time_step(particles, n):
  nbhds = make_nbhds(particles, n)
  #  detect_collisions(space)

  #  return fulfill_nbhds(space)
  return True

def move_cursor(x, d):
  print('\033[{}{}'.format(x, d), end='')

def publish_particles(particles):
  for p in particles.values():
    # set cursor
    move_cursor(p.x + 1, "A")
    move_cursor(p.y + 1, "C")
    print(p.color_code + 'O', end='')
    # reset cursor
    move_cursor(p.x, "B")
    move_cursor(p.y, "D")
    print(Colors['white'])

def animate(particles, n):
  flush_space(particles, n)
  publish_particles(particles)

conf = json.load(open(sys.argv[1]))
particles = {}
for key, val in conf.items():
  particles[key] = Cell(**val)

animate(particles, 20)
