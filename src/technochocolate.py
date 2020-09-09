import board, neopixel
import random, colorsys, randomcolor, time, signal, sys
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
        self.duration = random.randrange(1500, 5000)
        self.interval = random.randrange(200, 500)
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


white = (255,255,255)
black = (0,0,0)

n = 3
pixels = neopixel.NeoPixel(board.D18, n)
s = SequenceFactory(n).rand()

def signal_handler(sig, frame):
    print('Shutting down...')
    pixels.deinit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    if s.done():
        time.sleep(0.5 + random.random() * 2.0)
        s = SequenceFactory(n).rand()

    state = s.state()
    for i in range(n):
        pixels[i] = state[i]

    time.sleep(0.001)