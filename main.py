import pygame

pygame.init()

WIDTH = 800
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#PICS AND THEIR SIZES
dino_image = pygame.image.load("dino.png").convert_alpha()
dino_image = pygame.transform.scale(dino_image, (60,60))
cactus_image = pygame.image.load("cactus.png").convert_alpha()
cactus_image = pygame.transform.scale(cactus_image, (90,70))

pygame.display.set_caption("Chrome Dino Runner")

#DINO CO-ORDINATES
dino_x = 100
dino_y = 280

#INVIS RECTANGLE FOR OUR DINO
dino_rect = pygame.Rect(dino_x, dino_y, 60, 60)

#DINO JUMP VARIABLES
dino_velocity_y = 0
gravity = 1800
jump_strength = -750

ground_y = 280
cactus_positions = [600, 1000, 1400]
is_jumping = False

running = True
game_over = False
game_started = False
score = 0
clock = pygame.time.Clock()


#START SCREEN FONT
start_font = pygame.font.Font(None, 64)


#GAME OVER FONT
game_over_font = pygame.font.Font(None, 64)



game_over_text = game_over_font.render(
    "GAME OVER!", True, (200, 0, 0)
)

game_over_text_rect = game_over_text.get_rect(
    center = (WIDTH // 2, HEIGHT//2)
)


#START SCREEN TEXT
start_text = start_font.render(
    "DINO RUNNER", True, (40,40,40)
)

start_text_rect = start_text.get_rect(
    center = (WIDTH // 2, HEIGHT //2)
)


#SCORE
score_font = pygame.font.Font(None, 64)



# FPS DISPLAY
fps_font = pygame.font.Font(None, 28)



# GAME LOOP
while running:

    # TIME SINCE LAST FRAME
    dt = clock.tick(60) / 1000

    # KEY DETECTION
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # START GAME
            if not game_started:
                if event.key == pygame.K_SPACE:
                    game_started = True

            # RESTART GAME
            elif game_over:
                if event.key == pygame.K_r:
                    game_over = False
                    score = 0

                    dino_x = 100
                    dino_y = 280
                    dino_velocity_y = 0
                    is_jumping = False

                    cactus_positions = [600, 1000, 1400]

            # JUMP
            else:
                if event.key == pygame.K_UP and not is_jumping:
                    dino_velocity_y = jump_strength
                    is_jumping = True

    # START SCREEN
    if not game_started:
        screen.fill((255, 255, 255))

        pygame.draw.line(
            screen, (40, 40, 40),
            (0, 340), (WIDTH, 340), 3
        )

        screen.blit(start_text, start_text_rect)
        pygame.display.flip()

        continue

    # MOVE AND UPDATE GAME ONLY IF NOT GAME OVER
    if not game_over:

        # HORIZONTAL MOVEMENT
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            dino_x += 300 * dt

        if keys[pygame.K_LEFT]:
            dino_x -= 300 * dt

        dino_x = max(0, min(dino_x, WIDTH - 60))

        # JUMP PHYSICS
        dino_y += dino_velocity_y * dt
        dino_velocity_y += gravity * dt

        # LANDING
        if dino_y >= ground_y:
            dino_y = ground_y
            dino_velocity_y = 0
            is_jumping = False

        # UPDATE DINO RECTANGLE
        dino_rect.topleft = (dino_x, dino_y)

        # MOVE CACTI
        for i in range(len(cactus_positions)):
            cactus_positions[i] -= 300 * dt

            if cactus_positions[i] < -cactus_image.get_width():
                cactus_positions[i] = max(cactus_positions) + 400

        # COLLISION DETECTION
        cactus_y = 340 - cactus_image.get_height()

        for cactus_x in cactus_positions:
            cactus_rect = pygame.Rect(
                cactus_x + 23,
                cactus_y + 14,
                24,
                55
            )

            if dino_rect.colliderect(cactus_rect):
                game_over = True

        # UPDATE SCORE
        if not game_over:
            score += 1

    # DRAW EVERYTHING
    screen.fill((255, 255, 255))

    pygame.draw.line(
        screen, (40, 40, 40),
        (0, 340), (WIDTH, 340), 3
    )

    # DRAW CACTI
    cactus_y = 340 - cactus_image.get_height()

    for cactus_x in cactus_positions:
        screen.blit(cactus_image, (cactus_x, cactus_y))

    # DRAW DINO
    screen.blit(dino_image, (dino_x, dino_y))

    # DRAW SCORE
    score_text = score_font.render(
        f"Score: {score // 60}", True, (40, 40, 40)
    )
    screen.blit(score_text, (WIDTH - 190, 20))

    # DRAW FPS
    fps_text = fps_font.render(
        f"FPS: {clock.get_fps():.0f}",
        True, (40, 40, 40)
    )
    screen.blit(fps_text, (20, 20))

    # GAME OVER SCREEN
    if game_over:
        screen.blit(game_over_text, game_over_text_rect)

    pygame.display.flip()

pygame.quit()

