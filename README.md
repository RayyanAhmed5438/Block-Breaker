# 🧱 Block Breaker

A desktop brick-breaker arcade game built with **Python** and **PyQt5**, with sound effects powered by **Pygame**.

The goal is to keep the ball in play, use the paddle to bounce it back toward the blocks, and destroy the entire block formation without letting the ball reach the bottom of the screen.

## 🎮 Gameplay

The game starts with a large grid of blocks at the top of the play area, a paddle near the bottom, and a bouncing ball.

**Destroy every block to win.** If the ball reaches the bottom of the screen, the game ends.

The game uses randomized starting positions and directions when restarted, so each new attempt can begin slightly differently.

### Controls

| Key | Action |
|-----|--------|
| **← Left Arrow** | Change paddle movement to the left |
| **→ Right Arrow** | Change paddle movement to the right |
| **R** | Restart after Game Over or Win |

The paddle continues moving in the selected direction and is constrained to the game window boundaries.

## 🧱 Block Formation

The game generates **10 rows** of blocks using an alternating layout:

- Even-numbered rows contain **19 blocks**.
- Odd-numbered rows contain **18 blocks** and are horizontally offset.
- Each block is **43 × 35 pixels**.
- Horizontal spacing is **60 pixels**.
- Vertical spacing is **6 pixels**.
- This produces **185 blocks** in a complete round.

Each block is removed after a successful ball collision.

## ⚙️ Ball Physics

The ball starts at a configurable size of **30 × 30 pixels** and moves continuously using horizontal and vertical velocity values.

The ball:

- Bounces off the left and right walls.
- Bounces off the top of the play area.
- Bounces off the paddle.
- Changes direction when it collides with a block.
- Uses collision overlap to determine whether a block collision should reverse horizontal or vertical movement.
- Starts with randomized horizontal direction when a round is restarted.
- Can also start with either upward or downward vertical movement after a restart.

## ⚡ Random Power-Ups

Every time a block is hit, the game randomly selects a power-up outcome. The three implemented power-ups are:

### 🟦 Bigger Platform

The paddle width increases by **40 pixels**.

A temporary `BIGGER PLATFORM!!` notification is displayed with a fade animation.

### 🔴 Bigger Ball

The ball size increases by **4 pixels** in both dimensions.

A temporary `BIGGER BALL!!` notification is displayed.

### ⚡ Faster Ball

The absolute horizontal and vertical ball speeds are increased by **1**, making the ball move faster.

A temporary `FASTER BALL!?` notification is displayed.

These effects are selected randomly when a block is destroyed, so not every block produces a power-up.

## 🔊 Sound Effects

A sound effect is played whenever the ball destroys a block using **Pygame's mixer**.

The game also loads a custom font for its large Win/Game Over messages.

> **Note:** The current source code expects `assets/digit.TTF` and `assets/tap.mp3` to be present when the game is launched. These asset files are not currently present in the repository tree, so they need to be supplied locally for the corresponding features to work.

## 🏆 Win & Game Over

### Win

The game stops automatically when all blocks have been destroyed and displays:

**YOU WIN**

### Game Over

If the ball reaches the bottom of the window, the game timer stops and displays:

**GAME OVER**

A `R TO RESTART` message appears below the Game Over display.

Press **R** to create a fresh block formation and start another round.

## 🖥️ Interface

The game currently uses a **1950 × 980** window with:

- Grey game background
- Green paddle with a black border
- Red ball drawn using `QPainter`
- Blue blocks with black borders
- Large Win and Game Over messages
- Temporary power-up notifications
- Fade-in/fade-out animations for power-up messages

## 🛠️ Technologies

- **Python 3**
- **PyQt5**
- **Qt Widgets**
- **QPainter** for custom ball rendering
- **QTimer** for the real-time game loop
- **QPropertyAnimation** for power-up notifications
- **Pygame Mixer** for sound effects
- **random** for block layouts, starting positions, movement directions, and power-ups

## 📁 Project Structure

```text
Block-Breaker/
│
├── BlockBreaker.py       # Complete game implementation
├── LICENSE               # MIT License
├── .gitignore
└── README.md
```

The game currently keeps its implementation in a single Python file. The `Ball` class handles custom ball rendering, while `MainWindow` contains the game interface, physics, collision detection, block management, power-ups, controls, and game state.

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/RayyanAhmed5438/Block-Breaker.git
cd Block-Breaker
```

### 2. Install dependencies

```bash
pip install PyQt5 pygame
```

### 3. Add required assets

Create an `assets` folder in the project root and provide:

```text
assets/
├── digit.TTF
└── tap.mp3
```

The font is used for the large Win/Game Over text and the MP3 is used for block-hit sound effects.

### 4. Run the game

```bash
python BlockBreaker.py
```

## 🔄 Game Loop

The game uses a `QTimer` running at approximately **18 ms per update**. Each update handles three main tasks:

1. **Ball movement** — updates the ball position and wall/paddle interactions.
2. **Collision detection** — checks the ball against the blocks and determines bounce direction.
3. **Paddle movement** — moves the paddle according to the current direction while keeping it inside the window.

This keeps the game running as a simple real-time event loop without requiring a separate game engine.

## 🧩 Project Design

### `Ball`

A custom `QLabel` subclass that uses `QPainter` and antialiasing to draw the red circular ball.

### `MainWindow`

Contains the complete game state and gameplay systems, including:

- Paddle
- Ball physics
- Block generation
- Collision detection
- Power-ups
- Game loop
- Restart logic
- Win/Game Over states
- Sound playback
- UI animations

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for the complete license text.

## 👤 Author

**Rayyan Ahmed**
