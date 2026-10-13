import math

import pygame


# 1. Наш проверенный класс Vector3D
class Vector3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def length(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

# 2. Инициализация графики
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Wireframe Cube Engine")
clock = pygame.time.Clock()

CX = WIDTH / 2
CY = HEIGHT / 2

# 3. Вершины 3D-куба (8 углов в пространстве относительно центра)
cube_vertices = [
    Vector3D(-120, -120, -120),
    Vector3D( 120, -120, -120),
    Vector3D( 120,  120, -120),
    Vector3D(-120,  120, -120),
    Vector3D(-120, -120,  120),
    Vector3D( 120, -120,  120),
    Vector3D( 120,  120,  120),
    Vector3D(-120,  120,  120)
]

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Углы вращения куба по осям
angle_x = 0
angle_y = 0
angle_z = 0

# Функции вращения векторов в 3D (тригонометрические матрицы)
def rotate_x(v, angle):
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    y = v.y * cos_a - v.z * sin_a
    z = v.y * sin_a + v.z * cos_a
    return Vector3D(v.x, y, z)

def rotate_y(v, angle):
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    x = v.x * cos_a + v.z * sin_a
    z = -v.x * sin_a + v.z * cos_a
    return Vector3D(x, v.y, z)

def rotate_z(v, angle):
    rad = math.radians(angle)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    x = v.x * cos_a - v.y * sin_a
    y = v.x * sin_a + v.y * cos_a
    return Vector3D(x, y, v.z)

# 4. Главный игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление вращением стрелками или автоматическое вращение
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: angle_y -= 2
    if keys[pygame.K_RIGHT]: angle_y += 2
    if keys[pygame.K_UP]: angle_x -= 2
    if keys[pygame.K_DOWN]: angle_x += 2
    
    # Автоматическое плавное вращение, если не нажаты клавиши
    if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
        angle_x += 1.2
        angle_y += 1.5

    # Глубокий космический фон с эффектом следа
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.set_alpha(100)
    fade_surface.fill((10, 10, 25))
    screen.blit(fade_surface, (0, 0))

    # Массив для хранения спроецированных 2D-координат вершин
    projected_points = []

    for vertex in cube_vertices:
        # Применяем вращение по всем трем осям
        rotated = rotate_x(vertex, angle_x)
        rotated = rotate_y(rotated, angle_y)
        rotated = rotate_z(rotated, angle_z)

        # Отодвигаем объект вглубь по оси Z, чтобы камера не «резала» его
        distance = 450
        z_depth = rotated.z + distance

        # Перспективная проекция (3D -> 2D)
        k = 400 / z_depth
        screen_x = int(rotated.x * k + CX)
        screen_y = int(rotated.y * k + CY)

        projected_points.append((screen_x, screen_y))

    # Отрисовка рёбер куба (линий)
    for edge in cube_edges:
        p1 = projected_points[edge[0]]
        p2 = projected_points[edge[1]]
        pygame.draw.line(screen, (0, 255, 200), p1, p2, 2)

    # Отрисовка вершин (ярких неоновых точек на углах)
    for pt in projected_points:
        pygame.draw.circle(screen, (255, 255, 255), pt, 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()