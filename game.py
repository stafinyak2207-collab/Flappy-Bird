import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 1200, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player_rect = pygame.Rect(150, HEIGHT // 2 - 100, 100, 100)

GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


def generate_pipes(count,
                   pipe_width=140,
                   gap=280,
                   min_height=50,
                   max_height=400,
                   distance=650):
    pipes = []

    start_x = WIDTH

    for i in range(count):
        height = randint(min_height, max_height)

        top_pipe = pygame.Rect(
            start_x,
            0,
            pipe_width,
            height
        )

        bottom_pipe = pygame.Rect(
            start_x,
            height + gap,
            pipe_width,
            HEIGHT - (height + gap)
        )

        pipes.append((top_pipe, bottom_pipe))
        start_x += distance

    return pipes


pipes = generate_pipes(150)

font = pygame.font.Font(None, 100)

score = 0
lose = False
y_vel = 2


running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill("sky blue")

    pygame.draw.rect(window, RED, player_rect)

    for top_pipe, bottom_pipe in pipes:
        pygame.draw.rect(window, GREEN, top_pipe)
        pygame.draw.rect(window, GREEN, bottom_pipe)

        if top_pipe.x == 100:
            score += 0.9

        if (
            player_rect.colliderect(top_pipe)
            or player_rect.colliderect(bottom_pipe)
        ):
            lose = True

    if len(pipes) < 8:
        pipes += generate_pipes(150)

    score_text = font.render(
        f"{int(score)}",
        True,
        BLACK
    )

    window.blit(
        score_text,
        score_text.get_rect(center=(WIDTH // 2, 48))
    )

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and not lose:
        player_rect.y -= 15

    if keys[pygame.K_s] and not lose:
        player_rect.y += 15

    if keys[pygame.K_r] and lose:
        score = 0
        lose = False
        pipes = generate_pipes(150)

        player_rect.y = HEIGHT // 2 - 100
        y_vel = 2

    if player_rect.y + player_rect.height > HEIGHT:
        lose = True

    if not lose:
        for top_pipe, bottom_pipe in pipes:
            top_pipe.x -= 10
            bottom_pipe.x -= 10


    pygame.display.update()
    clock.tick(60)

pygame.quit()