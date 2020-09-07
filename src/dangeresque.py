import pygame, time, random, colorsys


class Burst:
    def __init__(self, color, duration):
        self.color = color
        self.duration = duration
        self.start_time = time.time()

    def done(self):
        return time.time() > (self.start_time + self.duration)
    
    def current(self):
        now = time.time()
        percentage = 1 - (now - self.start_time) / self.duration

        if percentage < 0:
            return (0, 0, 0)

        r, g, b = [x/255.0 for x in self.color]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = l * percentage
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        r, g, b = [x*255.0 for x in (r, g, b)]
        
        return (r, g, b)


def random_burst():
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    duration = random.randrange(3, 5)
    return Burst((r,g,b), duration)


class Sequence:
    def __init__(self):
        b = random_burst()
        self.bursts = [b, b, b]

    def done(self):
        return self.bursts[0].done()


pygame.init()

white = (255,255,255)
black = (0,0,0)

display = pygame.display.set_mode((800,600))

s = Sequence()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if s.done():
        s = Sequence()

    display.fill(black)
    pygame.draw.rect(display, s.bursts[0].current(), (200, 200, 100, 100))
    pygame.draw.rect(display, s.bursts[1].current(), (400, 200, 100, 100))
    pygame.draw.rect(display, s.bursts[2].current(), (600, 200, 100, 100))
    pygame.display.update()
