from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# Open scrabble list of words
with open("scrabble-words.txt", "r") as file:
    words = file.read().split()

DEFAULT_TILES = {
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

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


class TileManager:
    def __init__(self): # Currently used tiles
        self.current_tiles = {letter: {'points': values['points'], 'amount': values['amount']} for letter, values in DEFAULT_TILES.items()}

    def player_tiles(self, num_tiles): # Current player-held tiles
        tile_rack = []
        # add random, available tiles to tile_rack
        for _ in range(num_tiles):
            # list of available letter tiles
            tile_letters = [letter for letter, data in self.current_tiles.items() if data['amount'] > 0]
            if tile_letters:
                selected_tile = random.choice(tile_letters)
                tile_rack.append(selected_tile)
                self.current_tiles[selected_tile]['amount'] -= 1
        return tile_rack


class WordManager:
    def __init__(self):
        self.filtered_words = [word for word in words if len(word) <= 7]
        self.tile_manager = TileManager()
    
    def select_first_word(self):
        # Words with 7 letters or less
        filtered_words = [word for word in words if len(word) <= 7]
        
        word_not_in_board = True
        while word_not_in_board:
            word = random.choice(filtered_words)

            # split word into array of letters
            word_letters = list(word)

            counter = 0 # tiles removed
            enough_tiles = True

            # Verifies if there are enough tiles to create the word
            for letter in word_letters:
                if self.tile_manager.current_tiles[letter]['amount'] > 0:
                    self.tile_manager.current_tiles[letter]['amount'] -= 1
                    counter += 1
                else: # if not enough tiles
                    for letter in word_letters[:counter]: # add previous letter tiles back
                        self.tile_manager.current_tiles[letter]['amount'] += 1
                    enough_tiles = False
                    break # break inner loop if not enough tiles
            if enough_tiles:
                counter = 0
                break # break outer loop
        return word


@app.route('/word', methods=['GET'])
def send_word():    
    word_manager = WordManager()
    word = word_manager.select_first_word()
    tiles = word_manager.tile_manager.player_tiles(7)
    print(word, tiles)
    return jsonify({"word": word, "tiles": tiles})

# Only run code when imported as script, not a module
if __name__ == '__main__':
    app.run(debug=True)

# TODO: Add logic that shows the position of the first word.
    # Communicate starting position to JS
# TODO: Fix AttributeError within WordManager
