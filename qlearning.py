# Init values: learning rate, discount rate, epsilon greedy
# Define states and actions
# Create QTable of state-action pairs
# Create reward function
alpha = 0.05
gamma = 0.95
epsilon = 1

# Create agent
# Improve QTable by running agent in the game
from Snake_Game import SnakeGame
import pygame, sys, random

game = SnakeGame()
game.init()

directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    action = random.choice(directions)
    reward, old_state, new_state, terminated = game.step(action)

    # Update Q Table 

    if (game.game_over):
        game.restart()

# When game over, quit cleanly
game.end()