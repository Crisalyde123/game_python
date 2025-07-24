import pygame
import random

from settings import WIDTH, HEIGHT, PLAYER_SPEED, BULLET_SPEED, ALIEN_BULLET_SPEED


class Player(pygame.sprite.Sprite):
    """Spaceship controlled by the player."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.lives = 3

    def update(self, pressed, screen_rect):
        """Move according to pressed keys and stay on screen."""
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        self.rect.clamp_ip(screen_rect)


class Bullet(pygame.sprite.Sprite):
    """Projectile fired by the player."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()


class AlienBullet(pygame.sprite.Sprite):
    """Projectile fired by aliens."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += ALIEN_BULLET_SPEED
        if self.rect.top > HEIGHT:
            self.kill()


class Alien(pygame.sprite.Sprite):
    """Enemy alien descending towards the player."""

    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

    def maybe_shoot(self, bullets):
        if random.random() < 0.005:
            bullet = AlienBullet(self.rect.centerx, self.rect.bottom)
            bullets.add(bullet)


def create_wave(level, speed):
    """Create a wave of descending aliens."""
    aliens = pygame.sprite.Group()
    count = 5 + level * 2
    spacing = WIDTH // count
    for i in range(count):
        x = i * spacing + spacing // 2 - 20
        alien = Alien(x, -40, speed)
        aliens.add(alien)
    return aliens
