import pygame
import random
import sys
import os
from pygame import mixer

pygame.init()
mixer.init()

# Get screen dimensions
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Constants
TOP_BAR_HEIGHT = int(SCREEN_HEIGHT * 0.1)
FOOTER_HEIGHT = int(SCREEN_HEIGHT * 0.09)
GRID_SIZE = min(SCREEN_WIDTH // 40, SCREEN_HEIGHT // 30)
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - TOP_BAR_HEIGHT - FOOTER_HEIGHT) // GRID_SIZE
INITIAL_SPEED = 10
SPEED_INCREMENT = 2
LEVEL_SCORE_THRESHOLD = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
GRADIENT_START = (30, 30, 30)
GRADIENT_END = (10, 10, 10)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Load assets
GAME_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(GAME_DIR, 'assets')

# Load sounds
try:
    EAT_SOUND = mixer.Sound(os.path.join(ASSETS_DIR, 'eat.mp3'))
    CRASH_SOUND = mixer.Sound(os.path.join(ASSETS_DIR, 'crash.mp3'))
    POWERUP_SOUND = mixer.Sound(os.path.join(ASSETS_DIR, 'powerup.mp3'))
except:
    print("Warning: Sound files not found!")

# Load images
try:
    DOUBLOON_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'doubloon.png'))
    DOUBLOON_IMG = pygame.transform.scale(DOUBLOON_IMG, (GRID_SIZE, GRID_SIZE))
except:
    print("Warning: Doubloon image not found!")

# Load custom font
try:
    FONT_PATH = os.path.join(ASSETS_DIR, 'font.otf')
    FONT = pygame.font.Font(FONT_PATH, int(SCREEN_HEIGHT * 0.06))
except:
    print("Warning: Custom font not found! Using default font.")
    FONT = pygame.font.Font(None, int(SCREEN_HEIGHT * 0.06))

class PowerUp:
    def __init__(self):
        self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 3)
        self.color = BLUE
        self.active = False
        self.type = random.choice(['speed', 'invincibility', 'double_points'])
        self.duration = 6000  # 6 seconds
        self.start_time = 0

    def randomize_position(self):
        # Spawn in the center
        self.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.active = True
        self.type = random.choice(['speed', 'invincibility', 'double_points'])

    def render(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.color,
                           (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE + TOP_BAR_HEIGHT, GRID_SIZE, GRID_SIZE))

class Obstacle:
    def __init__(self):
        self.positions = []
        self.color = LIGHT_GRAY

    def add_edge_obstacles(self):
        # Top edge
        for x in range(GRID_WIDTH):
            self.positions.append((x, 0))
        # Bottom edge
        for x in range(GRID_WIDTH):
            self.positions.append((x, GRID_HEIGHT - 1))
        # Left edge
        for y in range(GRID_HEIGHT):
            self.positions.append((0, y))
        # Right edge
        for y in range(GRID_HEIGHT):
            self.positions.append((GRID_WIDTH - 1, y))

    def add_obstacle(self):
        """Add a new obstacle at a random position."""
        new_obstacle = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        self.positions.append(new_obstacle)

    def render(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, self.color,
                           (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE + TOP_BAR_HEIGHT, GRID_SIZE, GRID_SIZE))

class Snake:
    def __init__(self, obstacle):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.speed = INITIAL_SPEED
        self.invincible = False
        self.double_points = False
        self.effects = {}
        self.obstacle = obstacle  # Add obstacle attribute

    def increase_speed(self):
        self.speed += SPEED_INCREMENT

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x), (cur[1] + y))  # Remove modulo operation

        # Check if the new position is outside the grid or collides with an obstacle
        if (new[0] < 0 or new[0] >= GRID_WIDTH or new[1] < 0 or new[1] >= GRID_HEIGHT or
            new in self.obstacle.positions) and not self.invincible:
            return False

        # Check if the new position collides with the snake's body
        if new in self.positions[3:] and not self.invincible:
            return False

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def render(self, surface):
        for i, p in enumerate(self.positions):
            color = self.color
            if i == 0:
                color = GOLD
            pygame.draw.rect(surface, color,
                           (p[0] * GRID_SIZE, p[1] * GRID_SIZE + TOP_BAR_HEIGHT, GRID_SIZE, GRID_SIZE))

    def apply_powerup(self, powerup_type):
        if powerup_type == 'speed':
            self.speed = 15
            self.effects['speed'] = pygame.time.get_ticks()
        elif powerup_type == 'invincibility':
            self.invincible = True
            self.color = GOLD
            self.effects['invincibility'] = pygame.time.get_ticks()
        elif powerup_type == 'double_points':
            self.double_points = True
            self.effects['double_points'] = pygame.time.get_ticks()

    def update_effects(self):
        current_time = pygame.time.get_ticks()
        
        if 'speed' in self.effects and current_time - self.effects['speed'] > 5000:
            self.speed = 10
            del self.effects['speed']
            
        if 'invincibility' in self.effects and current_time - self.effects['invincibility'] > 5000:
            self.invincible = False
            self.color = GREEN
            del self.effects['invincibility']
            
        if 'double_points' in self.effects and current_time - self.effects['double_points'] > 5000:
            self.double_points = False
            del self.effects['double_points']

