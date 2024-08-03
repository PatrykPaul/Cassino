# Casino Game Project

## Overview

The Casino Game Project is a suite of interactive applications that introduce the player to various casino games. The main menu allows the player to choose between blackjack and roulette. The game also manages sound and displays player money information.

## Start Menu
![main](https://github.com/user-attachments/assets/290e539c-afd6-4ea3-9585-dac4c334484e)

The start menu is the user interface that lets the player select one of two casino games: blackjack or roulette. The main screen includes the game logo, a button to start the roulette game, a sound management button, and an exit button. The game also displays the player's current money balance and allows for displaying information about blackjack rules.

### Classes and Functions

- **MoneyDisplay**: Manages the display and update of the player's money information.
- **BeltImage**: Handles the display of the money belt image.
- **MoneyBeltDisplay**: Combines `MoneyDisplay` and `BeltImage` functionality to display money and the belt image.
- **ExitAndRunButton**: A button class for exiting the game and launching another application.
- **BlackjackQuestionButton**: A question button class for displaying blackjack rules.
- **run_roulette**: A function to launch the roulette application.

## Blackjack

**Blackjack** is a popular card game where the goal is to get as close to 21 points as possible without going over. The player aims to have a better hand than the dealer without exceeding 21 points.

In the Blackjack application:

- **Player**: Represents the player, managing their movements and interactions with the game.
- **MoneyDisplay**: Manages the display of money and updating the player's account balance.

## Roulette

**Roulette** is a casino game where players place bets on numbers, colors, or groups of numbers. The roulette wheel is spun, and a ball lands on one of the numbers. Winning depends on whether the result of the spin matches the player's bet.

In the Roulette application:

- **Player**: Represents the player, managing their movements and interactions with the game.
- **MoneyDisplay**: Manages the display of money and updating the player's account balance.

## Player Movement

The player moves around the board using the arrow keys (up, down, left, right). The player's movement is confined to the screen area. The player can interact with various objects on the board, such as game tables, and enter areas that activate buttons to start other applications.

### Classes and Functions

- **Player**: Manages the player's position and movement.
- **ImageButton**: Handles buttons on the screen, such as the button to start roulette or the exit button.

## Running the Game

To start the game, simply run the `main.py` file. The start menu will allow you to choose between blackjack and roulette, manage sound, and display money information.



