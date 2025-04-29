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
import plotext as plt
import numpy as np

env = SnakeEnvironment()
env.init()
env.isRendering = False

action_space = ['STRAIGHT', 'LEFT', 'RIGHT']
manual_mode = False  # Set to False for automatic execution

# Store episode scores and epsilon values
episode_scores = []
episode_epsilons = []

eps = 1
eps_decay = 0.999
min_eps = 0.01
steps = 0
episode = 0
mean_score = 0
eps_threshold = 0.1  # When epsilon falls below this, increase episode length

render_episode = 10000
# Frame rate control
clock = pygame.time.Clock()
FPS = 5000  # Frames per second


class QTable:
    def __init__(self):
        self.alpha_max = 0.1
        self.alpha_min = 0.0001
        self.alpha = self.alpha_max
        self.alpha_decay = 0.9
        self.gamma = 0.95
        self.table = {}
        pass

    def get_direction(self, state):
        # Convert state to key if it's a dictionary
        state_key = self.state_to_key(state) if isinstance(state, dict) else state
        
        # Initialize state in Q-table if it doesn't exist
        if state_key not in self.table:
            self.table[state_key] = {action: 0 for action in action_space}
        
        # Get the action with maximum Q-value
        max_q = float('-inf')
        best_action = None
        for action in action_space:
            q_value = self.table[state_key].get(action, 0)
            if q_value > max_q:
                max_q = q_value
                best_action = action
        
        # If all Q-values are equal (or state is new), choose randomly
        if best_action is None:
            return random.choice(action_space)
            
        return best_action

    def update(self, old_state, reward, action, new_state, percent_convergence = 100):
        # Convert states to keys if they're dictionaries
        old_state_key = self.state_to_key(old_state) if isinstance(old_state, dict) else old_state
        new_state_key = self.state_to_key(new_state) if isinstance(new_state, dict) else new_state
        
        # Initialize Q-table entry if it doesn't exist
        if old_state_key not in self.table:
            self.table[old_state_key] = {}
        if action not in self.table[old_state_key]:
            self.table[old_state_key][action] = 0

        # Find maximum Q-value for the next state
        max_next_q = float('-inf')
        for direction in action_space:
            next_q = self.table.get(new_state_key, {}).get(direction, 0)
            max_next_q = max(max_next_q, next_q)

        self.alpha *= self.alpha_decay
        self.alpha = max(self.alpha, self.alpha_min)

        # Update Q-value using Bellman equation
        current_q = self.table[old_state_key][action]
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.table[old_state_key][action] = new_q

    def state_to_key(self, state):
        """Convert state dictionary to a hashable tuple with consistent ordering"""
        # Sort keys to ensure consistent ordering
        sorted_keys = sorted(state.keys())
        # Create tuple of values in consistent order
        return tuple(state[key] for key in sorted_keys)

def visualize():
    # Visualize snake
    if episode == render_episode:
        env.isRendering = True
        # Create terminal plot
        plt.clear_figure()
        
        # Plot scores and epsilon on the same graph
        plt.plot(episode_scores, label="Score per Episode")
        
        # Add moving average for scores
        window_size = 100
        if len(episode_scores) >= window_size:
            moving_avg = np.convolve(episode_scores, np.ones(window_size)/window_size, mode='valid')
            plt.plot(range(window_size-1, len(episode_scores)), moving_avg, 
                    label=f"{window_size}-episode Moving Average")
    
        
        plt.title("Snake Game Performance")
        plt.xlabel("Episode")
        plt.ylabel("Score / Epsilon")
        plt.show()

model = QTable()

steps_without_food = 0
cur_score = env.score
while True:
    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    # Important metrics
    old_state = env.get_state()

    # Perform action
    action = None
    if (random.random() < 1 - eps):
        action = model.get_direction(old_state)
    else:
        action = random.choice(action_space)

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
        
        visualize()
        env.restart()


# When game over, quit cleanly
game.end()
