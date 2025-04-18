import pygame
import sys
import random

pygame.init()  # Must be outside main() for pygbag to initialize properly

WIDTH, HEIGHT = 600, 800
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Plane Shooter")

    font = pygame.font.SysFont(None, 40)
    big_font = pygame.font.SysFont(None, 70)

    # Load sounds with fallback for browser compatibility
    try:
        shoot_sound = pygame.mixer.Sound("shoot.wav")
    except:
        shoot_sound = None
    try:
        explosion_sound = pygame.mixer.Sound("explosion.wav")
    except:
        explosion_sound = None
    try:
        gameover_sound = pygame.mixer.Sound("gameover.wav")
    except:
        gameover_sound = None

    plane_width, plane_height = 50, 50
    plane = pygame.Rect(WIDTH // 2 - plane_width // 2, HEIGHT - 60, plane_width, plane_height)
    plane_speed = 5

    bullets = []
    bullet_speed = 7

    enemies = []
    enemy_speed = 3
    enemy_spawn_time = 30
    enemy_timer = 0

    score = 0
    lives = 3
    paused = False

    clock = pygame.time.Clock()
    FPS = 60

    def draw_text(text, size, color, x, y, center=True):
        f = pygame.font.SysFont(None, size)
        text_surface = f.render(text, True, color)
        rect = text_surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        screen.blit(text_surface, rect)

    def show_start_screen():
        screen.fill(WHITE)
        draw_text("PLANE SHOOTER", 60, BLACK, WIDTH // 2, HEIGHT // 3)
        draw_text("Arrows = Move | SPACE = Shoot", 40, BLACK, WIDTH // 2, HEIGHT // 2)
        draw_text("P = Pause/Unpause | ESC = Quit", 30, BLACK, WIDTH // 2, HEIGHT // 2 + 30)
        draw_text("Press any key to start", 30, RED, WIDTH // 2, HEIGHT - 100)
        pygame.display.flip()
        wait_for_key()

    def wait_for_key():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    return

    def show_game_over():
        screen.fill(WHITE)
        draw_text("GAME OVER", 70, RED, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(f"Your Score: {score}", 40, BLACK, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text("Press any key to play again", 30, GREEN, WIDTH // 2, HEIGHT - 100)
        pygame.display.flip()
        wait_for_key()

    def reset_game():
        nonlocal bullets, enemies, score, lives
        bullets = []
        enemies = []
        score = 0
        lives = 3
        plane.x = WIDTH // 2 - plane_width // 2

    show_start_screen()
    running = True

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and plane.left > 0:
                plane.x -= plane_speed
            if keys[pygame.K_RIGHT] and plane.right < WIDTH:
                plane.x += plane_speed
            if keys[pygame.K_SPACE]:
                if len(bullets) == 0 or bullets[-1].y < plane.y - 60:
                    bullet = pygame.Rect(plane.centerx - 5, plane.y, 10, 20)
                    bullets.append(bullet)
                    if shoot_sound:
                        shoot_sound.play()

            for bullet in bullets:
                bullet.y -= bullet_speed
            bullets = [b for b in bullets if b.y > -20]

            enemy_timer += 1
            if enemy_timer >= enemy_spawn_time:
                enemy_timer = 0
                x_pos = random.randint(0, WIDTH - 40)
                enemy = pygame.Rect(x_pos, -40, 40, 40)
                enemies.append(enemy)

            for enemy in enemies:
                enemy.y += enemy_speed

            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.colliderect(enemy):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        if explosion_sound:
                            explosion_sound.play()
                        score += 1
                        break

            for enemy in enemies[:]:
                if enemy.colliderect(plane) or enemy.y > HEIGHT:
                    enemies.remove(enemy)
                    lives -= 1
                    if lives <= 0:
                        if gameover_sound:
                            gameover_sound.play()
                        show_game_over()
                        reset_game()
                        break

        pygame.draw.rect(screen, BLUE, plane)
        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet)
        for enemy in enemies:
            pygame.draw.rect(screen, BLACK, enemy)

        draw_text(f"Score: {score}", 30, BLACK, 10, 10, center=False)
        draw_text(f"Lives: {lives}", 30, RED, WIDTH - 110, 10, center=False)

        if paused:
            draw_text("Game Paused", 50, GREEN, WIDTH // 2, HEIGHT // 2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
