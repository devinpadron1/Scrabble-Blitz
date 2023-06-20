from flask import Flask, jsonify, render_template, request
import random

app = Flask(__name__)

# Open scrabble list of words
with open("scrabble-words.txt", "r") as file:
    words_list = file.read().split()

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

BONUS_SQUARES = {
    'TW': [[0,0], [0,10], [10,0], [10,10]],
    'TL': [[0,5], [2,2], [2,8], [5,0], [5,10], [8,2], [8,8], [10,5]],
    'DW': [[1,1], [1,9], [3,3], [3,7], [5,5], [7,3], [7,7], [9,1], [9,9]],
    'DL': [[0,3], [0,7], [2,5], [3,0], [3,10], [4,4], [4,6],
           [5,2], [5,8], [6,4], [6,6], [7,0], [7,10], [8,5], [10,3], [10,7]],
}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/word', methods=['GET'])
def load_initial_state():    
    word = word_manager.get_first_word()
    tiles = word_manager.tile_manager.get_player_tiles(7)
    position, orientation = word_manager.initial_position(word)
    
    board_manager.clear_board()
    board_manager.add_first_word(word, position, orientation) # Adds it to the Python grid
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
    taken_spaces_horizontal = [] # Spaces wont be checked in horizontal direction
    taken_spaces_vertical = []  # Same as ^ in vertical direction
    words_on_board = {}
    
    def add_word(row, col, direction): # Returns word and spaces it takes up
        word, taken_hor, taken_ver = word_manager.check_word(row, col, direction) 
        if direction == "right":
            taken_spaces_horizontal.extend(taken_hor)
            words_on_board[word] = taken_hor
        else: 
            taken_spaces_vertical.extend(taken_ver)
            words_on_board[word] = taken_ver

    # Check if a word can be formed in a direction
    def check_for_word_and_add(row, col, direction):
        if word_manager.check_under(row, col)[0].isalpha() and direction == 'under':
            add_word(row, col, "under")
        elif word_manager.check_right(row, col)[0].isalpha() and direction == 'right':
            add_word(row, col, "right")

    # Loop through the grid, recognizing any valid word
    for i in range(11):
        for j in range(11):
            grid_element = board_manager.board[i][j][0]
            position = (i, j)
            # Skip the grid element if it is taken in both directions
            if position in taken_spaces_vertical and position in taken_spaces_horizontal:
                continue

            if grid_element.isalpha():
                if position not in taken_spaces_vertical and position not in taken_spaces_horizontal:
                    # Edge cases
                    if i == 10:
                        check_for_word_and_add(i, j, 'right')
                    elif j == 10:
                        check_for_word_and_add(i, j, 'under')
                    else:
                        check_for_word_and_add(i, j, 'under')
                        check_for_word_and_add(i, j, 'right')

                elif position in taken_spaces_vertical:
                    check_for_word_and_add(i, j, 'right')

                elif position in taken_spaces_horizontal:
                    check_for_word_and_add(i, j, 'under')

    board_manager.display()
    print(words_on_board)

    # TODO: Add code that verifies if all words in the dictionary are valid
    all_words_valid = True
    for word in words_on_board:
        if word not in words_list:
            print(word, "is not a valid word")
            all_words_valid = False
            response = {
                'message': f'{word} is not a valid word. Try again.'
            }
            return jsonify(response), 400 # 400 typically communicates client error
            # TODO: Reset tiles: In order to reset tiles I need to distinguish player tiles with in board tiles. 
    
    if all_words_valid:
        # Check if words intersecting
            # if no 
                # invalid_submission()
        return '', 200
    # else
        # print a message telling the user what the invalid word was
        # invalid_submission()

    # def invalid_submission()
        # clear board except for existing valid words
        # reset tiles back to player's rack
            
    word_manager.intercept_check(words_on_board) # checks if words have an intercepting square, if not, gets removed

    return '', 200

class TileManager:
    def __init__(self): # Currently used tiles
        self.current_tiles = {letter: {'points': values['points'], 'amount': values['amount']} for letter, values in DEFAULT_TILES.items()}

    def get_player_tiles(self, num_tiles): # Generates player-held tiles
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
        self.filtered_words = [word for word in words_list if len(word) <= 7]
        self.tile_manager = TileManager()
    
    def get_first_word(self):                
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
        # Defines tile that goes in the middle
        random_letter_index = random.randint(0, len(word) - 1)

        # if word has 7 letters and the random letter is either first or last, shift the index
        if len(word) == 7 and random_letter_index in [0, len(word) - 1]:
            random_letter_index = random_letter_index + 1 if random_letter_index == 0 else random_letter_index - 1

        orientation = random.choice(["horizontal", "vertical"])

        return random_letter_index, orientation
    
    def check_under(self, row, col):
        if row < 10:
            return board_manager.board[row + 1][col]
        else:
            return "1"
    def check_right(self, row, col):
        if col < 10:
            return board_manager.board[row][col + 1]
        else: 
            return "1"

    def check_word(self, row, col, direction):
        counter = 0
        potential_word = ""
        taken_horizontal = []
        taken_vertical = []
        check_func = self.check_right if direction == "right" else self.check_under

        element_contains_letter = check_func(row, col)[0].isalpha()
        while element_contains_letter:
            if (col if direction == "right" else row) + counter <= 10:
                letter = board_manager.board[row + counter if direction == "under" else row][col if direction == "under" else col + counter][0]
                if letter == "_":
                    element_contains_letter = False
                else:
                    potential_word += letter
                    counter += 1
            else:
                element_contains_letter = False
        start_coord = [row, col]
        end_coord = [row + counter - 1, col] if direction == "under" else [row, col + counter - 1]
        if direction == "under":
            taken_vertical = self.generate_coordinates(start_coord, end_coord)
        else:
            taken_horizontal = self.generate_coordinates(start_coord, end_coord)
        return potential_word, taken_horizontal, taken_vertical
    
    # Returns array of coordinates between two points
    def generate_coordinates(self, start, end): 
        if start[1] == end[1]: # Vertical word (constant y)
            return [(x, start[1]) for x in range(start[0], end[0] + 1)]
        elif start[0] == end[0]: # Horizontal word (constant x)
            return [(start[0], y) for y in range(start[1], end[1] + 1)]

    def intercept_check(self, words): # Do the words contain a square that intercepts another?
        words_to_remove = set()
        for word1, coords1 in words.items():
            # flag to indicate if the word has any shared coordinate
            has_shared_coordinate = False
            for word2, coords2 in words.items():
                if word1 != word2:  # avoid self comparison
                    # check for shared coordinates
                    if any(coord in coords2 for coord in coords1):
                        has_shared_coordinate = True
                        break  # no need to check further
            # if the word has no shared coordinate, add it to removal set
            if not has_shared_coordinate:
                words_to_remove.add(word1)
        # remove words that have no shared coordinate
        for word in words_to_remove:
            del words[word]

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

board_manager = BoardManager()
word_manager = WordManager()

# Only run code when imported as script, not a module
if __name__ == '__main__':
    app.run(debug=True)

# TODO: Add points functionality. Bonus squares, etc.
# TODO: If tile from an existing word isn't used then its invalid.
# TODO: Add timer functionality
# TODO: Add existing word and its tiles
            # I need a way to differentiate between the existing word(s) on the
            # board and the new tiles im adding. Perhaps a seperate dictionary
            # would do the trick

# DID: Communicate invalid word to player.