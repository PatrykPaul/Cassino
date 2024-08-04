# Casino Game Project

## Overview

The Casino Game Project is a suite of interactive applications that introduce the player to various casino games. The main menu allows the player to choose between blackjack and roulette. The game also manages sound and displays player money information.

## Start Menu
![mm](https://github.com/user-attachments/assets/c7a6c14d-99e7-48e4-9972-13bd19390af0)

The start menu is the user interface that lets the player select one of two casino games: blackjack or roulette. The main screen includes the game logo, a button to start the roulette game, a sound management button, and an exit button. The game also displays the player's current money balance and allows for displaying information about blackjack rules.

### Classes and Functions

- **MoneyDisplay**: Manages the display and update of the player's money information.
- **BeltImage**: Handles the display of the money belt image.
- **MoneyBeltDisplay**: Combines MoneyDisplay and BeltImage functionality to display money and the belt image.
- **ExitAndRunButton**: A button class for exiting the game and launching another application.
- **BlackjackQuestionButton**: A question button class for displaying blackjack rules.
- **run_roulette**: A function to launch the roulette application.
  
## Player Movement

The player moves around the board using the arrow keys (up, down, left, right). The player's movement is confined to the screen area. The player can interact with various objects on the board, such as game tables, and enter areas that activate buttons to start other applications.

![bj](https://github.com/user-attachments/assets/7cd090c5-1c0b-4a83-9916-0443a7172cc6)

## Blackjack
**Blackjack** is a popular card game where the goal is to get as close to 21 points as possible without going over. The player aims to have a better hand than the dealer without exceeding 21 points.

![bjg](https://github.com/user-attachments/assets/17e89015-70eb-4ccc-be4e-05c3c7c0ce55)



In the Blackjack application:

- **class_question.py**: Contains the QuestionButton class for the on-screen instructions.
- **class_money_display.py**: Contains the MoneyDisplay and BeltImage classes for managing and displaying the player's money.
- **class_button_exit.py**: Contains the Exit_Button class for the exit button functionality.
- **class_fireworks_bj.py**: Script to run for the fireworks animation when the player wins.
- **audio_files/putting_cards.mp3**: Sound effect for card dealing.
- **cards/**: Directory containing card images.
- **buttons/**: Directory containing button images.
- **rooms/**: Directory containing background images.
- **money.txt**: File to store the player's current money.
- **final_bet.txt**: File to store the player's final bet.

## Roulette

**Roulette** is a casino game where players place bets on numbers, colors, or groups of numbers. The roulette wheel is spun, and a ball lands on one of the numbers. Winning depends on whether the result of the spin matches the player's bet.

![rg](https://github.com/user-attachments/assets/6635a1e1-10a2-408e-92bd-a28e7527d67d)

In the Roulette application:
- **class_money_display.py**: Contains the MoneyDisplay class for managing and displaying the player's money.
- **class_belt_image.py**: Contains the BeltImage class for displaying the money belt image.
- **class_bet_buttons.py**: Contains the BetButtons class for managing bet buttons and current bets.
- **utils.py**: Contains utility functions like load_scaled_image, rotate_image, and play_button_press_sound.
- **draw_bets.py**: Contains the draw_bets function for rendering the current bets on the screen.
- **class_exit_button.py**: Contains the ExitButton class for handling the exit button functionality.
- **main.py**: Main script for running the roulette game, handling events, and managing game state.



