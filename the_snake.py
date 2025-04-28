from random import choice, randint

import pygame as pg

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


def quit():
    """Выход из программы"""
    pg.quit()
    raise SystemExit


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
        elif event.type == pg.KEYDOWN:
            handle_keydown(event, game_object)


def handle_keydown(event: pg.event.Event, game_object) -> None:
    """Обработка нажатия клавиш."""
    if event.key == pg.K_UP and game_object.direction != DOWN:
        game_object.update_direction(UP)
    elif event.key == pg.K_DOWN and game_object.direction != UP:
        game_object.update_direction(DOWN)
    elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
        game_object.update_direction(LEFT)
    elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
        game_object.update_direction(RIGHT)
    elif event.key == pg.K_ESCAPE:
        quit()
    elif event.key == pg.K_1:
        game_object.speed -= 1
    elif event.key == pg.K_2:
        game_object.speed += 1


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self,
                 color: tuple = SNAKE_COLOR,
                 position: tuple = START_POSITION) -> None:
        """Инициализатор класса."""
        self.position: tuple = position
        self.body_color: tuple = color

    def draw(self) -> None:
        """Абстрактный метод."""

    def draw_one_cell(self,
                      position: tuple,
                      color: tuple | None = None,
                      border_color: tuple = BORDER_COLOR) -> None:
        """Отрисовка одной клетки"""
        color = color or self.body_color
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self,
                 occupied_cells: list[tuple[int, int]] | None = None,
                 color: tuple = APPLE_COLOR,
                 position: tuple = START_POSITION) -> None:
        """Инициализатор класса."""
        super().__init__(color, position)
        occupied_cells = occupied_cells or []
        self.randomize_position(occupied_cells)

    def randomize_position(self,
                           occupied_cells: list[tuple[int, int]]) -> None:
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break

    def draw(self) -> None:
        """Отрисовка яблока."""
        self.draw_one_cell(self.position)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self,
                 color: tuple = SNAKE_COLOR,
                 position: tuple = START_POSITION) -> None:
        """Инициализатор класса."""
        super().__init__(color, position)
        self.last: tuple
        self.reset()
        self.direction: tuple = RIGHT

    def reset(self) -> None:
        """Устанавливает начальное состояние змейки."""
        self.length: int = 1
        self.positions: list[tuple] = [self.position]
        self.speed: int = SPEED
        self.direction = choice((RIGHT, LEFT, UP, DOWN))

    def move(self) -> None:
        """Обновляет позицию змейки."""
        x_head_position, y_head_position = self.get_head_position()
        dx, dy = self.direction
        new_x_head_pos = (
            x_head_position + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y_head_pos = (
            y_head_position + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_x_head_pos, new_y_head_pos)
        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def eating_apple(self) -> None:
        """Яблоко съедено"""
        self.speed += 1
        self.length += 1

    def update_direction(self, direction: tuple) -> None:
        """Обновляет направление движения змейки."""
        self.direction = direction

    def draw(self) -> None:
        """Отрисовка змейки."""
        # Затираем хвост.
        self.draw_one_cell(self.last, BOARD_BACKGROUND_COLOR,
                           BOARD_BACKGROUND_COLOR)
        # Рисуем голову.
        self.draw_one_cell(self.get_head_position())

    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змейки."""
        return self.positions[0]


def main() -> None:
    """Главная функция."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:

        clock.tick(snake.speed)

        # Обработка клавиш.
        handle_keys(snake)

        # Обновление позиций.
        snake.move()
        head_position = snake.get_head_position()
        
        # Логика съедения яблока.
        if head_position == apple.position:
            snake.eating_apple()
            apple.randomize_position(snake.positions)

        # Столкновение с хвостом.
        elif head_position in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка.
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
