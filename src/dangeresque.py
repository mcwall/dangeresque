import pygame, time, random


class Burst:
    def __init__(self, color, duration):
        self.color = color
        self.duration = duration
        self.start_time = time.time()

    def scale(self, start, end, percentage):
        diff = (end - start) * percentage
        return start + diff

    def done(self):
        return time.time() > (self.start_time + self.duration)
    
    def current(self):
        now = time.time()
        percentage = (now - self.start_time) / self.duration

        if percentage > 1:
            return (0, 0, 0)

        r = self.scale(self.color[0], 255, percentage)
        g = self.scale(self.color[1], 255, percentage)
        b = self.scale(self.color[2], 255, percentage)

        return (r, g, b)


def random_burst():
    r = random.randrange(0, 255)
    g = random.randrange(0, 255)
    b = random.randrange(0, 255)
    duration = random.randrange(1, 5)
    return Burst((r,g,b), duration)

pygame.init()

white = (255,255,255)
black = (0,0,0)

display = pygame.display.set_mode((800,600))

burst = random_burst()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if burst.done():
        burst = random_burst()

    display.fill(black)
    pygame.draw.rect(display, burst.current(), (200, 200, 100, 100))    
    pygame.display.update()
