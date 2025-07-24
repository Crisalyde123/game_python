# Space Shooter Game

A simple space shooter built with Pygame.

## Requirements
- Python 3.12+
- pygame

Install dependencies with:
```bash
pip install -r requirements.txt
# optional: confirm everything installed correctly
pip check
```

## Running the game
```bash
python main.py
```

Use left/right arrows or A/D to move the ship. Press space or click to fire. Aliens now appear in random positions and waves become tougher every 100 points. Collect the magenta life items that occasionally drift down – the longer since the last one appeared, the more likely a new one will spawn. You start with 3 lives; lose one if an alien reaches the bottom, collides with your ship, or hits you with a projectile. Game over when all lives are lost.
