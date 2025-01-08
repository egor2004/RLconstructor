import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame as pg
from os import path
import copy



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
        self.field = [[0] * self.field_size_x for _ in range(self.field_size_y)]
        self.mem_field = None
        self.surface = pg.Surface((self.width, self.height))

        # Инициализация изображений
        file_name = path.join(path.dirname(__file__), "../ui/img/elf.png")
        self.agent_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))
        file_name = path.join(path.dirname(__file__), "../ui/img/cookie.png")
        self.reward_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))
        file_name = path.join(path.dirname(__file__), "../ui/img/grass1.png")
        self.grass1_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))
        file_name = path.join(path.dirname(__file__), "../ui/img/grass2.png")
        self.grass2_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))
        file_name = path.join(path.dirname(__file__), "../ui/img/cliff_red.png")
        self.cliff_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))
        file_name = path.join(path.dirname(__file__), "../ui/img/fence_red.png")
        self.fence_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))
        file_name = path.join(path.dirname(__file__), "../ui/img/thorns.png")
        self.thorns_img = pg.transform.scale(pg.image.load(file_name), (self.cell_size, self.cell_size))

        # Параметры награды
        self.cookie_pos = None

        # Параметры агента
        self.agent_pos = [0, 0]  # Начальное положение
        self.mem_agent_pos = None

        self.state = None
        self.update_state()
        self.mem_state = None

        # Gym API: Пространство действий и наблюдений
        self.action_space = spaces.Discrete(4)  # 4 действия: влево, вверх, вправо, вниз
        self.observation_space = spaces.Box(low=0, high=5, shape=(self.field_size_y, self.field_size_x), dtype=np.int32)
        self.steps = 0
        self.max_steps = 20

    def remember_field(self):
        self.mem_field = copy.deepcopy(self.field)
        self.mem_agent_pos = self.agent_pos.copy()
        self.mem_state = copy.deepcopy(self.state)

    def forget_field(self):
        self.mem_field = None
        self.mem_agent_pos = None
        self.mem_state = None

    def update_state(self):
        self.state = self.agent_pos[0] + self.field_size_y * self.agent_pos[1]

    def mem_reset(self):
        """Сбрасывает состояние среды до запомненного состояния."""
        self.agent_pos = self.mem_agent_pos.copy()
        self.field = copy.deepcopy(self.mem_field)
        self.state = copy.deepcopy(self.mem_state)
        self.steps = 0




    def reset(self):
        """Сбрасывает состояние среды до запомненного или начального состояния."""
        if ((self.mem_field is None) or
        (self.mem_field == self.field and self.mem_agent_pos == self.agent_pos)):
            self.agent_pos = [0, 0]
            self.field = [[0] * self.field_size_x for _ in range(self.field_size_y)]

            self.update_state()

            self.forget_field()
        else:
            self.agent_pos = self.mem_agent_pos.copy()
            self.field = copy.deepcopy(self.mem_field)
            self.state = copy.deepcopy(self.mem_state)
        self.steps = 0
        return self.state

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
            reward = -5
        elif self.field[new_pos[1]][new_pos[0]] == 3:  # Награда
            reward = 100
            done = True
        elif self.field[new_pos[1]][new_pos[0]] == 5:  # Смерть
            reward = -10
            done = True
        elif self.field[new_pos[1]][new_pos[0]] == 0:  # Ход
            reward = -1

        self.agent_pos = new_pos

        # Проверка на превышение количества допустимых шагов
        self.steps += 1
        if self.steps > self.max_steps:
            self.steps = 0
            done = True
        # Возвращаем состояние, награду, флаг завершения и пустой словарь
        self.update_state()


        return self.state, reward, done

    def render(self, mode="human"):
        """Отображает текущее состояние среды."""
        color = "black"
        pg.draw.rect(self.surface, color, (0, 0, self.width, self.height), border_radius=5)

        for row in range(self.field_size_x):
            for col in range(self.field_size_y):
                color = self.COLORS.get(self.field[col][row], "white")

                x = row * self.cell_size + (row + 1) * self.margin
                y = col * self.cell_size + (col + 1) * self.margin

                # Рисуем фон или объекты на основе текущего состояния клетки

                if (row + col) % 2 == 0:
                    self.surface.blit(self.grass1_img, (x, y))
                else:
                    self.surface.blit(self.grass2_img, (x, y))
                if self.field[col][row] == 1:
                    self.surface.blit(self.fence_img, (x, y))
                elif self.field[col][row] == 3:
                    self.surface.blit(self.reward_img, (x, y))
                elif self.field[col][row] == 4:
                    self.surface.blit(self.thorns_img, (x, y))
                elif self.field[col][row] == 5:
                    self.surface.blit(self.cliff_img, (x, y))

        x_ag = self.agent_pos[0] * self.cell_size + (self.agent_pos[0] + 1) * self.margin
        y_ag = self.agent_pos[1] * self.cell_size + (self.agent_pos[1] + 1) * self.margin
        self.surface.blit(self.agent_img, (x_ag, y_ag))


    def update(self, mouse_x, mouse_y, item=0):
        """Позволяет обновить содержимое клетки по клику."""
        row = mouse_x // (self.cell_size + self.margin)
        col = mouse_y // (self.cell_size + self.margin)
        if item == 2:
            self.field[self.agent_pos[1]][self.agent_pos[0]] = 0
            self.agent_pos = [row, col]




        if [row, col] != self.agent_pos:
            # Ставим печеньку, увеличиваем переменную
            if item == 3:
                if self.cookie_pos != None:
                    self.field[self.cookie_pos[1]][self.cookie_pos[0]] = 0
                    self.cookie_pos = [row, col]
                else:
                    self.cookie_pos = [row, col]
            # Добавляем элемент на поле
            self.field[col][row] = item

        self.update_state()



