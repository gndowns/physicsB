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
  def __init__(self, dx=0, dy=0,
    color=None, nbhds=None):
    self.dx = dx
    self.dy = dy
    self.color = color
    self.nbhds = nbhds if nbhds else []

  def copy(self):
    return Cell(**self.__dict__)

def flush_space(particles, n):
  for _ in range(n):
    for _ in range(n):
      print(' - ', end='')
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
  for key, p in particles.items():
    x,y = [int(z) for z in key.split()]
    printc(x, y, 'O', p.color)

def publish_nbhd(x, y):
  # unicode box
  # offest so not directly on top of particles
  printc(x, y, '\u25A1', 'red', offset=-1)

def make_nbhds(particles, n):
  # nbhds maps its own location to a list of
  # coordinates of each owner of the nbhd
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
  return nbhds

def flush_obj(objs, res, offset=0):
  for key in objs.keys():
    x,y = [int(z) for z in key.split()]
    printc(x, y, res, 'white', offset=offset)

def fulfill_nbhds(particles, nbhds):
  out = {}
  for dest,l in nbhds.items():
    for p_coords in l:
      p = particles[p_coords]
      out[dest] = p
  return out

def detect_collisions(particles, nbhds):
  for nbhd in nbhds.values():
    if len(nbhd) > 1:
      handle_collision(particles, nbhd)

def handle_collision(particles, nbhd):
  original_particles = {}
  for coords in nbhd:
    original_particles[coords] = particles[coords].copy()

  for p_coords in nbhd:
    p = particles[p_coords]
    for q_coords in nbhd:
      if q_coords != p_coords:
        q = original_particles[q_coords]
        p.dx = q.dx
        p.dy = q.dy

def time_step(particles, n):
  sleep(0.5)

  nbhds = make_nbhds(particles, n)

  sleep(0.5)

  detect_collisions(particles, nbhds)
  flush_obj(nbhds, ' ', offset=-1)
  nbhds = make_nbhds(particles, n)

  sleep(0.25)

  flush_obj(nbhds, ' ', offset=-1)
  flush_obj(particles, '-')
  # advance particles
  return fulfill_nbhds(particles, nbhds)

def animate(particles, n):
  flush_space(particles, n)
  while(True):
    publish_particles(particles)
    particles = time_step(particles, n)

conf = json.load(open(sys.argv[1]))
particles = {}
for key, val in conf.items():
  particles[key] = Cell(**val)

animate(particles, 20)
