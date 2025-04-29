# Snake Game - QLearning
<img width="358" alt="image" src="https://github.com/user-attachments/assets/6f135ba6-e1cc-43f7-ac20-f55ed854f755" />

This project is a reinforcement learning experiment where an AI agent learns to play the classic Snake game using Q-Learning.

## Installation

Make sure you have Python 3.7+ installed.

Install the required dependencies:

```bash
pip install pygame plotext numpy
```

## Usage
To run the program, go into the home directory where qlearning.py is and run:
```bash
python qlearning.py
```
or
```bash
python3 qlearning.py
```

You can go to qlearning.py and adjust the following quality of life parameters:
1. ``render_episode`` -- Visualize the snake game and learning progress in the terminal when training reaches episode: ``render_episode``
2. ``frame_rate`` -- Frame rate of snake game visualization

## State Representation

The Q-learning agent observes the environment using a compact feature set that enables fast learning:

- **Danger indicators relative to snake** (Booleans):
  - `danger_ahead`
  - `danger_left`
  - `danger_right`
- **Snake’s current direction** (4 values): `up`, `down`, `left`, `right`
- **Relative food location** (Booleans):
  - `food_ahead`
  - `food_behind`
  - `food_left`
  - `food_right`

This results in a total of 1536 **hypothetical** states (`2³ danger × 4 directions × 2⁴ food positions`). In practice, many of these states aren't reachable, e.g. the food can't be both to the left and right.

## Actions

The agent chooses from 3 discrete actions:

- Turn left
- Turn right
- Move straight

## Images:
<img width="644" alt="image" src="https://github.com/user-attachments/assets/a9f9b295-550d-47d5-a65e-ac56013042b2" />
<img width="847" alt="image" src="https://github.com/user-attachments/assets/fea807a4-6382-4959-bcd2-b2d804ff995b" />


