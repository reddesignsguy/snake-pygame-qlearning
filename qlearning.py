# Init values: learning rate, discount rate, epsilon greedy
# Define states and actions
# Create QTable of state-action pairs
# Create reward function
alpha = 0.05
gamma = 0.95
epsilon = 1

# Create agent
# Improve QTable by running agent in the game
from Snake_Game import SnakeEnvironment
import pygame, sys, random

env = SnakeEnvironment()
env.init()

directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

class Model:
    def __init__(self):
        self.alpha = 0.05
        self.gamma = 0.95
        pass

    def get_direction():
        pass

    def update(old_state, reward, new_state):
        pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    action = random.choice(directions)
    reward, old_state, new_state, terminated = env.step(action)

    # Update Q Table 
    if (env.game_over):
        env.restart()

# When game over, quit cleanly
game.end()