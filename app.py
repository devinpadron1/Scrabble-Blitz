from flask import Flask, jsonify, render_template, request
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

    def player_tiles(self, num_tiles): # Generates player-held tiles
        tile_rack = []
        # Add random, available tiles to tile_rack
        for _ in range(num_tiles):
            # List of available letter tiles
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
        word_not_in_board = True
        while word_not_in_board:
            word = random.choice(self.filtered_words)

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

    def initial_position(self, word):
        random_letter_index = random.randint(0, len(word) - 1)

        # if word has 7 letters and the random letter is either first or last, shift the index
        if len(word) == 7 and random_letter_index in [0, len(word) - 1]:
            random_letter_index = random_letter_index + 1 if random_letter_index == 0 else random_letter_index - 1

        orientation = random.choice(["horizontal", "vertical"])

        return random_letter_index, orientation
    
    def check_under(self, row, col):
        return board_manager.board[row][col+1]  
    def check_right(self, row, col):
        return board_manager.board[row+1][col]

    def check_word(self, row, col, direction):
        counter = 0
        potential_word = ""
        taken_spaces = []
        if direction == "under":
            element_contains_letter = self.check_under(row, col)
            while element_contains_letter:
                if col + counter <= 10:
                    letter = board_manager.board[row][col+counter]
                    if letter == "_":
                        element_contains_letter = False
                    else:
                        potential_word += letter
                        counter += 1
                else:
                    element_contains_letter = False
            if potential_word in words:
                start_coord = [row, col]
                end_coord = [row, col + counter]
                print(potential_word, "is a valid word in cells", start_coord, "through", end_coord)
                taken_spaces = board_manager.taken_spaces(start_coord, end_coord, "vertical")
                return start_coord, end_coord, taken_spaces
            else:
                potential_word, start_coord, end_coord, taken_spaces = self.variable_reset()
                return start_coord, end_coord, taken_spaces

        elif direction == "right":
            element_contains_letter = self.check_right(row, col)
            while element_contains_letter:
                if row + counter <= 10:
                    letter = board_manager.board[row+counter][col]
                    if letter == "_":
                        element_contains_letter = False
                    else:
                        potential_word += letter
                        counter += 1
                else:
                    element_contains_letter = False
            if potential_word in words:
                start_coord = [row, col]
                end_coord = [row + counter, col]
                print(potential_word, "is a valid word in cells", start_coord, "through", end_coord)
                taken_spaces = board_manager.taken_spaces(start_coord, end_coord, "horizontal")
                return start_coord, end_coord, taken_spaces
            else:
                potential_word, start_coord, end_coord, taken_spaces = self.variable_reset()
                return start_coord, end_coord, taken_spaces
    
    def variable_reset(self):
        word = ""
        array = []
        print("No valid words on board.")
        return word, array, array, array

class BoardManager:
    def __init__(self, size=11): # Generate board
        self.board = [['_' for _ in range(size)] for _ in range(size)]

    def clear_board(self, size=11):
        self.board = [['_' for _ in range(size)] for _ in range(size)]

    def add_first_word(self, word, position, orientation):
        row, col = 5, 5 # Middle of board
        if orientation == "horizontal":
            for i, letter in enumerate(word):
                self.board[row][col+i-position] = letter
        elif orientation == "vertical":
            for i, letter in enumerate(word):
                self.board[row+i-position][col] = letter

    def add_letter(self, row, col, tileID):
        # If tile found in board, remove it
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == tileID:
                    self.board[i][j] = '_'
        self.board[row-1][col-1] = tileID

    def display(self):
        for row in self.board:
            print(' '.join(cell[0] for cell in row))

    def taken_spaces(self, start, end, orientation):
        # start = [i, j] | end = [i, j] | taken_pairs =  [[i, j], [i, j], [i, j]]
        taken_pairs = []
        if orientation == "horizontal":
            for n in range(start[1] - end[1]):
                # if there's a letter above or below, dont add it
                element_above = self.board[start[0] + 1][start[1] + n].isalpha()
                element_below = self.board[start[0] - 1][start[1] + n].isalpha()
                if not element_above or not element_below:
                    taken_pairs += [start[0], start[1] + n]
                    element_above = element_below = False
        elif orientation == "vertical":
            for n in range(start[0] - end[0]):
                # if there's a letter to the sides, don't add it
                element_left = self.board[start[0] + n][start[1] - 1].isalpha()
                element_right = self.board[start[0] + n][start[1] + 1].isalpha()
                if not element_left or not element_right:
                    taken_pairs += [start[0] + n, start[1]]
                    element_left = element_right = False
        return taken_pairs


board_manager = BoardManager()
word_manager = WordManager()

@app.route('/word', methods=['GET'])
def send_word():    
    word = word_manager.select_first_word()
    tiles = word_manager.tile_manager.player_tiles(7)
    position, orientation = word_manager.initial_position(word)
    
    board_manager.clear_board()
    board_manager.add_first_word(word, position, orientation)
    board_manager.display()

    print(word, tiles, position, orientation)

    return jsonify({"word": word, "tiles": tiles, "position": position, "orientation": orientation})

@app.route('/tile-position', methods=['POST'])
def update_tile_position():
    data = request.get_json()
    print(f"Received tile position: {data}")

    # Data Assignment
    tileID = data['tileID']
    letter = data['tileID'][0]
    position = data['position'].replace('grid','')
    row, col = map(int, position.split('_'))

    board_manager.add_letter(row, col, tileID)
    board_manager.display()

    print(letter, row, col)
    return '', 200

@app.route('/submit', methods=['POST'])
def submit():
    print(f"Received submit request")
    ## Define existing words
    # Loop through the grid
    taken_spaces = []
 
    for i in range(11):
        for j in range(11):
            if [i, j] not in taken_spaces: 
                grid_element = board_manager.board[i][j]
                if grid_element[0].isalpha():
                    # Right-most edge case
                    if i == 10:
                        word, start, end = word_manager.check_word(i, j, "under") # Check for letters under
                    # Bottom-most edge case
                    if j == 10:
                        word, start, end = word_manager.check_word(i, j, "right") # Check for letter to the right
                    if i < 10 and j < 10:
                        element_contains_letter = word_manager.check_under(i, j)
                        if element_contains_letter:
                            word, start, end = word_manager.check_word(i, j, "under")
                        element_contains_letter = word_manager.check_right(i, j)
                        if element_contains_letter:
                            word, start, end = word_manager.check_word(i, j, "right")

    print(board_manager.board)

    # if no letter is within one square of existing words, invalid submission

    # Verify that letter(s) placed are valid words
    # word needs to:
        # be in word (scrabble dictionary)
        # be attached to an existing word
        # Instance where you create a word parallel and next to another
            # Every letter needs to be checked horizontally & vertically
    return '', 200

# Only run code when imported as script, not a module
if __name__ == '__main__':
    app.run(debug=True)

# TODO: Add points functionality. Bonus squares, etc.
