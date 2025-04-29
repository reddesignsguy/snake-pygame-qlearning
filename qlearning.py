""" Made by reddesignsguy (Albany Patriawan) (4/29/2025) """

from Snake_Game import SnakeEnvironment
from pynput import keyboard
from qtable import QTable
import pygame, sys, random
import plotext as plt
import numpy as np

# Quality of Life params
render_episode = 1000 # Visualizes the snake game at this episode
frame_rate = 100

# Model Params
eps = 1
eps_decay = 0.999
min_eps = 0.01
steps = 0
episode = 0
mean_score = 0

# Store episode scores and epsilon values
episode_scores = []
episode_epsilons = []

env = SnakeEnvironment(frame_rate=frame_rate)
model = QTable(env.action_space)
steps_without_food = 0
cur_score = env.score

while True:
    env.injected_text = f"Episode: {episode}"

    # Press space bar to end
    if env.game_window:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    env.end()
                    pass

    old_state = env.get_state()

    # Perform action
    action = None
    if (random.random() < 1 - eps):
        action = model.get_direction(old_state)
    else:
        action = random.choice(env.action_space)
    reward, new_state, terminated = env.step(action)
    
    # Update Q Table 
    steps+=1
    model.update(old_state, reward, action, new_state)
        
    # End episode if no progress made
    steps_without_food += 1
    if cur_score != env.score:
        cur_score = env.score
        steps_without_food = 0
    if steps_without_food == 1000:
        print("Snake failed to get food in < 1000 steps. Restarting...")
        env.restart()
        continue

    if (env.game_over):
        # Update counters
        steps_without_food = 0
        cur_score = 0
        episode_scores.append(env.score)
        episode_epsilons.append(eps)
        episode += 1
        steps = 0
        eps *= eps_decay
        eps = max(eps, min_eps)

        # Print results occasionally
        if episode % 50 == 0:
            print(f"--------\n Episode {episode}: \n Mean {sum(episode_scores) / episode} \n High {env.high_score}")

        # Show snake game and plot
        if episode == render_episode:
            env.open_game_window()

            plt.clear_figure()
            plt.plot(episode_scores, label="Score per Episode")
            
            # Visualize moving average
            window_size = 100
            if len(episode_scores) >= window_size:
                moving_avg = np.convolve(episode_scores, np.ones(window_size)/window_size, mode='valid')
                plt.plot(range(window_size-1, len(episode_scores)), moving_avg, 
                        label=f"{window_size}-episode Moving Average")
        
            plt.title("Snake Game Performance")
            plt.xlabel("Episode")
            plt.ylabel("Score / Epsilon")
            plt.show()
        
        env.restart()
