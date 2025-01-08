from ui.renderer import Renderer
from src.environment.field_env import FieldEnv
from ui.selector import Selector
from agent.agent import *
from ui.slider import Slider
from ui.btn import Button
import pygame as pg
import time

pg.init()

env = FieldEnv(95, 5, 5, margin=1)
selector = Selector()
slider = Slider()
btn = Button(0, 0, 200, 50, "Обучить", pg.font.Font(None, 36), (150, 150, 150), (0,0,0))

surfaces = [
    {"surface": env, "position": (30, 120)},
    {"surface": selector, "position": (30, 20)},
    {"surface": slider, "position": (600, 120)},
    {"surface": btn, "position": (670, 470)},
]
renderer = Renderer(1024, 640, surfaces)

fps = 60
clock = pg.time.Clock()


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

        loc_slider_x = x - surfaces[2]["position"][0]
        loc_slider_y = y - surfaces[2]["position"][1]
        if (0 <= loc_slider_x < slider.width and
                0 <= loc_slider_y < slider.height):
            slider.update(loc_slider_x, loc_slider_y, is_dragging=True)
            slider.selected_slider = None




def check_events():
    global constructor
    global running
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_f:
                constructor = not constructor
            if event.key == pg.K_r:
                env.reset()
            if event.key == pg.K_s:
                print("Карта сохранена")
                env.remember_field()

def train_start():
    global constructor
    env.remember_field()
    trainModel()
    env.mem_reset()
    constructor = True

running = True
constructor = True
def main_loop():
    global constructor
    while running:
        check_events()

        if constructor == False:
            train_start()
        else:
            mouse_click()
        renderer.update()
        clock.tick(fps)


def trainModel():
    global env
    agent = Agent(env.field_size_x, 4)
    for episode in range (NUM_EPISODES):
        env.mem_reset()
        state = env.state
        total_reward = 0
        done = False

        while not done:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            agent.replay()
            state = next_state
            total_reward += reward

        if episode % TARGET_UPDATE == 0:
            agent.update_target()

        agent.epsilon = max(EPSILON_MIN, agent.epsilon * EPSILON_DECAY)
        print(f"Episode {episode + 1}, Total Reward: {total_reward}")

    print("Training complete.")

    env.mem_reset()
    state = env.state
    done = False
    renderer.update()
    last_move_time = time.time()
    agent_moves_per_second = 1
    move_interval = 1.0 / agent_moves_per_second
    total_reward = 0
    while not done:
        correct_time = time.time()
        if correct_time - last_move_time >= move_interval:
            last_move_time = correct_time
            action = torch.argmax(agent.target_model(state)).item()
            next_state, reward, done = env.step(action)
            state = next_state
            renderer.update()
            total_reward += reward

    print(f"Итоговая оценка: {total_reward}")



if __name__ == "__main__":
    main_loop()

