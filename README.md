# Space Warship Combat Game

## Project Overview

**Space Warship Combat** is an immersive 2D action game built using Python and Pygame. Players control a space warship and navigate through challenging levels, engaging in battles against a variety of enemies while collecting power-ups. The project aims to provide a dynamic and interactive space adventure that challenges players' strategic thinking and reflexes.

## Features

- **Player Controls**: Control your warship with intuitive movement, shooting bombs, and power-up collection.
- **Enemy AI**: Enemies spawn at different levels, with increasing difficulty, challenging players at every step.
- **Level Progression**: Complete levels to unlock progressively challenging environments.
- **Power-Ups**: Collect power-ups to enhance your warship's capabilities during gameplay.
- **Scoring System**: Destroy enemies to accumulate score, with points displayed during gameplay.
- **Pause and Resume**: Pause the game and navigate through resume or restart options.

## System Requirements

- **Python Version**: Python 3.7+
- **Pygame**: Pygame library version 2.0 or higher
- **Operating System**: Platform-independent (Windows, macOS, Linux)

## Installation and Setup

1. **Environment**: Install Python (version 3.7 or later) and use an IDE like PyCharm or Visual Studio Code to write and debug the code.
2. **Libraries**: Ensure Pygame is installed and functional. You can install it using the following command:
   ```sh
   pip install pygame
   ```
3. **Code and Assets**: Place the project code and all graphical and audio assets in the same working directory for easy access.
4. **Run**: Execute the main Python script to launch the game.
   ```sh
   python main.py
   ```
5. **Test**: Verify game functionalities, including level progression, control responsiveness, collision detection, and overall gameplay.

## Project Structure

- **main.py**: The entry point to start the game.
- **player.py**: Defines the player's warship and its behaviors.
- **enemy.py**: Manages enemy behaviors, spawning, and interactions.
- **level.py**: Handles the design of each level and controls the progression.
- **utils.py**: Contains helper functions like collision detection and asset loading.

## Game Design

The game follows a modular architecture, encapsulating components like player, enemy, and level classes to maintain clean, reusable code. Levels progressively increase in difficulty, and players are challenged to defeat enemies and advance to higher levels. The user interface provides information on health, score, and power-ups collected.

## Testing and Validation

**Unit Testing** and **System Testing** were conducted to ensure the functionality of individual components and the entire application.

- **Unit Testing**: Verified player controls, navigation, enemy behaviors, and collision detection.
- **System Testing**: Validated the game's cohesive functioning, including gameplay, level progression, performance, and UI responsiveness.

## Limitations

1. **Limited Level Variety**: Few levels available, which may affect replayability.
2. **Basic Enemy AI**: Simple behavior patterns, lacking sophisticated decision-making.
3. **No Multiplayer Support**: Currently only single-player mode is implemented.
4. **Basic UI Design**: Minimalistic user interface with potential for improvement.

## Future Enhancements

- **Multiplayer Mode**: Implement cooperative or competitive multiplayer gameplay.
- **Enhanced Enemy AI**: Develop more advanced enemy behaviors for dynamic encounters.
- **Additional Levels**: Add more levels with varied challenges and environments.
- **Upgrades and Power-ups**: Introduce more power-ups and an upgrade system for enhanced player progression.

## References

1. Python Software Foundation. (n.d.). [Python documentation](https://docs.python.org/).
2. Pygame. (n.d.). [Pygame documentation](https://www.pygame.org/docs/).
3. Python Official Documentation for Pygame Integration. Python Software Foundation. (n.d.). [Retrieved from](https://docs.python.org/3/library/pygame.html).
4. Pygame Community Tutorials. (n.d.). [Game development with Pygame](https://pygame-community-tutorials.com).
5. Sweigart, A. (2012). *Make Games with Python and Pygame*. No Starch Press.
6. Real Python. (n.d.). [Developing games with Pygame](https://realpython.com/pygame-a-primer/).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
