import random
import sys
import pygame

pygame.init()

# -------------------- НАСТРОЙКИ ОКНА --------------------
WIDTH, HEIGHT = 600, 800
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

# -------------------- ШРИФТЫ --------------------
font = pygame.font.SysFont("arial", 28, bold=True)
big_font = pygame.font.SysFont("arial", 56, bold=True)

# -------------------- ЦВЕТА --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
DARK_GRAY = (40, 40, 40)
YELLOW = (255, 220, 0)
GREEN = (30, 130, 30)
RED = (220, 40, 40)
BLUE = (60, 120, 255)

# -------------------- ДОРОГА И ПОЛОСЫ --------------------
ROAD_LEFT = 150
ROAD_RIGHT = 450
LANE_CENTERS = [200, 300, 400]  # 3 полосы

# -------------------- ИГРОВЫЕ ПЕРЕМЕННЫЕ --------------------
player_width = 48
player_height = 90
player_lane = 1
player_rect = pygame.Rect(0, 0, player_width, player_height)
player_rect.centerx = LANE_CENTERS[player_lane]
player_rect.bottom = HEIGHT - 30

coins_collected = 0
distance_score = 0
game_over = False

obstacles = []
coins = []

last_obstacle_spawn = 0
last_coin_spawn = 0
road_scroll = 0


def reset_game():
    """Сброс игры после проигрыша."""
    global player_lane, player_rect, coins_collected, distance_score
    global game_over, obstacles, coins, last_obstacle_spawn, last_coin_spawn, road_scroll

    player_lane = 1
    player_rect.centerx = LANE_CENTERS[player_lane]
    player_rect.bottom = HEIGHT - 30

    coins_collected = 0
    distance_score = 0
    game_over = False

    obstacles = []
    coins = []

    last_obstacle_spawn = 0
    last_coin_spawn = 0
    road_scroll = 0


def spawn_obstacle():
    """Создаёт машину-препятствие в случайной полосе."""
    lane = random.randint(0, 2)
    rect = pygame.Rect(0, 0, 52, 92)
    rect.centerx = LANE_CENTERS[lane]
    rect.y = -100
    speed = random.randint(6, 9)
    return {"rect": rect, "speed": speed}


def spawn_coin():
    """Создаёт монету в случайной полосе."""
    lane = random.randint(0, 2)
    rect = pygame.Rect(0, 0, 24, 24)
    rect.centerx = LANE_CENTERS[lane]
    rect.y = -30
    speed = random.randint(6, 9)
    return {"rect": rect, "speed": speed}


def draw_road():
    """Рисует дорогу и разметку."""
    # Фон
    screen.fill(GREEN)

    # Дорога
    pygame.draw.rect(screen, DARK_GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

    # Границы дороги
    pygame.draw.line(screen, YELLOW, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 6)
    pygame.draw.line(screen, YELLOW, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 6)

    # Прерывистые линии между полосами
    for lane_x in [250, 350]:
        for i in range(0, HEIGHT // 40 + 3):
            y = (i * 40 + road_scroll) % (HEIGHT + 40) - 40
            pygame.draw.rect(screen, WHITE, (lane_x - 3, y, 6, 24))


def draw_text(text, x, y, color=WHITE, fnt=font):
    """Удобный вывод текста."""
    surf = fnt.render(text, True, color)
    screen.blit(surf, (x, y))


def draw_coin(coin_rect):
    """Рисует монету."""
    pygame.draw.circle(screen, YELLOW, coin_rect.center, 12)
    pygame.draw.circle(screen, WHITE, coin_rect.center, 12, 2)


def draw_player():
    """Рисует машину игрока."""
    pygame.draw.rect(screen, BLUE, player_rect, border_radius=8)
    # Окна
    pygame.draw.rect(
        screen,
        (180, 220, 255),
        (player_rect.x + 10, player_rect.y + 12, player_rect.width - 20, 22),
        border_radius=4,
    )
    # Фары
    pygame.draw.rect(screen, (255, 255, 180), (player_rect.x + 4, player_rect.y + 8, 6, 14))
    pygame.draw.rect(screen, (255, 255, 180), (player_rect.right - 10, player_rect.y + 8, 6, 14))


reset_game()

# -------------------- ОСНОВНОЙ ЦИКЛ --------------------
while True:
    dt = clock.tick(FPS)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()

            if not game_over:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    if player_lane > 0:
                        player_lane -= 1
                        player_rect.centerx = LANE_CENTERS[player_lane]

                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    if player_lane < 2:
                        player_lane += 1
                        player_rect.centerx = LANE_CENTERS[player_lane]

    if not game_over:
        # Скорость игры чуть растёт со счётом
        current_speed = 7 + distance_score // 1200

        # Счёт за выживание
        distance_score += current_speed

        # Движение дороги
        road_scroll = (road_scroll + current_speed) % 40

        # Появление препятствий
        if now - last_obstacle_spawn > 1200:
            obstacles.append(spawn_obstacle())
            last_obstacle_spawn = now

        # Появление монет
        if now - last_coin_spawn > 900:
            coins.append(spawn_coin())
            last_coin_spawn = now

        # Обновление препятствий
        for obstacle in obstacles[:]:
            obstacle["rect"].y += obstacle["speed"] + current_speed // 2
            if obstacle["rect"].top > HEIGHT:
                obstacles.remove(obstacle)

            if player_rect.colliderect(obstacle["rect"]):
                game_over = True

        # Обновление монет
        for coin in coins[:]:
            coin["rect"].y += coin["speed"] + current_speed // 2
            if coin["rect"].top > HEIGHT:
                coins.remove(coin)
                continue

            if player_rect.colliderect(coin["rect"]):
                coins_collected += 1
                coins.remove(coin)

    # -------------------- ОТРИСОВКА --------------------
    draw_road()

    for coin in coins:
        draw_coin(coin["rect"])

    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle["rect"], border_radius=8)
        pygame.draw.rect(
            screen,
            (255, 180, 180),
            (obstacle["rect"].x + 10, obstacle["rect"].y + 12, obstacle["rect"].width - 20, 22),
            border_radius=4,
        )

    draw_player()

    # Счётчик монет справа сверху
    coin_text = font.render(f"Coins: {coins_collected}", True, WHITE)
    coin_rect = coin_text.get_rect(topright=(WIDTH - 20, 15))
    screen.blit(coin_text, coin_rect)

    # Дистанция слева сверху
    draw_text(f"Score: {distance_score // 10}", 20, 15, WHITE)

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        msg1 = big_font.render("GAME OVER", True, WHITE)
        msg2 = font.render("Press R to restart", True, WHITE)

        screen.blit(msg1, msg1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
        screen.blit(msg2, msg2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    pygame.display.flip()