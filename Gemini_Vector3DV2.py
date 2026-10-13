import random

import pygame


# 1. Наш новый мощный класс для 3D пространства
class Vector3D:

  def __init__(self, x=0.0, y=0.0, z=0.0):
    self.x = float(x)
    self.y = float(y)
    self.z = float(z)

  def __repr__(self):
    return f"Vector3D({self.x}, {self.y}, {self.z})"

  # Сложение трехмерных векторов
  def __add__(self, other):
    return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

  def __sub__(self, other):
    return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

  def length(self):
    return (self.x**2 + self.y**2 + self.z**2) ** 0.5


# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Vector Warp Speed")
clock = pygame.time.Clock()

# Центр экрана для проекции
CX = WIDTH / 2
CY = HEIGHT / 2

# 2. Создаем популяцию звезд в 3D (X и Y вокруг центра, Z — глубина)
stars = []
for _ in range(400):
  stars.append({
      "pos": Vector3D(
          random.randint(-400, 400),
          random.randint(-300, 300),
          random.randint(100, 800),
      ),
      "vel": Vector3D(0, 0, -4.0),  # Двигаем по оси Z к наблюдателю
  })

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Темный глубокий космос
  screen.fill((5, 5, 12))

  for star in stars:
    # 3. Движение в 3D пространстве в одно действие!
    star["pos"] = star["pos"] + star["vel"]

    # Если звезда пролетела сквозь камеру (z <= 0), возвращаем её в далёкий космос
    if star["pos"].z <= 0:
      star["pos"].z = 800
      star["pos"].x = random.randint(-400, 400)
      star["pos"].y = random.randint(-300, 300)

    # 4. МАГИЯ ПРОЕКЦИИ 3D -> 2D
    # Коэффициент перспективы: чем меньше Z (ближе звезда), тем больше k
    k = 300 / star["pos"].z
    screen_x = int(star["pos"].x * k + CX)
    screen_y = int(star["pos"].y * k + CY)

    # Рисуем только если звезда в пределах экрана
    if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
      # Размер и яркость автоматически зависят от глубины
      radius = max(1, int(k * 1.8))
      brightness = min(
          255, int(255 * (1 - star["pos"].z / 800))
      )  # Далекие тусклые, близкие яркие

      pygame.draw.circle(
          screen,
          (brightness, brightness, brightness),
          (screen_x, screen_y),
          radius,
      )

  pygame.display.flip()
  clock.tick(60)

pygame.quit()