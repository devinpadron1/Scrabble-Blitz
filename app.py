from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

with open("scrabble-words.txt", "r") as file:
    words = file.read().split()
# Words with 7 letters or less
filtered_words = [word for word in words if len(word) <= 7]

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/word', methods=['GET'])
def get_word():    

    # Default tiles with quantities
    default_tiles = {
        'A': {'points': 1, 'amount': 9},
        'B': {'points': 3, 'amount': 2},
        'C': {'points': 3, 'amount': 2},
        'D': {'points': 2, 'amount': 4},
        'E': {'points': 1, 'amount': 12},
        'F': {'points': 4, 'amount': 2},
        'G': {'points': 2, 'amount': 3},
        'H': {'points': 4, 'amount': 2},
        'I': {'points': 1, 'amount': 9},
        'J': {'points': 8, 'amount': 1},
        'K': {'points': 5, 'amount': 1},
        'L': {'points': 1, 'amount': 4},
        'M': {'points': 3, 'amount': 2},
        'N': {'points': 1, 'amount': 6},
        'O': {'points': 1, 'amount': 8},
        'P': {'points': 3, 'amount': 2},
        'Q': {'points': 10, 'amount': 1},
        'R': {'points': 1, 'amount': 6},
        'S': {'points': 1, 'amount': 4},
        'T': {'points': 1, 'amount': 6},
        'U': {'points': 1, 'amount': 4},
        'V': {'points': 4, 'amount': 2},
        'W': {'points': 4, 'amount': 2},
        'X': {'points': 8, 'amount': 1},
        'Y': {'points': 4, 'amount': 2},
        'Z': {'points': 10, 'amount': 1},  # blank tiles
    }
    # In game tiles
    current_tiles = {letter: {'points': values['points'], 'amount': values['amount']} for letter, values in default_tiles.items()}
    
    first_Turn = True
    word_not_in_board = True
    while word_not_in_board:
        if (first_Turn): # return word from scrabble dictionary thats 7 letters or less
            word = random.choice(filtered_words)
            first_Turn = False
        else:
            word = random.choice(words)

        # split word into array of letters
        word_letters = list(word)

        counter = 0 # tiles removed
        enough_tiles = True
        for letter in word_letters:
            if current_tiles[letter]['amount'] > 0:
                current_tiles[letter]['amount'] -= 1
                counter += 1
            else: # if not enough tiles
                for letter in word_letters[:counter]: # add previous letter tiles back
                    current_tiles[letter]['amount'] += 1
                enough_tiles = False
                first_Turn = True
                break # break inner loop if not enough tiles
        
        if enough_tiles:
            counter = 0
            break # break outer loop

    def player_tiles(current_tiles, num_tiles):
        tile_rack = []

        # list of available letter tiles
        tile_letters = [letter for letter, data in current_tiles.items() if data['amount'] > 0]
        
        # add random, available tiles to tile_rack
        for _ in range(num_tiles):
            if tile_letters:
                selected_tile = random.choice(tile_letters)
                tile_rack.append(selected_tile)
                current_tiles[selected_tile]['amount'] -= 1

        return tile_rack
    
    # Makes data tuples to preserve order
    
    tiles = player_tiles(current_tiles, 7)
    print(word, tiles)
    return jsonify({"word": word, "tiles": tiles})

# Only run code when imported as script, not a module
if __name__ == '__main__':
    app.run(debug=True)