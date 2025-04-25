from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Начальная скорость движения змейки:
SPEED = 5

# Стартовая позиция змейки:
START_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self) -> None:
        """Инициализатор класса."""
        self.position: tuple = START_POSITION
        self.body_color: tuple = SNAKE_COLOR

    def draw(self) -> None:
        """Абстрактный метод."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self) -> None:
        """Инициализатор класса."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self) -> None:
        """Отрисовка яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self) -> None:
        """Инициализатор класса."""
        super().__init__()
        self.next_direction: tuple | None = None
        self.body_color: tuple = SNAKE_COLOR
        self.reset()

    def reset(self) -> None:
        """Устанавливает начальное состояние змейки."""
        self.positions: list = [START_POSITION]
        self.direction: tuple = RIGHT
        self.speed = SPEED

    def move(self, apple: Apple) -> None:
        """Обновляет позицию змейки."""
        head_position = self.get_head_position()
        new_x_head_pos = (
            head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y_head_pos = (
            head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_x_head_pos, new_y_head_pos)

        if new_head_position in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if new_head_position == apple.position:
                self.speed += 1
                apple.randomize_position()
            else:
                self.positions.pop()

    def update_direction(self) -> None:
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self) -> None:
        """Отрисовка змейки."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змейки."""
        return self.positions[0]


def main() -> None:
    """Главная функция."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:

        clock.tick(snake.speed)

        # Обработка клавиш.
        handle_keys(snake)

        # Обновление направления змейки.
        snake.update_direction()

        # Обновление позиций.
        snake.move(apple)

        # Отрисовка.
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
