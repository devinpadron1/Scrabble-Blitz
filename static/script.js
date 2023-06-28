document.addEventListener("DOMContentLoaded", function(event) {
    
    const letterValues = {
        'A': 1,
        'B': 3,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 4,
        'G': 2,
        'H': 4,
        'I': 1,
        'J': 8,
        'K': 5,
        'L': 1,
        'M': 3,
        'N': 1,
        'O': 1,
        'P': 3,
        'Q': 10,
        'R': 1,
        'S': 1,
        'T': 1,
        'U': 1,
        'V': 4,
        'W': 4,
        'X': 8,
        'Y': 4,
        'Z': 10
    };

    document.getElementById('play-button').addEventListener('click', function() {
        document.getElementById('instructions').style.display = 'none';
        document.getElementById('game-screen').style.display = 'flex';
        startGame(); 
    });
    
    function startGame() {
        loadBoard();
        getTiles();
        startTimer();
    }
    
    function getTiles() {
        fetch('http://127.0.0.1:5000/word')
            .then(response => response.json())
            .then(data => {
                let wordString = data.word;
                let playerTiles = data.tiles;
                let startPosition = Number(data.position);
                let orientation = data.orientation;
                loadInitialWord(wordString, startPosition, orientation);
                loadPlayerTiles(playerTiles);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    function loadInitialWord(wordString, position, orientation) {
        // Load Word
        let wordLength = wordString.length;

        // Build out word
        for (let i=0; i < wordLength; i++) {
            let tileDiv = tileWordGenerator(wordString[i], `wordTile${i}`);
            tileDiv.className = 'tile-ingame'; // Set the class name of the <div> element
            if (orientation == "vertical") {
                let container = document.getElementById(`grid${6+i-position}_6`);
                container.appendChild(tileDiv);
            } else if (orientation == "horizontal") {
                let container = document.getElementById(`grid6_${6+i-position}`);
                container.appendChild(tileDiv);
            }
        }
    }

    function loadPlayerTiles(tiles) {
        let tileLength = tiles.length;
        let container = document.getElementById(`tray`);
            
        for (let i=0; i < tileLength; i++) {
            let letter = tiles[i].charAt(0);
            let tileID = tiles[i];
            let tileDiv = tileGenerator(letter, tileID);
            tileDiv.className = 'tile-tray';
            container.appendChild(tileDiv);
        }

        // Adds ability to drag and sort tiles in player hand.
        Sortable.create(container, {
            group: 'shared',
            animation: 100,
            onMove: evt => preventPlacementIfTaken(evt),
            onEnd: evt => {
                sendTilePlacementToServer(evt.item.id, evt.to.id);
            }
        });
    }

    function tileGenerator(letter, id) {
        let tileDiv = document.createElement('div');
        addLetterAndNumber(tileDiv, letter)
        tileDiv.setAttribute('id', id);  // Assign a unique ID to the tile
        tileDiv.classList.add("tile");    

        return tileDiv
    }

    function tileWordGenerator(letter) {
        let tileDiv = document.createElement('div');
        addLetterAndNumber(tileDiv, letter)
        return tileDiv
    }
    
    // Load board
    function loadBoard() {
        for (let i = 1; i <= 11; i++) {
            for (let j = 1; j <= 11; j++) {
                var boardSquare = document.createElement("div");
                boardSquare.setAttribute("class", "board-square");
                
                // assign coordinates
                boardSquare.setAttribute("id", `grid${i}_${j}`);
                
                // Create sets for each special square
                const doubleLetter = new Set(["1_4", "1_8", "3_6", "4_1", "4_11", "5_5", "5_7", "6_3", "6_9", "7_5", "7_7", "8_1", "8_11", "9_6", "11_4", "11_8"]);
                const tripleLetter = new Set(["1_6", "3_3", "3_9", "6_1", "6_11", "9_3", "9_9", "11_6"]);
                const doubleWord = new Set(["2_2", "2_10", "4_4", "4_8", "8_4", "8_8", "10_2", "10_10"]);
                const tripleWord = new Set(["1_1", "1_11", "11_1", "11_11"]);
    
                let position = `${i}_${j}`;
                
                // Adds text and class to bonus squares
                if (doubleLetter.has(position)) {
                    boardSquare.classList.add("double-letter");
                    // Add span element with bonus text
                    const bonusText = document.createElement('span');
                    bonusText.className = 'bonus-text';
                    boardSquare.appendChild(bonusText);
                } else if (tripleLetter.has(position)) {
                    boardSquare.classList.add("triple-letter");
                    const bonusText = document.createElement('span');
                    bonusText.className = 'bonus-text';
                    boardSquare.appendChild(bonusText);
                } else if (doubleWord.has(position)) {
                    boardSquare.classList.add("double-word");
                    const bonusText = document.createElement('span');
                    bonusText.className = 'bonus-text';
                    boardSquare.appendChild(bonusText);
                } else if (tripleWord.has(position)) {
                    boardSquare.classList.add("triple-word");
                    const bonusText = document.createElement('span');
                    bonusText.className = 'bonus-text';
                    boardSquare.appendChild(bonusText);    
                }
    
                // Append to container element
                var boardContainer = document.getElementById("board-square-container");
                boardContainer.appendChild(boardSquare);
            }
        }
        makeSquaresDroppable();
    }

    document.getElementById('submit').addEventListener('click', function() {
        fetch('http://127.0.0.1:5000/submit', {
            method: 'POST'
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            if (data.message) {
                document.querySelector('#message span').innerText = data.message;
                document.querySelector('#message span').style.color = 'red';
            }
            if (data.tiles_to_remove) {
                for (let pos of data.tiles_to_remove) {
                    let [row, col] = pos;
                    console.log(`row: ${row}, col: ${col}, gridID: grid${row + 1}_${col + 1}`);
                    let tileElement = document.getElementById(`grid${row + 1}_${col + 1}`).querySelector(".tile-tray");
                    console.log(tileElement);                    
                    // Remove tile from board
                    tileElement.remove();
                    // Append tile to player's hand
                    document.getElementById(`tray`).appendChild(tileElement);
                }
            }
            // Changes to be made after valid move
            if (data.status == 200) {
                document.querySelector('#message span').innerText = data.message;
                document.querySelector('#message span').style.color = 'green';

                // Change class of tiles on the board from 'tile-tray' to 'tile-ingame'
                let boardContainer = document.getElementById('board-square-container');
                let gameBoardTiles = boardContainer.querySelectorAll('.board-square .tile-tray');                
                gameBoardTiles.forEach(tile => {
                    tile.classList.add('tile-ingame');
                    tile.classList.remove('tile-tray');
                });
                // Load new tiles into player's hand
                if (data.tiles) {
                    let playerTiles = data.tiles;
                    loadPlayerTiles(playerTiles);
                }
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    // Shuffle button
    document.getElementById('shuffle-button').addEventListener('click', function() {
        fetch('http://127.0.0.1:5000/shuffle', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            // Remove current tiles from the tray
            let trayElement = document.getElementById('tray');
            while (trayElement.firstChild) {
                trayElement.removeChild(trayElement.firstChild);
            }
            // Load the new shuffled tiles
            loadPlayerTiles(data.tiles);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    function addLetterAndNumber(tileDiv, letter) {
        let letterDiv = document.createElement('div');
        letterDiv.textContent = letter; // Set the text content of the <div> element
        letterDiv.classList.add("letter");
        tileDiv.appendChild(letterDiv); // Add the letter div to the tile div

        let valueDiv = document.createElement('div');
        valueDiv.textContent = letterValues[letter]; // Set the text content of the value div
        valueDiv.classList.add("value");
        tileDiv.appendChild(valueDiv); // Add the value div to the tile div
    }

    function makeSquaresDroppable() {
        let boardContainer = document.getElementById("board-square-container");
        // Iterate through all child nodes of the board container and make them sortable
        for (let i = 0; i < boardContainer.children.length; i++) {
            Sortable.create(boardContainer.children[i], {
                group: 'shared', // set both sortables to same group
                filter: '.tile-ingame',
                onMove: evt => preventPlacementIfTaken(evt),
                onEnd: evt => {
                    sendTilePlacementToServer(evt.item.id, evt.to.id);
                }
            });
        }
    }

    function preventPlacementIfTaken(evt) {
        // if the target already has a child that is a div (i.e., a tile), cancel the move
        let children = evt.to.children;
        for (let j = 0; j < evt.to.children.length; j++) {
            if (children[j].nodeName === 'DIV' && children[j].classList.contains('tile-ingame')) {
                return false;
            }
        }
        return true; // if no tiles are found
    }

    function sendTilePlacementToServer(tileID, squareID) {
        let position;
        if (squareID.startsWith('grid')) {
            position = 'board';
        } else {
            position = 'tray';
        }
        
        // Construct the data object
        let data = {
            tileID: tileID,
            squareID: squareID,
            position: position,
        };
    
        // Send a fetch request
        fetch('/tile-position', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    
    function startTimer() {
        // Set the initial time (in seconds)
        let timeRemaining = 2 * 60;
        // Get the timer element
        let timerElement = document.getElementById("timer");
    
        // Update the timer display
        function updateTimerDisplay() {
            let minutes = Math.floor(timeRemaining / 60);
            let seconds = timeRemaining % 60;
            // Pad the minutes and seconds with leading zeros if necessary
            seconds = seconds < 10 ? "0" + seconds : seconds;
            // Update the timer element
            timerElement.innerText = `${minutes}:${seconds}`;
        }
    
        // Call the update function immediately to display the initial time
        updateTimerDisplay();
    
        // Set up the interval
        let timerInterval = setInterval(function() {
            // Decrease the time remaining
            timeRemaining--;
            // Update the timer display
            updateTimerDisplay();
            // If the time has run out, stop the interval
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
            }
        }, 1000);
    }
})