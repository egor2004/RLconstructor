import gymnasium as gym
import numpy as np
import random
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque

# Гиперпараметры
EPISODES = 1000       # Количество эпизодов для обучения
LEARNING_RATE = 0.001 # Скорость обучения
GAMMA = 0.99          # Коэффициент дисконтирования
EPSILON = 1.0         # Начальное значение для epsilon (epsilon-greedy)
EPSILON_DECAY = 0.995 # Скорость уменьшения epsilon
EPSILON_MIN = 0.01    # Минимальное значение epsilon
MEMORY_SIZE = 2000    # Размер памяти для хранения опыта
BATCH_SIZE = 32       # Размер батча для обучения

# Создание среды
# env = gym.make("FrozenLake-v1", is_slippery=False)  # Задаем среду без скольжения для большей детерминированности

# Модель DQN
class DQN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Агент DQN
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=MEMORY_SIZE)
        self.epsilon = EPSILON
        self.model = DQN(state_size, action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)
        self.criterion = nn.MSELoss()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        state = torch.FloatTensor(state).unsqueeze(0)
        with torch.no_grad():
            q_values = self.model(state)
        return torch.argmax(q_values).item()

    def replay(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = random.sample(self.memory, BATCH_SIZE)
        for state, action, reward, next_state, done in batch:
            state = torch.FloatTensor(state).unsqueeze(0)
            next_state = torch.FloatTensor(next_state).unsqueeze(0)
            target = reward
            if not done:
                target = reward + GAMMA * torch.max(self.model(next_state)).item()
            target_f = self.model(state)
            target_f[0][action] = target
            self.optimizer.zero_grad()
            loss = self.criterion(target_f, self.model(state))
            loss.backward()
            self.optimizer.step()
        if self.epsilon > EPSILON_MIN:
            self.epsilon *= EPSILON_DECAY

# # Инициализация агента
# state_size = env.observation_space.n
# action_size = env.action_space.n
# agent = DQNAgent(state_size, action_size)
#
# # Обучение агента
#
# MAX_STEPS = 20
#
# for e in range(EPISODES):
#     if e % 10 == 0:
#         env = gym.make("FrozenLake-v1", is_slippery=False, render_mode='human')
#     else:
#         env = gym.make("FrozenLake-v1", is_slippery=False)
#     state, _ = env.reset()
#     state = np.identity(state_size)[state]  # One-hot кодировка для состояния
#     total_reward = 0
#     done = False
#     steps = 0
#     while not done:
#         action = agent.act(state)
#         next_state, reward, done, _, _ = env.step(action)
#         next_state = np.identity(state_size)[next_state]  # One-hot кодировка для состояния
#         agent.remember(state, action, reward, next_state, done)
#         state = next_state
#         total_reward += reward
#         agent.replay()
#
#         steps += 1
#         if steps > MAX_STEPS:
#             done = True
#             steps = 0
#
#     print(f"Episode: {e + 1}/{EPISODES}, Total reward: {total_reward}, Epsilon: {agent.epsilon:.2f}")
#
# env.close()
