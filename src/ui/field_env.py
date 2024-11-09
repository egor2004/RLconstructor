import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame as pg
from os import path


class FieldEnv(gym.Env):
    COLORS = {0: "white", 1: "black", 2: "gray", 3: "yellow", 4: "red", 5: "purple"}

    def __init__(self, cell_size=70, field_size_x=8, field_size_y=8, margin=1):
        super(FieldEnv, self).__init__()

        self.render_mode = None

        # Параметры поля
        self.cell_size = cell_size
        self.field_size_x = field_size_x
        self.field_size_y = field_size_y
        self.margin = margin
        self.width = self.cell_size * self.field_size_x + self.margin * (self.field_size_x + 1)
        self.height = self.cell_size * self.field_size_y + self.margin * (self.field_size_y + 1)
        self.surface = pg.Surface((self.width, self.height))

        # Инициализация изображений
        self.agent_img = None
        self.reward_img = None
        self.background_img = None

        # Параметры агента
        self.agent_pos = [0, 0]  # Начальное положение
        self.field = [[0] * self.field_size_x for _ in range(self.field_size_y)]
        self.field[0][0] = 2  # Положение агента в начальной точке

        # Gym API: Пространство действий и наблюдений
        self.action_space = spaces.Discrete(4)  # 4 действия: влево, вверх, вправо, вниз
        self.observation_space = spaces.Box(low=0, high=5, shape=(self.field_size_y, self.field_size_x), dtype=np.int32)
        self.steps = 0
        self.max_steps = 10

    def reset(self):
        """Сбрасывает состояние среды до начального состояния."""
        self.agent_pos = [0, 0]
        self.field = [[0] * self.field_size_x for _ in range(self.field_size_y)]
        self.field[0][0] = 2  # Позиция агента
        return np.array(self.field, dtype=np.int32)

    def step(self, action):
        """Выполняет действие агента и возвращает новое состояние, награду, флаг завершения и доп. информацию."""
        x, y = self.agent_pos
        new_pos = list(self.agent_pos)

        # Определяем новое положение в зависимости от действия
        if action == 0 and x > 0 and self.field[y][x-1] != 1:  # Влево
            new_pos[0] -= 1
        elif action == 1 and y > 0 and self.field[y-1][x] != 1:  # Вверх
            new_pos[1] -= 1
        elif (action == 2 and x < self.field_size_x - 1 and
                self.field[y][x+1] != 1):  # Вправо
            new_pos[0] += 1
        elif (action == 3 and y < self.field_size_y - 1 and
                self.field[y+1][x] != 1):  # Вниз
            new_pos[1] += 1

        # Проверка на препятствия и обновление поля
        reward = 0
        done = False
        if self.field[new_pos[1]][new_pos[0]] == 4:  # Наказание
            reward = -10
        elif self.field[new_pos[1]][new_pos[0]] == 3:  # Награда
            reward = 10
        elif self.field[new_pos[1]][new_pos[0]] == 5:  # Награда
            reward = -100
            done = True

        # Обновляем позицию агента на поле
        self.field[y][x] = 0
        self.field[new_pos[1]][new_pos[0]] = 2
        self.agent_pos = new_pos

        # Проверка на превышение количества допустимых шагов
        self.steps += 1
        if self.steps > self.max_steps:
            self.steps = 0
            done = True
        # Возвращаем состояние, награду, флаг завершения и пустой словарь
        return np.array(self.field, dtype=np.int32), reward, done, {}

    def render(self, mode="human"):
        """Отображает текущее состояние среды."""
        if self.agent_img is None:
            file_name = path.join(path.dirname(__file__), "img/elf_down.png")
            self.agent_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))

        if self.reward_img is None:
            file_name = path.join(path.dirname(__file__), "img/cookie.png")
            self.reward_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))

        if self.background_img is None:
            file_name = path.join(path.dirname(__file__), "img/taxi_background.png")
            self.background_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))

        color = "black"
        pg.draw.rect(self.surface, color, (0, 0, self.width, self.height), border_radius=5)

        for row in range(self.field_size_x):
            for col in range(self.field_size_y):
                color = self.COLORS.get(self.field[col][row], "white")

                x = row * self.cell_size + (row + 1) * self.margin
                y = col * self.cell_size + (col + 1) * self.margin

                # Рисуем фон или объекты на основе текущего состояния клетки
                self.surface.blit(self.background_img, (x, y))
                if self.field[col][row] == 0:
                    self.surface.blit(self.background_img, (x, y))
                elif self.field[col][row] == 1:
                    pg.draw.rect(self.surface, color, (x, y, self.cell_size, self.cell_size))
                elif self.field[col][row] == 2:
                    self.surface.blit(self.agent_img, (x, y))
                elif self.field[col][row] == 3:
                    self.surface.blit(self.reward_img, (x, y))
                elif self.field[col][row] == 4:
                    pg.draw.rect(self.surface, color, (x, y, self.cell_size, self.cell_size))
                elif self.field[col][row] == 5:
                    pg.draw.rect(self.surface, color, (x, y, self.cell_size, self.cell_size))


    def update(self, mouse_x, mouse_y, item=0):
        """Позволяет обновить содержимое клетки по клику."""
        row = mouse_x // (self.cell_size + self.margin)
        col = mouse_y // (self.cell_size + self.margin)
        if item == 2:
            self.field[self.agent_pos[1]][self.agent_pos[0]] = 0
            self.agent_pos = [row, col]
        if self.field[col][row] != 2:
            self.field[col][row] = item
