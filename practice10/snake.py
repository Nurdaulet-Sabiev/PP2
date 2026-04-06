import random
import sys
import pygame

pygame.init()

# -------------------- НАСТРОЙКИ --------------------
CELL = 20
COLS = 30
ROWS = 30
HUD_HEIGHT = 60

WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + HUD_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# -------------------- ШРИФТЫ --------------------
font = pygame.font.SysFont("arial", 24, bold=True)
big_font = pygame.font.SysFont("arial", 48, bold=True)

# -------------------- ЦВЕТА --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK = (35, 35, 35)
GREEN = (40, 180, 60)
GREEN_DARK = (20, 120, 40)
RED = (220, 50, 50)
GRAY = (70, 70, 70)
BLUE = (70, 120, 255)

# -------------------- ИГРОВЫЕ ПЕРЕМЕННЫЕ --------------------
snake = []
direction = (1, 0)
next_direction = (1, 0)
food = (0, 0)

score = 0
level = 1
speed = 8
game_over = False


def spawn_food(snake_body):
    """Создаёт еду в случайной клетке, не попадая на змейку и стены."""
    while True:
        x = random.randint(1, COLS - 2)
        y = random.randint(1, ROWS - 2)
        pos = (x, y)
        if pos not in snake_body:
            return pos


def reset_game():
    """Начало новой игры."""
    global snake, direction, next_direction, food, score, level, speed, game_over

    start_x = COLS // 2
    start_y = ROWS // 2

    snake = [
        (start_x, start_y),
        (start_x - 1, start_y),
        (start_x - 2, start_y),
    ]

    direction = (1, 0)
    next_direction = (1, 0)
    food = spawn_food(snake)

    score = 0
    level = 1
    speed = 8
    game_over = False


def draw_text(text, x, y, color=WHITE, fnt=font):
    surf = fnt.render(text, True, color)
    screen.blit(surf, (x, y))


def draw_cell(pos, color):
    """Рисует клетку игрового поля."""
    x, y = pos
    rect = pygame.Rect(x * CELL, HUD_HEIGHT + y * CELL, CELL, CELL)
    pygame.draw.rect(screen, color, rect)


reset_game()

# -------------------- ОСНОВНОЙ ЦИКЛ --------------------
while True:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()

            if not game_over:
                # Управление направлением
                if event.key == pygame.K_UP:
                    nd = (0, -1)
                    if nd[0] != -direction[0] and nd[1] != -direction[1]:
                        next_direction = nd

                elif event.key == pygame.K_DOWN:
                    nd = (0, 1)
                    if nd[0] != -direction[0] and nd[1] != -direction[1]:
                        next_direction = nd

                elif event.key == pygame.K_LEFT:
                    nd = (-1, 0)
                    if nd[0] != -direction[0] and nd[1] != -direction[1]:
                        next_direction = nd

                elif event.key == pygame.K_RIGHT:
                    nd = (1, 0)
                    if nd[0] != -direction[0] and nd[1] != -direction[1]:
                        next_direction = nd

    if not game_over:
        # Переходим в выбранное направление
        direction = next_direction

        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        # Проверка выхода за границы поля
        if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:
            game_over = True
        else:
            will_eat = (new_head == food)

            # Проверка столкновения с телом
            body_to_check = snake if will_eat else snake[:-1]
            if new_head in body_to_check:
                game_over = True
            else:
                snake.insert(0, new_head)

                if will_eat:
                    score += 1

                    # Каждый 3-й кусочек еды — новый уровень
                    if score % 3 == 0:
                        level += 1
                        speed += 2  # ускоряем игру

                    food = spawn_food(snake)
                else:
                    snake.pop()

    # -------------------- ОТРИСОВКА --------------------
    screen.fill(BLACK)

    # Верхняя панель
    pygame.draw.rect(screen, DARK, (0, 0, WIDTH, HUD_HEIGHT))
    draw_text(f"Score: {score}", 15, 15)
    draw_text(f"Level: {level}", 180, 15)
    draw_text(f"Speed: {speed}", 330, 15)

    # Игровое поле
    pygame.draw.rect(screen, GRAY, (0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT), 4)

    # Стены вокруг поля
    pygame.draw.rect(screen, (55, 55, 55), (0, HUD_HEIGHT, WIDTH, CELL))  # верхняя стена
    pygame.draw.rect(screen, (55, 55, 55), (0, HEIGHT - CELL, WIDTH, CELL))  # нижняя
    pygame.draw.rect(screen, (55, 55, 55), (0, HUD_HEIGHT, CELL, HEIGHT - HUD_HEIGHT))  # левая
    pygame.draw.rect(screen, (55, 55, 55), (WIDTH - CELL, HUD_HEIGHT, CELL, HEIGHT - HUD_HEIGHT))  # правая

    # Еда
    fx, fy = food
    food_rect = pygame.Rect(fx * CELL + 2, HUD_HEIGHT + fy * CELL + 2, CELL - 4, CELL - 4)
    pygame.draw.rect(screen, RED, food_rect, border_radius=5)

    # Змейка
    for i, part in enumerate(snake):
        color = GREEN if i == 0 else GREEN_DARK
        draw_cell(part, color)

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        msg1 = big_font.render("GAME OVER", True, WHITE)
        msg2 = font.render("Press R to restart", True, WHITE)

        screen.blit(msg1, msg1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(msg2, msg2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    pygame.display.flip()