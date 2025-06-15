
import pygame  # Основная библиотека для создания игр
import random  # Для генерации случайных чисел
import sys  # Для работы с системными функциями
import os  # Для работы с файловой системой


pygame.init()

# Константы для настройки игрового поля
CELL_SIZE = 40  # Размер одной клетки в пикселях
GRID_WIDTH = 20  # Ширина игрового поля в клетках
GRID_HEIGHT = 15  # Высота игрового поля в клетках
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH  # Общая ширина экрана
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT  # Общая высота экрана
FPS = 10  # Количество кадров в секунду

# Цвета
BLACK = (0, 0, 0)  # Черный цвет
WHITE = (255, 255, 255)  # Белый цвет

class Game:
    def __init__(self):
        # Создаем экран для игры
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Змейка")  # Устанавливаем заголовок окна
        self.clock = pygame.time.Clock()  # Создаем объект для контроля FPS

        # Загружаем изображения
        self.load_images()

        # Сбрасываем состояние игры
        self.reset_game()

    def load_images(self):
        # Списки для хранения изображений яблок и сегментов змейки
        self.apple_images = []
        self.snake_segments = []

        # Получаем путь к директории скрипта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(script_dir, "assets")  # Путь к папке с ресурсами

        # Загружаем изображения яблок
        apple_count = 0
        while True:
            apple_count += 1
            img_path = os.path.join(assets_dir, f"apple_body_{apple_count}.png")
            if not os.path.exists(img_path):
                break
            try:
                img = pygame.image.load(img_path).convert_alpha()  # Загружаем изображение
                img = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))  # Масштабируем изображение
                self.apple_images.append(img)  # Добавляем изображение в список
            except:
                break

        # Если изображения яблок не найдены, создаем стандартное изображение
        if not self.apple_images:
            print("Не найдены изображения яблок, будет использовано стандартное")
            surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 0, 0), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2)  # Рисуем яблоко
            pygame.draw.circle(surf, (0, 100, 0), (CELL_SIZE // 2, CELL_SIZE // 4), CELL_SIZE // 8)  # Рисуем листик
            self.apple_images.append(surf)

        # Загружаем изображение головы змейки
        snake_img_path = os.path.join(assets_dir, "snake_head.png")
        if os.path.exists(snake_img_path):
            self.snake_head_img = pygame.image.load(snake_img_path).convert_alpha()
            self.snake_head_img = pygame.transform.scale(self.snake_head_img, (CELL_SIZE, CELL_SIZE))
        else:
            self.snake_head_img = None

    def reset_game(self):
        # Сбрасываем состояние игры
        self.snake_coords = [[5, 5]]  # Начальные координаты змейки
        self.snake_types = [0]  # Типы сегментов змейки
        self.generate_apple()  # Генерируем яблоко
        self.direction = (1, 0)  # Начальное направление движения
        self.next_direction = (1, 0)  # Следующее направление движения
        self.game_over = False  # Флаг окончания игры
        self.score = 0  # Счет
        self.snake_length = 1  # Длина змейки

    def generate_apple(self):
        # Генерируем координаты яблока
        while True:
            self.apple_coords = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
            if self.apple_coords not in self.snake_coords:
                break

        self.current_apple_type = random.randint(0, len(self.apple_images) - 1)  # Тип яблока

    def handle_events(self):
        # Обрабатываем события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0, 1):
                    self.next_direction = (0, -1)  # Движение вверх
                elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                    self.next_direction = (0, 1)  # Движение вниз
                elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                    self.next_direction = (-1, 0)  # Движение влево
                elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                    self.next_direction = (1, 0)  # Движение вправо
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()  # Перезапуск игры
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # Выход из игры

    def update(self):
        # Обновляем состояние игры
        if self.game_over:
            return

        self.direction = self.next_direction  # Обновляем направление движения

        head = self.snake_coords[0]  # Координаты головы змейки
        new_head = [
            (head[0] + self.direction[0]) % GRID_WIDTH,  # Новые координаты головы по оси X
            (head[1] + self.direction[1]) % GRID_HEIGHT  # Новые координаты головы по оси Y
        ]

        # Проверяем, не столкнулась ли змейка сама с собой
        if new_head in self.snake_coords:
            self.game_over = True
            return

        # Добавляем новую голову змейки
        self.snake_coords.insert(0, new_head)
        self.snake_types.append(self.current_apple_type)

        # Проверяем, не съела ли змейка яблоко
        if new_head == self.apple_coords:
            self.score += 1  # Увеличиваем счет
            self.snake_length += 1  # Увеличиваем длину змейки
            self.generate_apple()  # Генерируем новое яблоко
        else:
            # Удаляем последний сегмент змейки, если яблоко не было съедено
            self.snake_coords.pop()
            self.snake_types.pop()

    def draw(self):
        # Отрисовываем игровое поле
        self.screen.fill(BLACK)  # Заполняем экран черным цветом

        # Рисуем сетку
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y), (SCREEN_WIDTH, y))

        # Рисуем змейку
        for i, (x, y) in enumerate(self.snake_coords):
            if i == 0:
                # Рисуем голову змейки
                if self.snake_head_img:
                    self.screen.blit(self.snake_head_img, (x * CELL_SIZE, y * CELL_SIZE))
                else:
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                # Рисуем тело змейки
                apple_type = self.snake_types[i]
                if apple_type < len(self.apple_images):
                    self.screen.blit(self.apple_images[apple_type],
                                     (x * CELL_SIZE, y * CELL_SIZE))
                else:
                    pygame.draw.rect(self.screen, (200, 200, 200),
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Рисуем яблоко
        x, y = self.apple_coords
        if self.current_apple_type < len(self.apple_images):
            self.screen.blit(self.apple_images[self.current_apple_type],
                             (x * CELL_SIZE, y * CELL_SIZE))

        # Рисуем счет и длину змейки
        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f"Счет: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        length_text = font.render(f"Длина: {self.snake_length}", True, WHITE)
        self.screen.blit(length_text, (10, 50))

        # Рисуем экран окончания игры
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            font_large = pygame.font.SysFont('Arial', 50, bold=True)
            game_over_text = font_large.render("Игра окончена!", True, (255, 50, 50))

            font_medium = pygame.font.SysFont('Arial', 36)
            score_text = font_medium.render(f"Ваш счет: {self.score}", True, WHITE)

            font_small = pygame.font.SysFont('Arial', 24)
            restart_text = font_small.render("Нажмите R для рестарта", True, WHITE)
            exit_text = font_small.render("ESC для выхода", True, WHITE)

            self.screen.blit(game_over_text,
                             (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 - 80))
            self.screen.blit(score_text,
                             (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                              SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text,
                             (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 + 60))
            self.screen.blit(exit_text,
                             (SCREEN_WIDTH // 2 - exit_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()  # Обновляем экран

    def run(self):
        # Основной цикл игры
        while True:
            self.handle_events()  # Обрабатываем события
            self.update()  # Обновляем состояние игры
            self.draw()  # Отрисовываем игровое поле
            self.clock.tick(FPS)  # Контролируем FPS

# Запускаем игру, если скрипт запущен напрямую
if __name__ == "__main__":
    game = Game()
    game.run()