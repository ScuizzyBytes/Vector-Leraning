import random

import pygame


class Vector2D:

    def __init__(self, x=0.0, y=0.0):
      self.x = float(x)
      self.y = float(y)

    def __repr__(self):
      return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
      return Vector2D(self.x + other.x, self.y + other.y)

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("???")
clock  = pygame.time.Clock()

running = True

stars = []
for _ in range(50):
    pos = Vector2D(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    vel = Vector2D(0, random.uniform(0.5, 2.03))

    random_rgb = (
        random.randint(50, 255),
        random.randint(50, 255),
        random.randint(50, 255),
  )
    stars.append({"pos": pos, "vel": vel, "color": random_rgb})

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 10, 25))

    for star in stars:
        star["pos"] = star["pos"] + star["vel"]

        if star["pos"].y > HEIGHT:
          star["pos"].y = 0
          star["pos"].x = random.randint(0, WIDTH)

        pygame.draw.circle(screen, star["color"], (int(star["pos"].x), int(star["pos"].y)), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.QUIT()

    