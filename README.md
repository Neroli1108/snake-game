# Snake Game - Multi-Mode Python Game

A feature-rich Snake game implementation using Python and Pygame with multiple game modes and bilingual support.

## 🎮 Game Features

### Multiple Game Modes

- **Single Player (AI)**: Watch AI play the classic Snake game
- **Single Player (Manual)**: Play the classic Snake game yourself
- **Dual Mode**: AI vs Human split-screen competition
- **Battle Royale**: 25 snakes fight in a shrinking arena (1 human + 24 AI)

### Language Support

- **Bilingual Interface**: English and Chinese (中文) support
- **Dynamic Font Loading**: Automatically loads appropriate fonts for each language
- **Click-to-Switch**: Easy language switching via flag icon

### Advanced Features

- **Dynamic Speed System**: Snake speed decreases as length increases (Battle Royale mode)
- **Shrinking Arena**: Safe zone shrinks every minute in Battle Royale
- **Smart AI**: Pathfinding AI that avoids obstacles and finds food
- **Collision System**: Larger snakes can eat smaller ones
- **Real-time Statistics**: Score, length, survival time tracking

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/neroli1108/snake-game.git
cd snake-game
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python src/main.py
```

## 🎯 How to Play

### Controls

- **Arrow Keys** or **WASD**: Move snake (Manual mode)
- **Mouse Click**: Click flag to switch language
- **Number Keys 1-4**: Select game mode
- **R**: Restart game (when game over)
- **Q/ESC**: Quit game or return to menu

### Game Modes

#### Single Player Mode

- Control your snake to eat food and grow
- Avoid walls and your own tail
- Try to achieve the highest score

#### Dual Mode

- Split screen: AI (left) vs Human (right)
- First to die loses
- Compare scores and survival time

#### Battle Royale Mode

- 25 snakes compete in a survival arena
- You control the cyan snake with white outline
- Larger snakes can eat smaller ones
- Safe zone shrinks every 60 seconds
- Last snake standing wins!

### Battle Royale Special Rules

- **Speed System**: Longer snakes move slower (Speed 5-25)
- **Eating Mechanics**: Big snakes eat small snakes on contact
- **Shrinking Zone**: Red areas are dangerous, stay in white-bordered safe zone
- **Elimination**: Game ends immediately if human player dies

## 🏗️ Project Structure

```
snake-game/
├── src/
│   ├── main.py              # Main game entry point and menu
│   ├── game.py              # Single player game logic
│   ├── dual_game.py         # Dual mode game logic
│   ├── battle_royale.py     # Battle royale game logic
│   ├── snake.py             # Snake class implementation
│   └── ai_controller.py     # AI pathfinding logic
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── .gitignore             # Git ignore file
```

## 🤖 AI Implementation

The AI uses a simple but effective pathfinding algorithm:

- **Target Priority**: Food > Safe movement > Avoid obstacles
- **Pathfinding**: Direct path calculation with obstacle avoidance
- **Boundary Awareness**: Respects game boundaries and safe zones
- **Collision Avoidance**: Prevents self-collision and wall collision

## 🎨 Graphics and UI

- **Minimal Design**: Clean, retro-style graphics
- **Color Coding**: Different colors for different snakes and elements
- **Real-time Info**: Live statistics and game state display
- **Responsive Layout**: Adapts to different screen sizes
- **Visual Feedback**: Clear indication of game states and events

## 🌐 Internationalization

- **Font System**: Automatic Chinese font detection and loading
- **Fallback Fonts**: Graceful degradation if fonts not available
- **Cultural Elements**: Appropriate flag representations
- **Complete Translation**: All UI elements translated

## 🔧 Technical Details

### Dependencies

- **pygame**: Game engine and graphics
- **random**: Random number generation
- **sys**: System operations
- **os**: File system operations
- **math**: Mathematical calculations

### Performance

- **60 FPS**: Smooth gameplay with 60 FPS for battle royale
- **Scalable**: Handles 25 simultaneous snake entities
- **Memory Efficient**: Minimal memory footprint
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🐛 Known Issues

- Chinese font loading may fail on non-Windows systems
- Large battle royale games might slow down on older hardware
- AI pathfinding could be improved for complex scenarios

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and Pygame
- Inspired by classic Snake games
- Battle Royale concept adapted for Snake gameplay
- Bilingual support for international accessibility

## 📊 Game Statistics

- **4 Game Modes**: Single AI, Single Manual, Dual, Battle Royale
- **2 Languages**: English and Chinese
- **25 Snakes**: Maximum simultaneous snakes in Battle Royale
- **Dynamic Speed**: 5-25 speed range based on snake length
- **60 Second Cycles**: Arena shrinking interval

---

**Enjoy the game and happy coding!** 🐍🎮
