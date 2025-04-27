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

action_space = ['STRAIGHT', 'LEFT', 'RIGHT']
manual_mode = False  # Set to False for automatic execution

class QTable:
    def __init__(self):
        self.alpha_max = 0.1
        self.alpha_min = 0.0001
        self.alpha = self.alpha_max
        self.alpha_decay = 0.99995
        self.gamma = 0.99
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

        # Calculate alpha based on percent_convergence
        # When percent_convergence is 0, alpha = alpha_max
        # When percent_convergence is 100, alpha = alpha_min
        convergence_factor = percent_convergence / 100.0
        self.alpha = self.alpha_max - (self.alpha_max - self.alpha_min) * convergence_factor
        self.alpha = max(self.alpha_min, min(self.alpha_max, self.alpha))

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

model = QTable()

eps = 1
eps_decay = 0.99
steps = 0
episode = 0
episode_length = 1000
final_episode_length = 10000
eps_threshold = 0.1  # When epsilon falls below this, increase episode length

# Frame rate control
clock = pygame.time.Clock()
FPS = 5000  # Frames per second

while True:
    # Control frame rate
    # clock.tick(FPS)
    # pygame.time.wait(1)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

    print("\n")
    old_state = env.get_state()
    action = None
    if (random.random() < 1 - eps):
        action = model.get_direction(old_state)
    else:
        action = random.choice(action_space)

    reward, new_state, terminated = env.step(action)
    
    # Calculate percent_convergence based on epsilon
    # When epsilon is 1.0, percent_convergence is 0
    # When epsilon is eps_threshold (0.1) or less, percent_convergence is 100
    # Linear interpolation between these points
    if eps >= 1.0:
        percent_convergence = 0
    elif eps <= eps_threshold:
        percent_convergence = 100
    else:
        # Map epsilon from [eps_threshold, 1.0] to [100, 0]
        percent_convergence = 100 * (1.0 - (eps - eps_threshold) / (1.0 - eps_threshold))
    
    # Update Q Table 
    steps+=1
    model.update(old_state, reward, action, new_state, percent_convergence)

    print(f"Episode: {episode}")
    print(f"Step: {steps}")
    print(f"Action taken: {action}")
    print(f"Old State: {old_state}")
    print(f"Reward: {reward}")
    print(f"New State: {new_state}")
    print(f"Game Over: {terminated}")
    print(f"Current Score: {env.score}")
    print(f"Q Table size: {len(model.table)}")
    print(f"Epsilon: {eps}")
    print(f"Alpha: {model.alpha}")

    if (env.game_over or steps >= episode_length):
        episode += 1
        steps = 0
        eps *= eps_decay
        
        # Increase episode length when epsilon falls below threshold
        if eps < eps_threshold and episode_length < final_episode_length:
            episode_length = final_episode_length
            print(f"\nIncreasing episode length to {final_episode_length}!")
            
        env.restart()

# When game over, quit cleanly
game.end()