import math
import sys
import pygame

pygame.init()

# -------------------- НАСТРОЙКИ --------------------
WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 110
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

# -------------------- ШРИФТЫ --------------------
font = pygame.font.SysFont("arial", 22, bold=True)
small_font = pygame.font.SysFont("arial", 18, bold=True)

# -------------------- ЦВЕТА --------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (235, 235, 235)
DARK_GRAY = (70, 70, 70)
BLUE = (70, 120, 255)
RED = (220, 60, 60)
GREEN = (60, 170, 80)
YELLOW = (255, 210, 0)
PURPLE = (170, 90, 220)
ORANGE = (255, 150, 60)
CYAN = (60, 210, 210)
PINK = (255, 120, 180)

# -------------------- ХОЛСТ --------------------
canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

# -------------------- РЕЖИМЫ --------------------
tool = "pen"  # pen, rect, circle, eraser
selected_color = BLACK
drawing = False
start_pos = None
last_pos = None

# Толщина кисти
brush_size = 6
eraser_size = 24

# -------------------- КНОПКИ --------------------
tool_buttons = {
    "pen": pygame.Rect(20, 20, 90, 35),
    "rect": pygame.Rect(120, 20, 110, 35),
    "circle": pygame.Rect(240, 20, 110, 35),
    "eraser": pygame.Rect(360, 20, 110, 35),
    "clear": pygame.Rect(490, 20, 90, 35),
    "save": pygame.Rect(590, 20, 90, 35),
}

color_buttons = [
    ("black", BLACK, pygame.Rect(710, 20, 32, 32)),
    ("red", RED, pygame.Rect(750, 20, 32, 32)),
    ("green", GREEN, pygame.Rect(790, 20, 32, 32)),
    ("blue", BLUE, pygame.Rect(830, 20, 32, 32)),
    ("yellow", YELLOW, pygame.Rect(870, 20, 32, 32)),
    ("purple", PURPLE, pygame.Rect(910, 20, 32, 32)),
    ("orange", ORANGE, pygame.Rect(950, 20, 32, 32)),
]


def draw_button(rect, text, active=False):
    """Рисует кнопку инструмента."""
    color = (210, 210, 210) if active else (245, 245, 245)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, DARK_GRAY, rect, 2, border_radius=8)

    label = small_font.render(text, True, BLACK)
    screen.blit(label, label.get_rect(center=rect.center))


def draw_toolbar():
    """Рисует панель инструментов и цвета."""
    pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, DARK_GRAY, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 2)

    draw_button(tool_buttons["pen"], "Pen", tool == "pen")
    draw_button(tool_buttons["rect"], "Rect", tool == "rect")
    draw_button(tool_buttons["circle"], "Circle", tool == "circle")
    draw_button(tool_buttons["eraser"], "Eraser", tool == "eraser")
    draw_button(tool_buttons["clear"], "Clear")
    draw_button(tool_buttons["save"], "Save")

    # Цветовые кнопки
    for _, color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect, border_radius=6)
        pygame.draw.rect(screen, DARK_GRAY, rect, 2, border_radius=6)

        # Отмечаем выбранный цвет рамкой
        if color == selected_color:
            pygame.draw.rect(screen, BLACK, rect.inflate(6, 6), 2, border_radius=8)

    # Подпись
    info = font.render(f"Tool: {tool}   Color", True, BLACK)
    screen.blit(info, (20, 70))


def in_canvas(pos):
    """Проверяет, находится ли мышь внутри холста."""
    return pos[1] >= TOOLBAR_HEIGHT


def canvas_pos(pos):
    """Переводит координаты окна в координаты холста."""
    return (pos[0], pos[1] - TOOLBAR_HEIGHT)


def draw_line(surface, color, start, end, size):
    """Рисует линию на поверхности."""
    pygame.draw.line(surface, color, start, end, size)


def draw_rect_shape(surface, color, start, end, size):
    """Рисует прямоугольник по двум точкам."""
    x1, y1 = start
    x2, y2 = end
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    pygame.draw.rect(surface, color, (left, top, width, height), size)


def draw_circle_shape(surface, color, start, end, size):
    """Рисует окружность с центром в start и радиусом по расстоянию до end."""
    radius = int(math.dist(start, end))
    pygame.draw.circle(surface, color, start, radius, size)


def clear_canvas():
    """Очищает холст."""
    canvas.fill(WHITE)


def save_canvas():
    """Сохраняет рисунок в файл."""
    pygame.image.save(canvas, "paint_saved.png")
    print("Saved to paint_saved.png")


# -------------------- ОСНОВНОЙ ЦИКЛ --------------------
while True:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Горячие клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool = "pen"
            elif event.key == pygame.K_2:
                tool = "rect"
            elif event.key == pygame.K_3:
                tool = "circle"
            elif event.key == pygame.K_4:
                tool = "eraser"
            elif event.key == pygame.K_c:
                clear_canvas()
            elif event.key == pygame.K_s:
                save_canvas()

        # Нажатие мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Кнопки сверху
            if tool_buttons["pen"].collidepoint(mouse_pos):
                tool = "pen"
            elif tool_buttons["rect"].collidepoint(mouse_pos):
                tool = "rect"
            elif tool_buttons["circle"].collidepoint(mouse_pos):
                tool = "circle"
            elif tool_buttons["eraser"].collidepoint(mouse_pos):
                tool = "eraser"
            elif tool_buttons["clear"].collidepoint(mouse_pos):
                clear_canvas()
            elif tool_buttons["save"].collidepoint(mouse_pos):
                save_canvas()
            else:
                # Цвета
                clicked_color = False
                for _, color, rect in color_buttons:
                    if rect.collidepoint(mouse_pos):
                        selected_color = color
                        tool = "pen"  # после выбора цвета удобно вернуться к кисти
                        clicked_color = True
                        break

                # Работа на холсте
                if not clicked_color and in_canvas(mouse_pos):
                    drawing = True
                    start_pos = canvas_pos(mouse_pos)
                    last_pos = start_pos

                    # Для кисти и ластика сразу ставим первый штрих
                    if tool == "pen":
                        pygame.draw.circle(canvas, selected_color, start_pos, brush_size // 2)
                    elif tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, start_pos, eraser_size // 2)

        # Движение мыши
        if event.type == pygame.MOUSEMOTION and drawing:
            current_pos = canvas_pos(mouse_pos)

            if tool == "pen":
                draw_line(canvas, selected_color, last_pos, current_pos, brush_size)
                last_pos = current_pos

            elif tool == "eraser":
                draw_line(canvas, WHITE, last_pos, current_pos, eraser_size)
                last_pos = current_pos

        # Отпускание мыши
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and start_pos is not None and in_canvas(mouse_pos):
                end_pos = canvas_pos(mouse_pos)

                if tool == "rect":
                    draw_rect_shape(canvas, selected_color, start_pos, end_pos, brush_size)

                elif tool == "circle":
                    draw_circle_shape(canvas, selected_color, start_pos, end_pos, brush_size)

            drawing = False
            start_pos = None
            last_pos = None

    # -------------------- ОТРИСОВКА --------------------
    screen.fill(WHITE)
    draw_toolbar()

    # Показываем холст
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    # Предпросмотр фигур при удержании мыши
    if drawing and start_pos is not None and in_canvas(mouse_pos):
        preview = canvas.copy()
        end_pos = canvas_pos(mouse_pos)

        if tool == "rect":
            draw_rect_shape(preview, selected_color, start_pos, end_pos, brush_size)

        elif tool == "circle":
            draw_circle_shape(preview, selected_color, start_pos, end_pos, brush_size)

        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    pygame.display.flip()