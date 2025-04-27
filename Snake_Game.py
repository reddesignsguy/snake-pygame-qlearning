"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random
from typing import Dict, Tuple

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

class SnakeGame():
    def __init__(self, get_direction=None, fr=20):
        self.frame_size_x = int(720 / 1.3)
        self.frame_size_y = int(480 / 1.3)
        self.game_window = None
        self.fps_controller = pygame.time.Clock()
        self.frame_rate = fr
        self.food_spawn = True
        self.game_over = False
        self.orientation = "RIGHT"
        self.score = 0
        self.high_score = 0
        self.steps_survived = 0
        self.highest_steps_survived = 0
        self.snake_pos = [100, 50]
        self.food_pos = [
            random.randrange(1, (self.frame_size_x // 10)) * 10,
            random.randrange(1, (self.frame_size_y // 10)) * 10
        ]
        self.snake_body = []
        self.initialize_snake_body()

    # Init game window
    def init(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
            sys.exit(-1)
        else:
            print('[+] Game successfully initialised')

        # Initialise game window
        pygame.display.set_caption('Snake Eater')
        self.game_window = pygame.display.set_mode((self.frame_size_x, self.frame_size_y))

    def step(self, action):
        if self.game_over:
            print("Game already over. Must restart environment!")
            return

        self.steps_survived += 1
    
        # Convert relative action to absolute direction
        direction = self.get_absolute_direction(action)

        # Moving the snake
        if direction == 'UP':
            self.snake_pos[1] -= 10
        if direction == 'DOWN':
            self.snake_pos[1] += 10
        if direction == 'LEFT':
            self.snake_pos[0] -= 10
        if direction == 'RIGHT':
            self.snake_pos[0] += 10

        self.orientation = direction

        # Snake body growing mechanism
        self.snake_body.insert(0, list(self.snake_pos))
        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 1
            self.food_spawn = False
        else:
            self.snake_body.pop()

        # Spawning food on the screen
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True

        # Game Over conditions
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x-10:
            self.game_over = True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y-10:
            self.game_over = True
        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                self.game_over = True
        
        self.render()

    def restart(self):
        if self.score > self.high_score:
            self.high_score = self.score
        if self.steps_survived > self.highest_steps_survived:
            self.highest_steps_survived = self.steps_survived
        self.snake_pos = [100, 50]
        self.initialize_snake_body()
        self.food_pos = [random.randrange(1, (self.frame_size_x//10)) * 10, random.randrange(1, (self.frame_size_y//10)) * 10]
        self.food_spawn = True
        self.score = 0
        self.steps_survived = 0
        self.game_over = False

    def initialize_snake_body(self):
        self.snake_body = [[100 - (i * 10), 50] for i in range(3)]
    
    def end(self):
        pygame.quit()
        sys.exit()
        return
        
    def get_absolute_direction(self, relative_action):
        """Convert relative action (STRAIGHT, LEFT, RIGHT) to absolute direction (UP, DOWN, LEFT, RIGHT)"""
        if self.orientation == 'UP':
            if relative_action == 'STRAIGHT':
                return 'UP'
            elif relative_action == 'LEFT':
                return 'LEFT'
            elif relative_action == 'RIGHT':
                return 'RIGHT'
        elif self.orientation == 'DOWN':
            if relative_action == 'STRAIGHT':
                return 'DOWN'
            elif relative_action == 'LEFT':
                return 'RIGHT'
            elif relative_action == 'RIGHT':
                return 'LEFT'
        elif self.orientation == 'LEFT':
            if relative_action == 'STRAIGHT':
                return 'LEFT'
            elif relative_action == 'LEFT':
                return 'DOWN'
            elif relative_action == 'RIGHT':
                return 'UP'
        elif self.orientation == 'RIGHT':
            if relative_action == 'STRAIGHT':
                return 'RIGHT'
            elif relative_action == 'LEFT':
                return 'UP'
            elif relative_action == 'RIGHT':
                return 'DOWN'

    def render(self):
        # Body
        self.game_window.fill(black)
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Head
        head_pos = self.snake_body[0]
        pygame.draw.rect(self.game_window, red, pygame.Rect(head_pos[0], head_pos[1], 10, 10))

        # Food
        pygame.draw.rect(self.game_window, white, pygame.Rect(self.food_pos[0], self.food_pos[1], 10, 10))

        # Score
        self.show_score(1, white, 'consolas', 20)
        self.show_high_score(1, white, 'consolas', 20)
        self.show_highest_steps_survived(1, white, 'consolas', 20)

        pygame.display.update()

    # Score
    def show_score(self, choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (self.frame_size_x/10, 15)
        else:
            score_rect.midtop = (self.frame_size_x/2, self.frame_size_y/1.25)
        self.game_window.blit(score_surface, score_rect)

    # High Score
    def show_high_score(self, choice, color, font, size):
        high_score_font = pygame.font.SysFont(font, size)
        high_score_surface = high_score_font.render('High Score : ' + str(self.high_score), True, color)
        high_score_rect = high_score_surface.get_rect()
        if choice == 1:
            high_score_rect.midtop = (self.frame_size_x/10, 35)
        else:
            high_score_rect.midtop = (self.frame_size_x/2, self.frame_size_y/1.15)
        self.game_window.blit(high_score_surface, high_score_rect)

    # Highest Steps Survived
    def show_highest_steps_survived(self, choice, color, font, size):
        steps_font = pygame.font.SysFont(font, size)
        steps_surface = steps_font.render('Highest Steps Survived : ' + str(self.highest_steps_survived), True, color)
        steps_rect = steps_surface.get_rect()
        if choice == 1:
            steps_rect.midtop = (self.frame_size_x/10, 55)
        else:
            steps_rect.midtop = (self.frame_size_x/2, self.frame_size_y/1.05)
        self.game_window.blit(steps_surface, steps_rect)

class SnakeEnvironment(SnakeGame):
    def __init__(self, frame_rate=25):
        super().__init__(fr=frame_rate)
    
    def step(self, action):
        old_score = self.score

        super().step(action)

        reward = self.get_reward(old_score)
        new_state = self.get_state()
        terminated = self.game_over
        return (reward, new_state, terminated)
    
    def get_state(self):
        # State 1: Is there danger straight / left / right?
        danger_straight = self.is_danger('STRAIGHT')
        danger_left = self.is_danger('LEFT')
        danger_right = self.is_danger('RIGHT')
        
        # State 2: Current direction (up/down/left/right)
        direction = self.orientation
        
        # State 3: Food is to the left / right / ahead / behind
        food_position = self.get_food_position()

        return {
            "danger_straight": danger_straight,
            "danger_left": danger_left,
            "danger_right": danger_right,
            "direction": direction,
            "food_position": food_position
        }
    
    def get_reward(self, old_score) -> int:
        # died
        if self.game_over:
            if self.score < 10: # strong penalty for early death
                return -10
            elif self.score < 50:
                return -5
            else:
                return -2

        # got food
        if self.score > old_score:
            return 10
        # still survived
        elif old_score == self.score:
            return 1

            
    def is_danger(self, direction):
        # Check for danger in the specified direction (STRAIGHT, LEFT, RIGHT)
        if direction == 'STRAIGHT':
            # Check straight ahead in the current direction for up to 10 blocks
            for i in range(1, 11):  # Iterate from 1 to 10 blocks ahead
                if self.orientation == 'UP':
                    new_pos = [self.snake_pos[0], self.snake_pos[1] - i * 10]  # Straight up
                elif self.orientation == 'DOWN':
                    new_pos = [self.snake_pos[0], self.snake_pos[1] + i * 10]  # Straight down
                elif self.orientation == 'LEFT':
                    new_pos = [self.snake_pos[0] - i * 10, self.snake_pos[1]]  # Straight left
                elif self.orientation == 'RIGHT':
                    new_pos = [self.snake_pos[0] + i * 10, self.snake_pos[1]]  # Straight right
                
                if self.check_collision(new_pos):  # Check if the current block is blocked
                    return True  # Danger found, return True

        elif direction == 'LEFT':
            # Check left of the snake's head for up to 10 blocks
            for i in range(1, 11):  # Iterate from 1 to 10 blocks to the left
                if self.orientation == 'UP':
                    new_pos = [self.snake_pos[0] - i * 10, self.snake_pos[1]]  # Look left
                elif self.orientation == 'DOWN':
                    new_pos = [self.snake_pos[0] + i * 10, self.snake_pos[1]]  # Look right
                elif self.orientation == 'LEFT':
                    new_pos = [self.snake_pos[0], self.snake_pos[1] + i * 10]  # Look down
                elif self.orientation == 'RIGHT':
                    new_pos = [self.snake_pos[0], self.snake_pos[1] - i * 10]  # Look up
                
                if self.check_collision(new_pos):  # Check if the current block is blocked
                    return True  # Danger found, return True

        elif direction == 'RIGHT':
            # Check right of the snake's head for up to 10 blocks
            for i in range(1, 11):  # Iterate from 1 to 10 blocks to the right
                if self.orientation == 'UP':
                    new_pos = [self.snake_pos[0] + i * 10, self.snake_pos[1]]  # Right of the head
                elif self.orientation == 'DOWN':
                    new_pos = [self.snake_pos[0] - i * 10, self.snake_pos[1]]  # Right of the head
                elif self.orientation == 'LEFT':
                    new_pos = [self.snake_pos[0], self.snake_pos[1] - i * 10]  # Right of the head
                elif self.orientation == 'RIGHT':
                    new_pos = [self.snake_pos[0], self.snake_pos[1] + i * 10]  # Right of the head
                
                if self.check_collision(new_pos):  # Check if the current block is blocked
                    return True  # Danger found, return True

        return False  # No danger found after checking

    def get_food_position(self):
        head_x, head_y = self.snake_pos  # Snake's head position
        food_x, food_y = self.food_pos   # Food's position
        
        isAhead = False
        isBehind = False
        isLeft = False
        isRight = False
        
        if self.orientation == 'UP':
            if food_y < head_y:
                isAhead = True
            elif food_y > head_y:
                isBehind = True
            elif food_x < head_x:
                isLeft = True
            elif food_x > head_x:
                isRight = True
        elif self.orientation == 'DOWN':
            if food_y > head_y:
                isAhead = True
            elif food_y < head_y:
                isBehind = True
            elif food_x > head_x:
                isLeft = True
            elif food_x < head_x:
                isRight = True
        elif self.orientation == 'LEFT':
            if food_x < head_x:
                isAhead = True
            elif food_x > head_x:
                isBehind = True
            elif food_y > head_y:
                isLeft = True
            elif food_y < head_y:
                isRight = True
        elif self.orientation == 'RIGHT':
            if food_x > head_x:
                isAhead = True
            elif food_x < head_x:
                isBehind = True
            elif food_y < head_y:
                isLeft = True
            elif food_y > head_y:
                isRight = True
        
    
        return (isAhead, isBehind, isLeft, isRight)
    
    def check_collision(self, position):
        """Check if there is a collision at the given position."""
        if position in self.snake_body or position[0] < 0 or position[1] < 0 or position[0] >= self.frame_size_x or position[1] >= self.frame_size_y:
            return True
        return False
    
    def end(self):
        super().end()
