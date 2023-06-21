document.addEventListener("DOMContentLoaded", function(event) {

    // Fetch word and rack from Flask
    fetch('http://127.0.0.1:5000/word')
    .then(response => response.json())
    .then(data => {
        let wordString = data.word;
        let playerTiles = data.tiles;
        let startPosition = Number(data.position);
        let orientation = data.orientation;
        loadWord(wordString, startPosition, orientation);
        loadTiles(playerTiles);
    })
    .catch((error) => {
        console.error('Error:', error);
    });

    let tileCount = 0;

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

    function dragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.id);
        e.dataTransfer.effectAllowed = "move";
        e.target.style.opacity = '0.01'; 
        e.stopPropagation();
        console.log('Drag Start');
    }
    function dragEnter(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    function dragEnd(e) {
        e.target.style.opacity = '1';
        console.log('Drag End');
    }   
    function dragOver(e) {
        e.preventDefault();
        e.stopPropagation();
    }   
    function dragLeave(e) {
        e.stopPropagation();
        console.log('Drag Leave');
    }
    function drop(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('Drop');
        const id = e.dataTransfer.getData('text/plain');
        const draggableElement = document.getElementById(id);
        const dropzone = e.target;
        if (!dropzone.classList.contains('board-square')) {
            dropzone = dropzone.parentNode;
        }
        if (!dropzone.querySelector(".tile")) {  // check if dropzone is empty
            draggableElement.parentNode.removeChild(draggableElement); // Remove the tile from its original parent
            dropzone.appendChild(draggableElement); // Append it to the dropzone
            // Send tile position to Python
            let tilePosition = {
                tileID: draggableElement.id,
                position: dropzone.id,
            };
            fetch('http://127.0.0.1:5000/tile-position', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(tilePosition),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        } else {
            console.log('Square is occupied');
        }
    }

    function addLetterAndNumber(tileDiv, letter) {
        let letterDiv = document.createElement('div');
        letterDiv.textContent = letter; // Set the text content of the <div> element
        letterDiv.classList.add("letter");
        tileDiv.appendChild(letterDiv); // Add the letter div to the tile div

        let valueDiv = document.createElement('div');
        valueDiv.textContent = letterValues[letter]; // Set the text content of the value div
        valueDiv.classList.add("value");
        tileDiv.appendChild(valueDiv); // Add the value div to the tile div

        tileCount++;
    }

    function tileGenerator(letter, id) {
        let tileDiv = document.createElement('div');
        addLetterAndNumber(tileDiv, letter)

        // Drag Features
        tileDiv.setAttribute('draggable', true);
        tileDiv.setAttribute('id', id);  // Assign a unique ID to the tile
        tileDiv.classList.add("tile");
        tileDiv.addEventListener('dragstart', dragStart);
        tileDiv.addEventListener('dragend', dragEnd);

        return tileDiv
    }

    function tileWordGenerator(letter) {
        let tileDiv = document.createElement('div');
        addLetterAndNumber(tileDiv, letter)
        return tileDiv
    }

    function loadWord(wordString, position, orientation) {
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

    function loadTiles(tiles) {
        let tileLength = tiles.length;

        for (let i=0; i < tileLength; i++) {
            let tileDiv = tileGenerator(tiles[i], `${tiles[i]}${i}`);
            tileDiv.className = 'tile-tray';
            let container = document.getElementById(`tray`);
            container.appendChild(tileDiv);
        }
    }
    
    // Load the board.
    for (let i = 1; i <= 11; i++) {
        for (let j = 1; j <= 11; j++) {
            // Create element
            var boardSquare = document.createElement("div");
            // assign its id
            boardSquare.setAttribute("class", "board-square");
            // assign coordinates
            boardSquare.setAttribute("id", `grid${i}_${j}`);
            boardSquare.addEventListener('dragover', dragOver);
            boardSquare.addEventListener('dragenter', dragEnter);
            boardSquare.addEventListener('dragleave', dragLeave);
            boardSquare.addEventListener('drop', drop);
            
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

    document.getElementById('play-button').addEventListener('click', function() {
        document.getElementById('instructions').style.display = 'none';
        document.getElementById('high-score-button').style.display = 'none';
        document.getElementById('game-screen').style.display = 'flex';
        startGame(); 
    });

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
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    function startGame() {
        // Start the game: 
        // 1. Start the timer.
        // 2. Load the tray.
    }
})


// TODO: Add ability to return tile into stack.
// TODO: Add ability to move tile within the stack.
// TODO: Don't allow for tiles to stack on top of each other