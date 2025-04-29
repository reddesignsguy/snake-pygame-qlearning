""" Made by reddesignsguy (Albany Patriawan) (4/29/2025) """
class QTable:
    def __init__(self, action_space):
        self.alpha_max = 0.1
        self.alpha_min = 0.0001
        self.alpha = self.alpha_max
        self.alpha_decay = 0.9
        self.gamma = 0.95
        self.table = {}
        self.action_space = action_space
        pass

    def get_direction(self, state):
        # Initialize state in Q-table if it doesn't exist
        if state not in self.table:
            self.table[state] = {action: 0 for action in self.action_space}
        
        # Get the action with maximum Q-value
        max_q = float('-inf')
        best_action = None
        for action in self.action_space:
            q_value = self.table[state].get(action, 0)
            if q_value > max_q:
                max_q = q_value
                best_action = action
        
        # If all Q-values are equal (or state is new), choose randomly
        if best_action is None:
            return random.choice(self.action_space)
            
        return best_action

    def update(self, state, reward, action, new_state):
        # Initialize Q-table entry if it doesn't exist
        if state not in self.table:
            self.table[state] = {}
        if action not in self.table[state]:
            self.table[state][action] = 0

        # Find maximum Q-value for the next state (to be used in Bellman equation)
        max_next_q = float('-inf')
        for direction in self.action_space:
            next_q = self.table.get(new_state, {}).get(direction, 0)
            max_next_q = max(max_next_q, next_q)

        self.alpha *= self.alpha_decay
        self.alpha = max(self.alpha, self.alpha_min)

        # Update Q-value using Bellman equation
        current_q = self.table[state][action]
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        self.table[state][action] = new_q