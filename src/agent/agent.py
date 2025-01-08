import torch
from torch import nn
from torch import optim
from collections import deque
import random

# Параметры обучения
NUM_EPISODES = 20
BATCH_SIZE = 32
GAMMA = 0.99
EPSILON_START = 1.0
EPSILON_MIN = 0.1
EPSILON_DECAY = 0.995
LEARNING_RATE = 0.001
TARGET_UPDATE = 5

class DQN(nn.Module):
    def __init__(self, grid_size, num_actions):
        super(DQN, self).__init__()
        self.grid_size = grid_size
        self.fc1 = nn.Linear(grid_size * grid_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, num_actions)

    def forward(self, grid):
        grid_tensor = torch.tensor(grid, dtype=torch.int64)
        x = nn.functional.one_hot(grid_tensor, self.grid_size**2).float()
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class Agent:
    def __init__(self, input_din, output_din):
        self.model = DQN(input_din, output_din)
        self.target_model = DQN(input_din, output_din)
        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model.eval()
        self.memory = deque(maxlen=10000)
        self.optimizer = optim.Adam(self.model.parameters(), lr=LEARNING_RATE)
        self.epsilon = EPSILON_START

    def act(self, state):
        if random.random() < self.epsilon:
            return random.choice(range(4))
        else:
            with torch.no_grad():
                return torch.argmax(self.model(state)).item()

    def remember(self,state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self):
        if len(self.memory) < BATCH_SIZE:
            return

        batch = random.sample(self.memory, BATCH_SIZE)
        for state, action, reward, next_state, done in batch:
            q_values = self.model(state)
            next_q_values = self.target_model(next_state)

            target = q_values.clone()
            target[action] = reward + (1 - done) * GAMMA * torch.max(next_q_values)

            loss = nn.MSELoss()(q_values, target)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def update_target(self):
        self.target_model.load_state_dict(self.model.state_dict())

