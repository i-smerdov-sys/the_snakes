
import random
import sys

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 20

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

CENTER_POSITION = (
    SCREEN_WIDTH // 2,
    SCREEN_HEIGHT // 2
)

DIRECTION_MAP = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self):
        """Инициализирует базовые атрибуты объекта."""
        self.position = CENTER_POSITION
        self.body_color = None

    def draw(self):
        """Заготовка метода отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку и стирает её последний сегмент."""
        for position in self.positions:
            rect = pygame.Rect(
                position,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last is not None:
            last_rect = pygame.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                screen,
                BOARD_BACKGROUND_COLOR,
                last_rect
            )
            self.last = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = random.choice(
            [UP, DOWN, LEFT, RIGHT]
        )
        self.next_direction = None
        self.last = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            snake.next_direction = DIRECTION_MAP.get(
                (event.key, snake.direction),
                snake.direction
            )


def main():
    """Запускает игру «Изгиб Питона»."""
    global screen

    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    pygame.display.set_caption('Изгиб Питона')

    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while apple.position in snake.positions:
        apple.randomize_position()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

        if (
            snake.length > 1
            and snake.get_head_position() in snake.positions[1:]
        ):
            snake.reset()

            while apple.position in snake.positions:
                apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
