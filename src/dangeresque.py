import pygame, random, colorsys, randomcolor
from datetime import datetime

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def random_color():
    return hex_to_rgb(randomcolor.RandomColor().generate(luminosity='bright')[0])


def timestamp():
    return int(round(datetime.now().timestamp() * 1000))

class Burst:
    def __init__(self, color, duration, delay=0):
        self.color = color
        self.duration = duration
        self.start_time = timestamp() + delay

    def done(self):
        return timestamp() > (self.start_time + self.duration)
    
    def state(self):
        now = timestamp()
        percentage = 1 - (now - self.start_time) / self.duration

        if percentage < 0 or percentage > 1:
            return (0, 0, 0)

        r, g, b = [x/255.0 for x in self.color]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = l * percentage
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        r, g, b = [x*255.0 for x in (r, g, b)]
        
        return (r, g, b)


class Sequence:
    def __init__(self, bursts):
        self.bursts = bursts

    def done(self):
        return all(b.done() for b in self.bursts)

    def state(self):
        return [b.state() for b in self.bursts]


class SequenceFactory:
    def __init__(self, n):
        self.n = n
        self.duration = random.randrange(1000, 4000)
        self.interval = random.randrange(100, 400)
        self.unicolor = random_color() if bool(random.getrandbits(1)) else None

    def simul(self):
        bursts = []
        for i in range(self.n):
            bursts.append(Burst(self.unicolor or random_color(), self.duration))

        return Sequence(bursts)

    def lr(self):
        bursts = []
        for i in range(self.n):
            bursts.append(Burst(self.unicolor or random_color(), self.duration, self.interval * i))

        return Sequence(bursts)

    def rl(self):
        bursts = []
        for i in range(self.n):
            bursts.append(Burst(self.unicolor or random_color(), self.duration, self.interval * (self.n - 1 - i)))

        return Sequence(bursts)

    def rand(self):
        r = random.randrange(3)
        if r == 0:
            return self.simul()
        elif r == 1:
            return self.lr()
        else:
            return self.rl()


pygame.init()

white = (255,255,255)
black = (0,0,0)

display = pygame.display.set_mode((800,600))

s = SequenceFactory(3).rand()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if s.done():
        s = SequenceFactory(3).rand()

    display.fill(black)
    state = s.state()
    pygame.draw.rect(display, state[0], (200, 200, 100, 100))
    pygame.draw.rect(display, state[1], (400, 200, 100, 100))
    pygame.draw.rect(display, state[2], (600, 200, 100, 100))
    pygame.display.update()
