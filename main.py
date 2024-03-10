import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Определение констант
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CHARACTER_WIDTH = 50
CHARACTER_HEIGHT = 50
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра с прыжками")

# Загрузка изображений
character_img = pygame.image.load("character.png")
character_img = pygame.transform.scale(character_img, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
obstacle_img = pygame.image.load("obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# Класс для персонажа
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = character_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - CHARACTER_HEIGHT // 2)
        self.velocity = 0
        self.jump = False

    def update(self):
        if self.jump:
            self.rect.y -= self.velocity * 2
            self.velocity -= 1
            if self.velocity < 0:
                self.jump = False
        else:
            if self.rect.y < SCREEN_HEIGHT - CHARACTER_HEIGHT // 2:
                self.rect.y += self.velocity * 2
                self.velocity += 1
            else:
                self.rect.y = SCREEN_HEIGHT - CHARACTER_HEIGHT // 2

    def jump_start(self):
        if not self.jump:
            self.velocity = 10
            self.jump = True

# Класс для препятствия
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = obstacle_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH + OBSTACLE_WIDTH // 2, SCREEN_HEIGHT - OBSTACLE_HEIGHT // 2)
        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH + OBSTACLE_WIDTH // 2
            self.speed = random.randint(3, 5)

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
character = Character()
all_sprites.add(character)

# Таймер для генерации препятствий
obstacle_timer = pygame.time.get_ticks()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                character.jump_start()

    current_time = pygame.time.get_ticks()
    if current_time - obstacle_timer > 2000:  # Генерация препятствий каждые 2 секунды
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)
        obstacle_timer = current_time

    screen.fill(WHITE)

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
