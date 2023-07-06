# Scrabble Blitz

#### Play Now: http://devinpadron.pythonanywhere.com/

#### Video Demo: https://www.youtube.com/watch?v=4xN2doP4wTk

## Description:
Scrabble-Blitz is a web-based board game inspired by Scrabble. It challenges players to create words under a time limit using a set of randomly assigned tiles.

Unlike the original Scrabble, Scrabble Blitz is played on your own, without an opponent. A random word will be loaded onto the center of the board, and your task will be to build off of it and score as many points as possible before time runs out.

## Gameplay

1. When the game starts, a single word is loaded onto the game board, and the player receives a tray of letter tiles.
2. The player attempts to make words on the game board using the tiles in their tray.
3. Points are awarded based on the value of the tiles used and the use of bonus squares. The value of the points also gets added to the timer in seconds. So if a word is worth 10 points you get 10 seconds added to the clock.
4. A timer counts down, and the game ends when time runs out.
5. The goal is to get as many points as possible before the timer runs out.


### Special Features

* `Shuffle`: If you're stuck and need new inspiration, you can shuffle the tiles in your tray to get a fresh perspective.

* `Discard`: If you're feeling stuck and want to change the tiles in your hand, you can choose to exchange them with new ones from the tile pool. This allows you to refresh your options and potentially find better combinations. Use this strategic move wisely to improve your chances of scoring big! Keep in mind you can only exchange tiles twice in a single game, so use your exchanges wisely.

* `High Score`: Keep track of your best game and challenge yourself to beat your highest score!


## Development

* `Python (Flask)`: The backend of Scrabble-Blitz is powered by Python using the Flask framework. Flask was chosen for its simplicity, flexibility, and fine-grained control over configurations. Flask routes were created to handle HTTP requests and return appropriate responses, allowing for communication between the frontend and the backend. Logic for game mechanics such as tile distribution, score calculation, and word validation was implemented in Python.

* `JavaScript`: On the client-side, JavaScript was extensively used to provide dynamic and responsive gameplay. Fetch API was utilized for asynchronous communication with the server, enabling real-time updates to the game state without requiring a page reload. DOM manipulation was used to handle the game board, allowing users to drag and drop tiles.

* `HTML/CSS`: HTML was used for structuring the web content, while CSS was employed for styling and animations to improve the user interface and experience. CSS Grid was used to layout the game board, and CSS transitions were leveraged to provide smooth visual feedback to users.

* `Git and GitHub`: Git was used for version control, allowing for efficient handling of project iterations and updates. GitHub was used for remote repository hosting, facilitating collaboration and project sharing.

* `Deployment`: The application was deployed on PythonAnywhere, a cloud-based hosting platform that supports Python web applications.

## License

This project is licensed under the terms of the MIT license.
