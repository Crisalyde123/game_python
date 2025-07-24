import pygame

from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    INITIAL_ALIEN_SPEED,
    ALIEN_DROP_INCREASE,
    POINTS_PER_ALIEN,
    SPEED_UP_SCORE,
)
from sprites import Player, Bullet, create_wave


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
        player.update(pressed, screen.get_rect())

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


if __name__ == "__main__":
    main()
