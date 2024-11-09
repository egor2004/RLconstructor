from fontTools.merge.util import current_time

from ui.renderer import Renderer
from ui.field_env import FieldEnv
from ui.selector import Selector
from agent.test import *
import pygame as pg
import time

env = FieldEnv(70, 8, 8, margin=1)
selector = Selector()

surfaces = [
    {"surface": env, "position": (30, 120)},
    {"surface": selector, "position": (30, 20)}
]
renderer = Renderer(1024, 720, surfaces)

fps = 60
clock = pg.time.Clock()

agent_moves_per_second = 2
move_interval = 1.0 / agent_moves_per_second
last_move_time = time.time()

def mouse_click():
    # Обработка нажатий на элементы игрового поля и селектора
    x, y = pg.mouse.get_pos()
    b1, b2, b3 = pg.mouse.get_pressed()

    if b1:
        loc_selector_x = x - surfaces[1]["position"][0]
        loc_selector_y = y - surfaces[1]["position"][1]
        if (0 <= loc_selector_x < selector.width and
            0 <= loc_selector_y < selector.height):
            selector.update(loc_selector_x, loc_selector_y)

        loc_field_x = x - surfaces[0]["position"][0]
        loc_field_y = y - surfaces[0]["position"][1]
        if (0 <= loc_field_x < env.width - env.margin and
            0 <= loc_field_y < env.height - env.margin):
            env.update(loc_field_x, loc_field_y, selector.selected_item)


def main_loop():
    global last_move_time
    running = True
    constructor = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    constructor = not constructor
                if event.key == pg.K_r:
                    env.reset()

        if constructor == False:
            current_time = time.time()
            if current_time - last_move_time > move_interval:
                env.step(env.action_space.sample())
                last_move_time = current_time
        else:
            mouse_click()
        renderer.update()
        clock.tick(fps)



if __name__ == "__main__":
    main_loop()