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

directions = ['STRAIGHT', 'LEFT', 'RIGHT']

class Model:
    def __init__(self):
        self.alpha = 0.05
        self.gamma = 0.95
        pass

    def get_direction(self, state):
        return "RIGHT"
        pass

    def update(self, old_state, reward, new_state):
        pass

model = Model()

eps = 1
eps_decay = 0.001
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("\n")
                old_state = env.get_state()
                if (random.random() < 1 - eps):
                    action = model.get_direction(old_state)
                    print("Exploiting")
                else:
                    action = random.choice(directions)
                    print("Picking randomly")

                print(f"Action taken: {action}")
                reward, new_state, terminated = env.step(action)
                print(f"Old State: {old_state}")
                print(f"Reward: {reward}")
                print(f"New State: {new_state}")
                print(f"Game Over: {terminated}")
                print(f"Current Score: {env.score}")
                
                # Update Q Table 
                if (env.game_over):
                    env.restart()

                eps -= eps_decay
                eps = max(0, eps)

# When game over, quit cleanly
game.end()