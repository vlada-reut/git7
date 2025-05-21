import pygame
import os
import random
import sys

pygame.init()
pygame.font.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Образовательная игра: Арифметика")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (255, 200, 200)
LIGHT_BLUE = (173, 216, 230)

DIGITS_PATH = "digits"
SYMBOLS_PATH = "symbols"

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

DIGIT_SIZE = (150, 150)
digit_images = {
    str(d): pygame.transform.scale(
        pygame.image.load(os.path.join(DIGITS_PATH, f"{d}.png")), DIGIT_SIZE
    )
    for d in range(10)
}
minus_image = pygame.transform.scale(
    pygame.image.load(os.path.join(DIGITS_PATH, "minus.png")), DIGIT_SIZE
)

SYMBOL_SIZE = (150, 150)
symbol_images = {
    "+": pygame.transform.scale(pygame.image.load(os.path.join(SYMBOLS_PATH, "plus.png")), SYMBOL_SIZE),
    "-": pygame.transform.scale(pygame.image.load(os.path.join(SYMBOLS_PATH, "minus.png")), SYMBOL_SIZE),
    "*": pygame.transform.scale(pygame.image.load(os.path.join(SYMBOLS_PATH, "multiply.png")), SYMBOL_SIZE),
    "/": pygame.transform.scale(pygame.image.load(os.path.join(SYMBOLS_PATH, "divide.png")), SYMBOL_SIZE),
    "?": pygame.transform.scale(pygame.image.load(os.path.join(SYMBOLS_PATH, "question.png")), SYMBOL_SIZE),
    "=": pygame.transform.scale(pygame.image.load(os.path.join(SYMBOLS_PATH, "equal.png")), SYMBOL_SIZE)
}

def render_number(number):
    str_number = str(number)
    parts = []
    for ch in str_number:
        if ch == "-":
            parts.append(minus_image)
        else:
            parts.append(digit_images[ch])
    total_width = sum(part.get_width() - 20 for part in parts) + 20
    max_height = max(part.get_height() for part in parts)
    surface = pygame.Surface((total_width, max_height), pygame.SRCALPHA)
    x = 0
    for part in parts:
        surface.blit(part, (x, 0))
        x += part.get_width() - 20
    return surface

def generate_problem():
    op = random.choice(["+", "-", "*", "/"])
    if op == "*":
        a = random.randint(0, 10)
        b = random.randint(0, 10)
    elif op == "/":
        b = random.randint(1, 10)
        answer = random.randint(1, 10)
        a = b * answer
    else:
        a = random.randint(0, 100)
        b = random.randint(0, 100)
    answer = eval(f"{a}{op}{b}")
    return a, b, op, int(answer)

def generate_choices(correct_answer):
    choices = [correct_answer]
    while len(choices) < 3:
        fake = correct_answer + random.randint(-10, 10)
        if fake != correct_answer and fake not in choices:
            choices.append(fake)
    random.shuffle(choices)
    return choices

def render_problem(a, b, op):
    parts = [
        render_number(a),
        symbol_images[op],
        render_number(b),
        symbol_images["="],
        symbol_images["?"]
    ]
    total_width = sum(p.get_width() + 5 for p in parts) - 5
    max_height = max(p.get_height() for p in parts)
    x = (SCREEN_WIDTH - total_width) // 2
    y = 100
    for part in parts:
        screen.blit(part, (x, y))
        x += part.get_width() + 5

def main():
    clock = pygame.time.Clock()
    a, b, op, correct_answer = generate_problem()
    choices = generate_choices(correct_answer)

    feedback_color = None
    feedback_timer = 0
    selected = None

    running = True
    while running:
        if feedback_color:
            screen.fill(feedback_color)
        else:
            screen.blit(background, (0, 0))

        render_problem(a, b, op)

        option_surfaces = [render_number(choice) for choice in choices]
        spacing = 60
        total_width = sum(s.get_width() + spacing for s in option_surfaces) - spacing
        x = (SCREEN_WIDTH - total_width) // 2
        y = 300

        option_rects = []
        for i, surf in enumerate(option_surfaces):
            rect = surf.get_rect(topleft=(x, y))
            border_rect = rect.inflate(30, 30)
            pygame.draw.rect(screen, LIGHT_BLUE, border_rect, border_radius=25)
            pygame.draw.rect(screen, BLACK, border_rect, 3, border_radius=25)
            screen.blit(surf, rect.topleft)
            option_rects.append((choices[i], border_rect))
            x += surf.get_width() + spacing

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for value, rect in option_rects:
                    if rect.collidepoint(pos):
                        selected = value
                        if selected == correct_answer:
                            feedback_color = LIGHT_GREEN
                        else:
                            feedback_color = LIGHT_RED
                        feedback_timer = pygame.time.get_ticks()

        # Обновляем задачу после задержки
        if feedback_color and pygame.time.get_ticks() - feedback_timer > 1000:
            feedback_color = None
            a, b, op, correct_answer = generate_problem()
            choices = generate_choices(correct_answer)
            selected = None

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
