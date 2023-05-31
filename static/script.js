document.addEventListener("DOMContentLoaded", function(event) {
    let fetchedWord;

    // Fetch word from Flask
    fetch('http://127.0.0.1:5000/word')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        fetchedWord = data.word;
        console.log('Type of fetchedWord:', typeof fetchedWord);
        loadWord(fetchedWord);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
    
    function loadWord(word) {
        let letters = word.split('')
        for(let i=0; i<letters.length; i++){
            // Get a reference to the square where the letter should go
            
            const tileDiv = document.createElement('div');
            tileDiv.className = 'tile'; // Set the class name of the <div> element
            tileDiv.textContent = `${letters[i]}`; // Set the text content of the <div> element

            let container = document.getElementById(`grid8_${1+(i)}`);
            container.appendChild(tileDiv);
        }
    }
    
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
            const doubleLetter = new Set(["1_4", "1_12", "3_7", "3_9", "4_1", "4_8", "4_15", "7_3", "7_7", "7_9", "7_13", "8_4", "8_12", "9_3", "9_7", "9_9", "9_13", "12_1", "12_8", "12_15", "13_7", "13_9", "15_4", "15_12"]);
            const tripleLetter = new Set(["2_6", "2_10", "6_2", "6_6", "6_10", "6_14", "10_2", "10_6", "10_10", "10_14", "14_6", "14_10"]);
            const doubleWord = new Set(["2_2", "2_14", "3_3", "3_13", "4_4", "4_12", "5_5", "5_11", "7_3", "7_7", "7_9", "7_13", "9_3", "9_7", "9_9", "9_13", "11_5", "11_11", "12_4", "12_12", "13_3", "13_13", "14_2", "14_14"]);
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

    document.getElementById('play-button').addEventListener('click', function() {
        document.getElementById('instructions').style.display = 'none';
        document.getElementById('high-score-button').style.display = 'none';
        document.getElementById('game-screen').style.display = 'flex';
        startGame(); 
    });
    
    function startGame() {
        // Start the game: 
        // 1. Start the timer.
        // 2. Load the tray.
    }
})

// TODO: Create letter tile
// TODO: Add star to center square
// TODO: Add letters to bonus squares
// TODO: Load tray of letters
