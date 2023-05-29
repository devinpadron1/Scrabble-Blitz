document.addEventListener("DOMContentLoaded", function(event) {
    document.getElementById('play-button').addEventListener('click', function() {
        document.getElementById('instructions').style.display = 'none';
        document.getElementById('high-score-button').style.display = 'none';
        document.getElementById('game-screen').style.display = 'flex';
        startGame();
    });
    
    function startGame() {
        // Start the game: 
        // 1. Start the timer.
    
        // 2. Load the board.
        for (let i = 1; i <= 15; i++) {
            for (let j = 1; j <= 15; j++) {
                // Create element
                var boardSquare = document.createElement("div");
                // assign its id
                boardSquare.setAttribute("class", "board-square");
                // assign coordinates
                boardSquare.setAttribute("id", `grid${i}_${j}`);
                
                // Create sets for each special square
                const doubleLetter = new Set(["1_4", "1_12", "4_1", "4_8", "4_15", "12_1", "12_8", "12_15", "15_4", "15_12", "8_4", "8_12"]);
                const tripleLetter = new Set(["2_6", "2_10", "6_2", "6_6", "6_10", "6_14", "10_2", "10_6", "10_10", "10_14", "14_6", "14_10"]);
                const doubleWord = new Set(["2_2", "2_14", "3_7", "3_9", "7_3", "7_7", "7_9", "7_13", "9_3", "9_7", "9_9", "9_13", "13_7", "13_9", "14_2", "14_14"]);
                const tripleWord = new Set(["1_1", "1_8", "1_15", "8_1", "8_15", "15_1", "15_8", "15_15"]);

                let position = `${i}_${j}`;

                if (doubleLetter.has(position)) {
                    boardSquare.classList.add("double-letter");
                } else if (tripleLetter.has(position)) {
                    boardSquare.classList.add("triple-letter");
                } else if (doubleWord.has(position)) {
                    boardSquare.classList.add("double-word");
                } else if (tripleWord.has(position)) {
                    boardSquare.classList.add("triple-word");
                }

                // Append to container element
                var boardContainer = document.getElementById("board-square-container");
                boardContainer.appendChild(boardSquare);
        }
    }


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
    

})

// TODO: Load Grid
// TODO: Load initial word