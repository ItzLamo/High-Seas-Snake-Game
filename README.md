
# High Seas Snake Game

Welcome to **High Seas Snake Game**, a modern take on the classic Snake game with exciting features, power-ups, and a nautical twist!

---

## Features

- **Dynamic Gameplay:** Navigate a grid-based arena while collecting food and avoiding obstacles.
- **Power-Ups:** Unlock special abilities like speed boosts, invincibility, and double points.
- **Obstacle Challenge:** Edges and randomly spawning obstacles make the game more thrilling.
- **Adaptive Speed:** The game increases in difficulty as you progress.
- **Custom Assets:** Unique sound effects, background images, and themed items.
- **Scoring System:** Track your score and strive for a new high score!

---

## Installation and Requirements

### Prerequisites

- Python 3.6 or higher
- `pygame` library installed (`pip install pygame`)

### Setup

1. Clone or download the repository to your local machine.
2. Ensure the following directories exist:
   - `assets/` for game assets:
     - `background.png` (background image)
     - `doubloon.png` (food image)
     - `font.otf` (custom font)
     - `eat.mp3`, `crash.mp3`, `powerup.mp3` (sound effects)
3. Place the asset files in the correct directories.
4. Run the game.
---

## Controls

- **Arrow Keys:** Move the snake (Up, Down, Left, Right)
- **P:** Pause/Resume the game
- **Esc:** Exit the game

---

## How to Play

1. **Objective:** Control the snake to collect food, grow in size, and score points.
2. **Power-Ups:** Pick up power-ups for special effects, but beware of their time limits!
3. **Avoid Obstacles:** Stay away from the edges and other obstacles in the arena.
4. **Level Up:** Each level increases the speed and adds more challenges.

---

## Game Mechanics

- **Grid System:** The play area adapts to your screen size for an optimal experience.
- **Power-Up Effects:**
  - **Speed:** Increases movement speed temporarily.
  - **Invincibility:** Makes you immune to collisions for a short duration.
  - **Double Points:** Doubles the score earned while active.
- **Scoring:** Earn points by collecting food. Bonus points are awarded with power-ups.
- **Game Over:** Collide with yourself or obstacles, and the game ends.

---

## Customization

Modify constants in the code for personalized gameplay:
- **Grid Size, Colors, Speed, etc.**
- Replace assets in the `assets/` folder for a custom theme.

---

## Troubleshooting

- **Sound/Image Not Found:** Ensure all asset files are correctly placed in the `assets/` folder.
- **Performance Issues:** Try lowering the screen resolution or grid size.

