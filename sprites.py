import pygame
import random

from settings import (
    WIDTH,
    HEIGHT,
    PLAYER_SPEED,
    PLAYER_BULLET_SPEED,
    ALIEN_BULLET_SPEED,
    LIFE_ITEM_SPEED,
)


class Player(pygame.sprite.Sprite):
    """Spaceship controlled by the player."""

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.lives = 3
        # Last movement direction used for shooting
        self.direction = pygame.math.Vector2(0, -1)

    def update(self, pressed, screen_rect):
        """Move according to pressed keys in four directions."""
        move = pygame.math.Vector2(0, 0)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            move.x -= PLAYER_SPEED
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            move.x += PLAYER_SPEED
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            move.y -= PLAYER_SPEED
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            move.y += PLAYER_SPEED
        self.rect.x += move.x
        self.rect.y += move.y
        if move.length_squared() > 0:
            self.direction = move.normalize()
        self.rect.clamp_ip(screen_rect)


class Bullet(pygame.sprite.Sprite):
    """Projectile fired by the player in any direction."""

    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(direction).normalize() * PLAYER_BULLET_SPEED

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (
            self.rect.bottom < 0
            or self.rect.top > HEIGHT
            or self.rect.right < 0
            or self.rect.left > WIDTH
        ):
            self.kill()


class AlienBullet(pygame.sprite.Sprite):
    """Projectile fired by aliens in variable directions."""

    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(direction).normalize() * ALIEN_BULLET_SPEED

    def update(self):
        # Add slight random drift so paths aren't perfectly straight
        self.velocity.rotate_ip(random.uniform(-2, 2))
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (
            self.rect.bottom < 0
            or self.rect.top > HEIGHT
            or self.rect.right < 0
            or self.rect.left > WIDTH
        ):
            self.kill()


class Alien(pygame.sprite.Sprite):
    """Enemy alien moving freely across the screen."""

    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        # random initial velocity vector
        vec = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if vec.length_squared() == 0:
            vec.y = 1
        self.velocity = vec.normalize() * speed

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        # bounce at screen edges
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velocity.x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.velocity.y *= -1

    def maybe_shoot(self, bullets, target_pos):
        if random.random() < 0.005:
            direction = pygame.math.Vector2(target_pos) - pygame.math.Vector2(self.rect.center)
            if direction.length_squared() == 0:
                direction.y = 1
            bullet = AlienBullet(self.rect.centerx, self.rect.centery, direction)
            bullets.add(bullet)


class LifeItem(pygame.sprite.Sprite):
    """Floating item granting an extra life when collected."""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += LIFE_ITEM_SPEED
        if self.rect.top > HEIGHT:
            self.kill()


def create_wave(level, speed):
    """Create a wave of freely moving aliens."""
    aliens = pygame.sprite.Group()
    count = 5 + level * 2
    for _ in range(count):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(0, HEIGHT // 2)
        alien = Alien(x, y, speed)
        aliens.add(alien)
    return aliens
