import pygame as pg

class Slider:
    def __init__(self):
        self.width = 400
        self.height = 400
        self.surface = pg.Surface((self.width, self.height))
        self.dragging = -1
        # Список параметров и их значений
        self.parameters = [
            {"name": "NUM_EPISODES", "value": 20, "min": 1, "max": 100},
            {"name": "BATCH_SIZE", "value": 32, "min": 16, "max": 128},
            {"name": "GAMMA", "value": 0.99, "min": 0.8, "max": 1.0},
            {"name": "EPSILON_START", "value": 1.0, "min": 0.1, "max": 1.0},
            {"name": "EPSILON_MIN", "value": 0.1, "min": 0.01, "max": 0.5},
            {"name": "EPSILON_DECAY", "value": 0.995, "min": 0.9, "max": 1.0},
            {"name": "LEARNING_RATE", "value": 0.001, "min": 0.0001, "max": 0.01},
            {"name": "TARGET_UPDATE", "value": 5, "min": 1, "max": 50}
        ]
        self.sliders = []
        self.selected_slider = None

    def render(self):
        self.surface.fill((200, 200, 200))
        font = pg.font.Font(None, 24)

        # Отрисовка всех слайдеров
        for i, param in enumerate(self.parameters):
            x, y = 10, 10 + i * 40
            param_name = font.render(param["name"], True, (0, 0, 0))
            self.surface.blit(param_name, (x, y))

            # Слайдер
            slider_x = x + 150
            slider_width = 120
            slider_height = 10
            slider_rect = pg.Rect(slider_x, y + 8, slider_width, slider_height)
            pg.draw.rect(self.surface, (240, 240, 240), slider_rect)

            # Ручка слайдера
            handle_x = slider_x + int(((param["value"] - param["min"]) / (param["max"] - param["min"])) * slider_width)
            handle_rect = pg.Rect(handle_x - 5, y + 5, 10, 16)
            pg.draw.rect(self.surface, (0, 0, 255), handle_rect)

            # Значение параметра
            value_text = font.render(f"{param['value']:.3f}" if isinstance(param['value'], float) else f"{param['value']}", True, (0, 0, 0))
            self.surface.blit(value_text, (slider_x + slider_width + 10, y))

            self.sliders.append((slider_rect, param))

    def update(self, mouse_x, mouse_y, is_dragging):
        if not is_dragging:
            self.selected_slider = None

        if self.selected_slider or is_dragging:
            for slider_rect, param in self.sliders:
                if slider_rect.collidepoint(mouse_x, mouse_y) or param == self.selected_slider:
                    self.selected_slider = param
                    slider_x = slider_rect.x
                    slider_width = slider_rect.width
                    rel_x = max(0, min(slider_width, mouse_x - slider_x))
                    param["value"] = param["min"] + (rel_x / slider_width) * (param["max"] - param["min"])

                    # Приводим к целому числу, если изначально параметр был целым
                    if isinstance(param["value"], int) or isinstance(param["min"], int):
                        param["value"] = int(param["value"])
                    break