class Food:
    def __init__(self, snake, obstacle):
        self.position = (0, 0)
        self.snake = snake
        self.obstacle = obstacle
        self.randomize_position()

    def randomize_position(self):
        while True:
            new_position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            # Ensure the new position is not on the snake or an obstacle
            if new_position not in self.snake.positions and new_position not in self.obstacle.positions:
                self.position = new_position
                break

    def render(self, surface):
        try:
            surface.blit(DOUBLOON_IMG, (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE + TOP_BAR_HEIGHT))
        except:
            pygame.draw.rect(surface, RED,
                            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE + TOP_BAR_HEIGHT, GRID_SIZE, GRID_SIZE))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('High Seas Snake Game')
        self.clock = pygame.time.Clock()
        self.font = FONT
        self.reset_game()

        # Create a semi-transparent surface for the game space (excluding top bar)
        self.game_space_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - TOP_BAR_HEIGHT), pygame.SRCALPHA)
        self.game_space_surface.set_alpha(200)  # (0 = fully transparent, 255 = fully opaque)

        # Initialize background attribute
        self.background = None
        try:
            self.background = pygame.image.load(os.path.join(ASSETS_DIR, 'background.png'))
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("Warning: Background image not found! Using gradient background.")

        # Load Game Over image
        try:
            self.game_over_image = pygame.image.load(os.path.join(ASSETS_DIR, 'game_over.png'))  # Replace with your image file
            self.game_over_image = pygame.transform.scale(self.game_over_image, (int(SCREEN_WIDTH * 0.3), int(SCREEN_HEIGHT * 0.5)))  # Resize image
        except:
            print("Warning: Game Over image not found! Using text only.")
            self.game_over_image = None

    def render_top_bar(self):
        """Render the top bar with the game name and score and level."""
        pygame.draw.rect(self.screen, WHITE, (0, 0, SCREEN_WIDTH, TOP_BAR_HEIGHT))

        game_name = self.font.render("High Seas Snake Game", True, BLACK)
        self.screen.blit(game_name, (SCREEN_WIDTH // 2 - game_name.get_width() // 2, 10))

        try:
            self.screen.blit(DOUBLOON_IMG, (10, 10))
            score_text = self.font.render(f'{self.snake.score}', True, BLACK)
            self.screen.blit(score_text, (50, 15))
        except:
            score_text = self.font.render(f'Score: {self.snake.score}', True, BLACK)
            self.screen.blit(score_text, (5, 10))

        level_text = self.font.render(f'Level: {self.level}', True, BLACK)
        self.screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))

    def render_footer(self):
        """Render the footer at the bottom of the screen."""
        pygame.draw.rect(self.screen, DARK_GRAY, (0, SCREEN_HEIGHT - FOOTER_HEIGHT, SCREEN_WIDTH, FOOTER_HEIGHT))

        footer_text = self.font.render("Use Arrow Keys to Move | P to Pause | ESC to Exit", True, WHITE)
        self.screen.blit(footer_text, (SCREEN_WIDTH // 2 - footer_text.get_width() // 2, SCREEN_HEIGHT - FOOTER_HEIGHT -5))

    def render(self):
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # Fallback to gradient background
            for y in range(SCREEN_HEIGHT):
                color = (
                    GRADIENT_START[0] + (GRADIENT_END[0] - GRADIENT_START[0]) * y // SCREEN_HEIGHT,
                    GRADIENT_START[1] + (GRADIENT_END[1] - GRADIENT_START[1]) * y // SCREEN_HEIGHT,
                    GRADIENT_START[2] + (GRADIENT_END[2] - GRADIENT_START[2]) * y // SCREEN_HEIGHT
                )
                pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

        # Render the top bar
        self.render_top_bar()

        # Render the footer
        self.render_footer()

        # Clear the game space surface
        self.game_space_surface.fill((0, 0, 0, 0))

        # Render the game grid onto the semi-transparent surface
        self.snake.render(self.game_space_surface)
        self.food.render(self.game_space_surface)
        self.powerup.render(self.game_space_surface)
        self.obstacle.render(self.game_space_surface)

        # Blit the semi-transparent surface onto the screen
        self.screen.blit(self.game_space_surface, (0, TOP_BAR_HEIGHT))

        # Draw active effects below the top bar
        effects_text = []
        if 'speed' in self.snake.effects:
            effects_text.append("SPEED :)")
        if 'invincibility' in self.snake.effects:
            effects_text.append("INVINCIBLE ^_^")
        if 'double_points' in self.snake.effects:
            effects_text.append("2X POINTS ^0^")
        
        y_offset = TOP_BAR_HEIGHT + 10
        for effect in effects_text:
            effect_surface = self.font.render(effect, True, GOLD)
            self.screen.blit(effect_surface, (10, y_offset))
            y_offset += 30

        # Draw pause text if the game is paused
        if self.paused:
            pause_text = self.font.render("PAUSED", True, BLACK)
            self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def reset_game(self):
        self.obstacle = Obstacle()
        self.obstacle.add_edge_obstacles()
        self.snake = Snake(self.obstacle)
        self.food = Food(self.snake, self.obstacle)
        self.powerup = PowerUp()
        self.game_over = False
        self.paused = False
        self.high_score = self.load_high_score() 
        self.level = 1

    def show_menu(self, text):
        """Display the game-over menu with the given text."""
        self.screen.fill(BLACK)  # Clear the screen with black

        # Render the Game Over image (if available)
        if self.game_over_image:
            image_x = SCREEN_WIDTH // 2 - self.game_over_image.get_width() // 2
            image_y = SCREEN_HEIGHT // 4 - self.game_over_image.get_height() // 2
            self.screen.blit(self.game_over_image, (image_x, image_y))

        # Render the game-over text
        title = self.font.render(text, True, WHITE)
        score = self.font.render(f"Score: {self.snake.score}", True, WHITE)
        high_score = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        press_key = self.font.render("Press SPACE to play again", True, WHITE)

        # Center the text on the screen
        text_y = SCREEN_HEIGHT // 2
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, text_y))
        self.screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, text_y + 50))
        self.screen.blit(high_score, (SCREEN_WIDTH // 2 - high_score.get_width() // 2, text_y + 100))
        self.screen.blit(press_key, (SCREEN_WIDTH // 2 - press_key.get_width() // 2, text_y + 150))

        pygame.display.flip()

    def load_high_score(self):
        """Load the high score from a file. If the file doesn't exist, return 0."""
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read())
        except FileNotFoundError:
            return 0 
        except ValueError:
            return 0 

    def save_high_score(self):
        """Save the current high score to a file."""
        with open('high_score.txt', 'w') as f:
            f.write(str(max(self.high_score, self.snake.score)))

    def update_level(self):
        # Check if the score has reached the threshold for the next level
        if self.snake.score >= self.level * LEVEL_SCORE_THRESHOLD:
            self.level += 1
            self.snake.increase_speed()  
            self.obstacle.add_obstacle() 

    def run(self):
        while True:
            if self.game_over:
                self.show_menu("GAME OVER!")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                        if event.key == pygame.K_ESCAPE:  # Exit on ESC
                            pygame.quit()
                            sys.exit()
                continue

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    if event.key == pygame.K_ESCAPE:  # Exit on ESC
                        pygame.quit()
                        sys.exit()
                    if not self.paused:
                        self.handle_input(event.key)

            if not self.paused:
                self.update()
                self.render()

            self.clock.tick(self.snake.speed)

    def handle_input(self, key):
        if key == pygame.K_UP and self.snake.direction != DOWN:
            self.snake.direction = UP
        elif key == pygame.K_DOWN and self.snake.direction != UP:
            self.snake.direction = DOWN
        elif key == pygame.K_LEFT and self.snake.direction != RIGHT:
            self.snake.direction = LEFT
        elif key == pygame.K_RIGHT and self.snake.direction != LEFT:
            self.snake.direction = RIGHT

    def update(self):
        # Update snake and check for collisions
        if not self.snake.update() and not self.snake.invincible:
            self.game_over = True
            self.save_high_score()
            try:
                CRASH_SOUND.play()
            except:
                pass
            return

        # Update power-up effects
        self.snake.update_effects()

        # Check for food collision
        if self.snake.get_head_position() == self.food.position:
            self.snake.length += 1
            points = 2 if self.snake.double_points else 1
            self.snake.score += points
            self.food.randomize_position()
            try:
                EAT_SOUND.play()
            except:
                pass

            self.update_level()

            # Spawn power-up with 20% chance
            if random.random() < 0.2:
                self.powerup.randomize_position()

        # Check for power-up collision
        if self.powerup.active and self.snake.get_head_position() == self.powerup.position:
            self.snake.apply_powerup(self.powerup.type)
            self.powerup.active = False
            try:
                POWERUP_SOUND.play()
            except:
                pass

        # Check for obstacle collision (including edge obstacles)
        if self.snake.get_head_position() in self.obstacle.positions and not self.snake.invincible:
            self.game_over = True
            self.save_high_score()
            try:
                CRASH_SOUND.play()
            except:
                pass

if __name__ == '__main__':
    game = Game()
    game.run()