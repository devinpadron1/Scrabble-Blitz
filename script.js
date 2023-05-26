document.getElementById('play-button').addEventListener('click', function() {
    document.getElementById('instructions').style.display = 'none';
    document.getElementById('game-screen').style.display = 'flex';
    startGame();
});

function startGame() {
    // Start the game: 
    // 1. Start the timer.
    // 2. Load the board.
    // 3. Load the tray.
}


// Create tiles with values and quantities
const scrabbleTiles = {
    'A': {points: 1, amount: 9},
    'B': {points: 3, amount: 2},
    'C': {points: 3, amount: 2},
    'D': {points: 2, amount: 4},
    'E': {points: 1, amount: 12},
    'F': {points: 4, amount: 2},
    'G': {points: 2, amount: 3},
    'H': {points: 4, amount: 2},
    'I': {points: 1, amount: 9},
    'J': {points: 8, amount: 1},
    'K': {points: 5, amount: 1},
    'L': {points: 1, amount: 4},
    'M': {points: 3, amount: 2},
    'N': {points: 1, amount: 6},
    'O': {points: 1, amount: 8},
    'P': {points: 3, amount: 2},
    'Q': {points: 10, amount: 1},
    'R': {points: 1, amount: 6},
    'S': {points: 1, amount: 4},
    'T': {points: 1, amount: 6},
    'U': {points: 1, amount: 4},
    'V': {points: 4, amount: 2},
    'W': {points: 4, amount: 2},
    'X': {points: 8, amount: 1},
    'Y': {points: 4, amount: 2},
    'Z': {points: 10, amount: 1},
    '_': {points: 0, amount: 2}, // blank tiles
  };

// Create board grid, 15x15
for (let i = 0; i < 14; i++) {
    for (let j = 0; j < 14; j++) {
        // Create grid
    }
}
