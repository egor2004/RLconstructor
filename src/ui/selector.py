import pygame as pg
from os import path

class Selector:
    COLORS = ["white", "black", "gray", "yellow", "red", "purple"]

    def __init__(self):
        self.width = 480
        self.height = 80
        self.surface = pg.Surface((self.width, self.height))
        self.selected_item = 0
        self.cell_size = 44

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

        self.images = [self.grass1_img, self.fence_img, self.agent_img, self.reward_img, self.thorns_img, self.cliff_img]

    def render(self):
        self.surface.fill((200,200, 200))
        pg.draw.rect(self.surface,"black", (0, 0, self.width, self.height), border_radius=10)
        pg.draw.rect(self.surface, "white", (5, 5, self.width - 10, self.height - 10), border_radius=10)
        for i, image in enumerate(self.images):
            x = i * 82 + 10
            rect_color = "black" if i == self.selected_item else (100, 100, 100)
            pg.draw.rect(self.surface, rect_color, (x + 0, 10, 50, 50), border_radius=10)

            # Создаем новую поверхность с альфа-каналом
            rounded_surface = pg.Surface((self.cell_size, self.cell_size), pg.SRCALPHA)
            # Создаем белый круг с прозрачностью
            rect = rounded_surface.get_rect()
            pg.draw.rect(rounded_surface, (255, 255, 255, 0), rect)  # Прозрачный фон
            pg.draw.rect(rounded_surface, (255, 255, 255), rect, border_radius=10)  # Белый с закруглениями

            # Маска: удаляем все, что не внутри круга
            if i == 0 or i == 5:
                rounded_surface.blit(image, (0, 0), special_flags=pg.BLEND_RGBA_MIN)
            else:
                rounded_surface.blit(self.grass1_img, (0, 0), special_flags=pg.BLEND_RGBA_MIN)
                rounded_surface.blit(image, (0, 0))




            self.surface.blit(rounded_surface, (x+3, 13),)



    def update(self, mouse_x, mouse_y):
        for i in range(len(self.COLORS)):
            x1 = i * 82 + 10
            y1 = 10
            x2 = x1 + 50
            y2 = y1 + 50
            if (x1 <= mouse_x < x2 and
                y1 <= mouse_y < y2):
                self.selected_item = i

