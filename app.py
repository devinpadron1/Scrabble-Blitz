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
    # This is where you would get a word from your word source.
    
    # Initialize key variables
    points = amount = None

    # Create tiles with values and quantities
    default_tiles = {
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
        '_': {points: 0, amount: 2}, # blank tiles
      }
    current_tiles = {
        'A': {'amount': 9},
        'B': {'amount': 2},
        'C': {'amount': 2},
        'D': {'amount': 4},
        'E': {'amount': 12},
        'F': {'amount': 2},
        'G': {'amount': 3},
        'H': {'amount': 2},
        'I': {'amount': 9},
        'J': {'amount': 1},
        'K': {'amount': 1},
        'L': {'amount': 4},
        'M': {'amount': 2},
        'N': {'amount': 6},
        'O': {'amount': 8},
        'P': {'amount': 2},
        'Q': {'amount': 1},
        'R': {'amount': 6},
        'S': {'amount': 4},
        'T': {'amount': 6},
        'U': {'amount': 4},
        'V': {'amount': 2},
        'W': {'amount': 2},
        'X': {'amount': 1},
        'Y': {'amount': 2},
        'Z': {'amount': 1},
        '_': {'amount': 2},  # blank tiles
    }
    first_Turn = True
    while True:
        # return a random word from scrabble dictionary
        if (first_Turn):
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
                # add previous letter tiles back
                for letter in word_letters[:counter]:
                    current_tiles[letter]['amount'] += 1
                enough_tiles = False            
                break # break inner loop if not enough tiles
        
        if enough_tiles:
            counter = 0
            break # break outer loop

    return jsonify({"word": word})

# Only run code when imported as script, not a module
if __name__ == '__main__':
    app.run(debug=True)