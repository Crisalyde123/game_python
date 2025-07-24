import pygame
import random

# Game constants
WIDTH, HEIGHT = 800, 600
FPS = 60

PLAYER_SPEED = 5
BULLET_SPEED = -8
ALIEN_BULLET_SPEED = 4
INITIAL_ALIEN_SPEED = 1
ALIEN_DROP_INCREASE = 0.5

POINTS_PER_ALIEN = 10
SPEED_UP_SCORE = 100

pygame.init()
pygame.display.set_caption("Space Shooter")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.lives = 3

    def update(self, pressed):
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        self.rect.clamp_ip(screen.get_rect())

class Bullet(pygame.sprite.Sprite):
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
    aliens = pygame.sprite.Group()
    count = 5 + level * 2
    spacing = WIDTH // count
    for i in range(count):
        x = i * spacing + spacing // 2 - 20
        alien = Alien(x, -40, speed)
        aliens.add(alien)
    return aliens


def main():
    player = Player()
    player_group = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    alien_bullets = pygame.sprite.Group()

    score = 0
    level = 0
    alien_speed = INITIAL_ALIEN_SPEED
    aliens = create_wave(level, alien_speed)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)

        pressed = pygame.key.get_pressed()
        player.update(pressed)

        bullets.update()
        aliens.update()
        alien_bullets.update()

        for alien in aliens:
            alien.maybe_shoot(alien_bullets)
            if alien.rect.colliderect(player.rect):
                alien.kill()
                player.lives -= 1
        if pygame.sprite.groupcollide(aliens, bullets, True, True):
            score += POINTS_PER_ALIEN
        if pygame.sprite.spritecollide(player, alien_bullets, True):
            player.lives -= 1

        if score // SPEED_UP_SCORE > level:
            level += 1
            alien_speed += ALIEN_DROP_INCREASE
            aliens = create_wave(level, alien_speed)
        elif len(aliens) == 0:
            level += 1
            alien_speed += ALIEN_DROP_INCREASE
            aliens = create_wave(level, alien_speed)

        if player.lives <= 0:
            running = False

        screen.fill((0, 0, 0))
        player_group.draw(screen)
        bullets.draw(screen)
        aliens.draw(screen)
        alien_bullets.draw(screen)

        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_surf = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))
        screen.blit(lives_surf, (WIDTH - 110, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
