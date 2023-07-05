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

    let dropSound = new Audio("static/tile_drop.mp3");
    let invalidSound = new Audio("static/invalid.mp3");
    let validSound = new Audio("static/valid.mp3");
    let highScoreSound = new Audio("static/high-score.mp3");
    let endSound = new Audio("static/end.mp3");
    dropSound.volume = .2;
    invalidSound.volume = .08;
    validSound.volume = .3;
    highScoreSound.volume = .2;
    endSound.volume = .05;

    const audioObjects = [dropSound, invalidSound, validSound, highScoreSound, endSound];

    document.getElementById('play-button').addEventListener('click', function() {
        startLogic();
    });

    document.getElementById('sound').addEventListener('click', function() {
        soundTextContent = document.querySelector('#sound').innerText
        if (soundTextContent == "Sound (ON)") {
            document.querySelector('#sound').innerText = "Sound (OFF)";
            for (let i = 0; i < audioObjects.length; i++) {
                audioObjects[i].muted = true;
            };
        } else {
            document.querySelector('#sound').innerText = "Sound (ON)";
            for (let i = 0; i < audioObjects.length; i++) {
                audioObjects[i].muted = false;
            };
        }
    });

    document.getElementById('new-game').addEventListener('click', function() {
        document.getElementById('shuffle').style.removeProperty('display');
        document.getElementById('submit').style.removeProperty('display');
        document.getElementById('discard').style.removeProperty('display');
        document.getElementById('new-game').classList.remove('end-game');
        document.querySelector('#points').innerHTML = 0; // Reset points
        timer.reset();
        timer.start();

        // Discard reset
        document.getElementById('discard').disabled = false;
        discards = 2;
        document.getElementById('discard').textContent = `Discard (${discards})`;

        displayMessage("", 'black');
        gameData.highScoreAchieved = false;
        startLogic();
    });

    function startLogic() {
        document.getElementById('instructions').style.display = 'none';
        document.getElementById('game-screen').style.display = 'flex';
        dropSound.play();
        startGame(); 
    }
    
    let gameLoaded = false;

    function startGame() {
        if (!gameLoaded) {
            loadBoard();
            gameLoaded = true;
        }
        getTiles();
        timer.start(); 
    }
    
    function getTiles() {
        fetch('/word')
            .then(response => response.json())
            .then(data => {
                clearTrayAndBoard();
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

    function clearTrayAndBoard() {
        const trayContainer = document.getElementById("tray");
        while (trayContainer.firstChild) {
            trayContainer.removeChild(trayContainer.firstChild);
        }

        let boardSquareContainer = document.getElementById('board-square-container');
        for (let i = 0; i < boardSquareContainer.children.length; i++) {
            let boardSquare = boardSquareContainer.children[i];
            let childNodes = Array.from(boardSquare.childNodes); // Create a copy of child nodes
            childNodes.forEach(child => {
                if (child.nodeName === "DIV") {
                    boardSquare.removeChild(child);
                }
            });
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
            animation: 50,
            onMove: evt => {
                let canMove = preventPlacementIfTaken(evt);
                return canMove;
            },
            onEnd: evt => {
                sendTilePlacementToServer(evt.item.id, evt.to.id);
                displayMessage("", 'black');
                dropSound.play();
            },
            chosenClass: 'sortable-chosen',
            forceFallback: true,
            fallbackClass: 'sortable-fallback',
            ghostClass: 'sortable-ghost',
            tolerance: 'pointer',
            swapThreshold: 0.65,
            invertSwap: true,
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

    let gameData = {
        highScoreAchieved: false,
        // Other game data here
    };

    document.getElementById('submit').addEventListener('click', function() {
        fetch('/submit', {
            method: 'POST'
        })
        .then(response => {
            return response.json()
        })
        .then(data => {
            if (data.message && data.status == 'fail') {
                invalidSound.play();
                displayMessage(data.message, 'red');
            }
            if (data.tiles_to_remove && data.status == 'fail') {
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
            if (data.status == 'success') {
                validSound.play();
                displayMessage(data.message, 'green');         

                // Change class of tiles on the board from 'tile-tray' to 'tile-ingame'
                let boardContainer = document.getElementById('board-square-container');
                let gameBoardTiles = boardContainer.querySelectorAll('.board-square .tile-tray');                
                gameBoardTiles.forEach(tile => {
                    tile.classList.add('tile-ingame');
                    tile.classList.remove('tile-tray');
                });

                timer.addTime(data.word_points); // to add 30 seconds    }
                                
                document.querySelector('#points').innerText = data.points;
                let highScore = parseInt(document.getElementById('high-score').innerText);
                if ((data.points > highScore) && !gameData.highScoreAchieved) {
                    displayMessage("New high score achieved! Congratulations!", 'blue');
                    document.querySelector('#message span').style.fontWeight = 'bold';
                    highScoreSound.play();
                    gameData.highScoreAchieved = true;
                }

                if (gameData.highScoreAchieved) {
                    document.querySelector('#high-score').innerHTML = data.points;
                }

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
    document.getElementById('shuffle').addEventListener('click', function() {
        fetch('/shuffle', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            dropSound.play();
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

    // Discard button
    document.getElementById('discard').addEventListener('click', function() {
        fetch('/discard', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                invalidSound.play();
                displayMessage(data.message, 'red');
            } else {
                dropSound.play();
                let tray = document.querySelector('#tray');
                while (tray.firstChild) { // Empty tray
                    tray.removeChild(tray.firstChild);
                }
                loadPlayerTiles(data.tiles);
                let discards = data.discards;
                document.getElementById('discard').textContent = `Discard (${discards})`;
                if (discards === 0) {
                    document.getElementById('discard').disabled = true;
                    displayMessage('You ran out of discards.', 'red')
                }
            }
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
                onMove: evt => {
                    let canMove = preventPlacementIfTaken(evt);
                    return canMove;
                },
                onEnd: evt => {
                    sendTilePlacementToServer(evt.item.id, evt.to.id);
                    displayMessage("", 'black');
                    dropSound.play();
                },
                chosenClass: 'sortable-chosen',
                forceFallback: true,
                fallbackClass: 'sortable-fallback',
                ghostClass: 'sortable-ghost',
                tolerance: 'pointer',
                swapThreshold: 0.65,
                invertSwap: true,
            });
        }
    }

    function preventPlacementIfTaken(evt) {
        if (evt.to.id === "tray") {
            return true;
        }
        // if the target already has a child that is a div (i.e., a tile), cancel the move
        let children = evt.to.children;
        for (let j = 0; j < evt.to.children.length; j++) {
            if (children[j].nodeName === 'DIV' && (children[j].classList.contains('tile-ingame') || children[j].classList.contains('tile-tray'))) {
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
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            console.log('Data successfully sent to the server.');
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
    
    function displayMessage(message, color) {
        document.querySelector('#message span').innerText = message;
        document.querySelector('#message span').style.color = color;
        document.querySelector('#message span').style.fontWeight = 'normal';
    }

    let timerInterval;

    let timer = {
        initialTime: 60 * 2, // 2 minutes
        timeRemaining: 60 * 2, // 2 minutes

        addTime: function(seconds) {
            this.timeRemaining += seconds;
        },

        reset: function() {
            this.timeRemaining = this.initialTime;
        },

        start: function() {
            // Get the timer element
            let timerElement = document.getElementById("timer");

            // Update the timer display
            function updateTimerDisplay() {
                let minutes = Math.floor(timer.timeRemaining / 60);
                let seconds = timer.timeRemaining % 60;
                // Pad the minutes and seconds with leading zeros if necessary
                seconds = seconds < 10 ? "0" + seconds : seconds;
                // Update the timer element
                timerElement.innerText = `${minutes}:${seconds}`;
            }

            // Clear the previous interval if it exists
            if(timerInterval) {
                clearInterval(timerInterval);
            }

            // Call the update function immediately to display the initial time
            updateTimerDisplay();

            // Set up the interval
            timerInterval = setInterval(function() {
                // Decrease the time remaining
                timer.timeRemaining--;
                // Update the timer display
                updateTimerDisplay();
                // If the time has run out, stop the interval
                if (timer.timeRemaining <= 0) {
                    clearInterval(timerInterval);
                    displayMessage("Time's up! Play again!", 'black');
                    endSound.play();
                    document.getElementById('new-game').classList.add('end-game');
                    document.querySelector('#message span').style.fontWeight = 'bold';
                    document.getElementById('shuffle').style.display = 'none';
                    document.getElementById('submit').style.display = 'none';
                    document.getElementById('discard').style.display = 'none';
                    document.getElementById('new-game').style.display = 'block';
                }
            }, 1000);
        }
    }

})