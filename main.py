import pygame
import random

from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    INITIAL_ALIEN_SPEED,
    ALIEN_DROP_INCREASE,
    POINTS_PER_ALIEN,
    SPEED_UP_SCORE,
)
from sprites import Player, Bullet, LifeItem, CoinItem, create_wave


pygame.init()
pygame.display.set_caption("Space Shooter")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


def main():
    player = Player()
    player_group = pygame.sprite.Group(player)
    bullets = pygame.sprite.Group()
    alien_bullets = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    frames_since_life = 0

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
                    bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
                    bullets.add(bullet)
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
                bullets.add(bullet)

        pressed = pygame.key.get_pressed()
        player.update(pressed, screen.get_rect())

        bullets.update()
        aliens.update()
        alien_bullets.update()
        life_items.update()
        coins.update()

        frames_since_life += 1
        if random.random() < min(0.0005 * frames_since_life, 0.05):
            item = LifeItem(random.randint(20, WIDTH - 20), -20)
            life_items.add(item)
            frames_since_life = 0

        for alien in aliens:
            alien.maybe_shoot(alien_bullets, player.rect.center)
            if alien.rect.colliderect(player.rect):
                alien.kill()
                player.lives -= 1
                coins.add(CoinItem(alien.rect.centerx, alien.rect.centery))
        destroyed = pygame.sprite.groupcollide(aliens, bullets, True, True)
        for alien in destroyed:
            score += POINTS_PER_ALIEN
            coins.add(CoinItem(alien.rect.centerx, alien.rect.centery))
        if pygame.sprite.spritecollide(player, alien_bullets, True):
            player.lives -= 1
        if pygame.sprite.spritecollide(player, life_items, True):
            player.lives += 1
        for coin in pygame.sprite.spritecollide(player, coins, True):
            score += 5

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
        life_items.draw(screen)
        coins.draw(screen)

        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_surf = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))
        screen.blit(lives_surf, (WIDTH - 110, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
