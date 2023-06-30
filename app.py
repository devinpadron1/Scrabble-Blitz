from flask import Flask, jsonify, render_template, request
import random, copy

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
    global board_manager
    global tile_manager
    board_manager = BoardManager()
    tile_manager = TileManager()
    return render_template('index.html')

@app.route('/word', methods=['GET'])
def load_initial_state():    
    word = word_manager.get_first_word()
    position, orientation = word_manager.initial_position(word)

    tiles = tile_manager.get_player_tiles(7)
    
    board_manager.clear_board()
    board_manager.add_first_word(word, position, orientation) # Adds it to server-side grid
    board_manager.display()
    board_manager.existing_words[word] = "" 

    print(tiles)

    return jsonify({"word": word, "tiles": tiles, "position": position, "orientation": orientation})

@app.route('/tile-position', methods=['POST'])
def update_tile_position():
    data = request.get_json()
    print(f"Received tile position: {data}")
    tileID = data['tileID']

    if data['position'] == "tray":
        board_manager.remove_tile_from_board(data['tileID'])
        if data['tileID'] not in tile_manager.player_rack:
            tile_manager.player_rack.append(tileID)

    else: # being placed on board
        coordinates = data['squareID'].replace('grid','')
        row, col = map(int, coordinates.split('_'))

        board_manager.add_letter(row, col, tileID)

        if tileID in tile_manager.player_rack:
            tile_manager.player_rack.remove(tileID)

    board_manager.display()
    print("Player rack:", tile_manager.player_rack)
    print("List of player moves:", board_manager.player_moves)

    return ''

@app.route('/shuffle', methods=['POST'])
def shuffle():
    print(f"Received shuffle request")
    tile_manager.shuffle_tiles()
    print("Player rack:", tile_manager.player_rack)
    return jsonify({"tiles": tile_manager.player_rack})

@app.route('/discard', methods=['POST'])
def discard():
    print(f"Received discard request")
    
    tiles, discards = tile_manager.discard_tiles()
    print("New player rack:", tile_manager.player_rack)
    return jsonify({
        "tiles": tiles,
        "discards": discards,
    })

@app.route('/submit', methods=['POST'])
def submit():
    print(f"Received submit request")
    ## Define existing words
    taken_spaces_horizontal = [] # Spaces wont be checked in horizontal direction
    taken_spaces_vertical = []  # Same as ^ in vertical direction
    words_on_board = {}
    all_words_valid = True
    
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
        nonlocal all_words_valid
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

    # Add coordinates to existing word dictionary
    for key in words_on_board:
        if key in board_manager.existing_words:
            board_manager.existing_words[key] = words_on_board[key]

    # Verifies if all words on the board are valid
    if all_words_valid:
        for word in words_on_board:
            if word not in words_list:
                print(word, "is not a valid word")
                all_words_valid = False
                response = {
                    'message': f'{word} is not a valid word. Try again.',
                    'tiles_to_remove': board_manager.player_moves
                }
                board_manager.erase_player_moves()
                print(board_manager.display())
                return jsonify(response), 400 # 400 communicates client error
    
    if not bool(board_manager.player_moves): # if player moves is empty
        all_words_intercept = True
    else:
        all_words_intercept = word_manager.all_moves_intersect(words_on_board)

    # Valid submission
    if all_words_valid and all_words_intercept and bool(board_manager.player_moves):
        new_words_this_turn = []
        # word player created based on moves       
        for word, coord in words_on_board.items():
            if word not in board_manager.existing_words:
                board_manager.existing_words[word] = coord # Add new words to existing words
                new_words_this_turn.append(word)
        
        word = new_words_this_turn[0]
        unique_tiles_used = set([move[2] for move in board_manager.player_moves])
        old_player_rack = copy.deepcopy(tile_manager.player_rack)
        new_player_rack = tile_manager.get_player_tiles(len(unique_tiles_used))
        
        new_player_tiles = [tile for tile in new_player_rack if tile not in old_player_rack]
        print(tile_manager.player_rack)

        board_manager.player_moves = []
        board_manager.player_moves_coords = []
        
        response = {
            'message': f'{word} is a valid word. Create a new word.',
            'tiles': new_player_tiles,
            'status': 200
        }
        return jsonify(response)
    elif all_words_valid and all_words_intercept and not bool(board_manager.player_moves): # not bool checks if player moves is empty
        response = {
            'message': 'Place tiles to create a word.'
        }
        return jsonify(response)
    else: 
        response = {
            'message': 'Tile does not intercept with existing word. Try again',
            'tiles_to_remove': board_manager.player_moves
        }
        board_manager.erase_player_moves()
        print(board_manager.display())
        return jsonify(response), 400 # 400 communicates client error

    
class TileManager:
    def __init__(self): # Currently used tiles
        self.current_tiles = {letter: {'points': values['points'], 'amount': values['amount']} for letter, values in DEFAULT_TILES.items()}
        self.player_rack = []
        self.tile_id_counter = 0
        self.tiles_to_discard = 0
        self.discards = 2

    def get_player_tiles(self, num_tiles): # Generates player-held tiles
        # Add random, available tiles to player_rack
        for _ in range(num_tiles):
            # List of available letter tiles
            tile_letters = [letter for letter, data in self.current_tiles.items() if data['amount'] > 0]
            if tile_letters:
                selected_tile = random.choice(tile_letters)
                self.player_rack.append(selected_tile + str(self.tile_id_counter))
                self.tile_id_counter += 1
                self.current_tiles[selected_tile]['amount'] -= 1
        return self.player_rack

    def discard_tiles(self):
        self.tiles_to_discard = 0
        if self.discards > 0:
            for tile in self.player_rack.copy():
                self.player_rack.remove(tile)
                self.current_tiles[tile[0]]['amount'] += 1
                self.tiles_to_discard += 1
            self.discards -= 1
            return self.get_player_tiles(self.tiles_to_discard), self.discards

    def shuffle_tiles(self):
        random.shuffle(self.player_rack)

class WordManager:
    def __init__(self):
        self.filtered_words = [word for word in words_list if len(word) <= 7]
        self.points = 0
    
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
                if tile_manager.current_tiles[letter]['amount'] > 0:
                    tile_manager.current_tiles[letter]['amount'] -= 1
                    counter += 1
                else: # if not enough tiles
                    for letter in word_letters[:counter]: # add previous letter tiles back
                        tile_manager.current_tiles[letter]['amount'] += 1
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

    def all_moves_intersect(self, words_on_board):
        # Flattening the list of coordinates in existing_words
        existing_coords = [coord for coords in board_manager.existing_words.values() for coord in coords]
        # Counter for new words that intersect with existing words
        intersect_counter = 0
        for move in board_manager.player_moves_coords:
            for word, coords in words_on_board.items():
                if move in coords:  # If a move is part of a word
                    if any(coord in existing_coords for coord in coords):  # and if that word intersects with existing words
                        intersect_counter += 1
                        break
        # If the counter equals the number of new words, all new words intersect with existing words
        return intersect_counter == len(board_manager.player_moves_coords)
    
    def get_player_words(self, words_on_board):
        player_words = {}
        for word, coordinates in words_on_board:
            for coord in coordinates:
                if coord in board_manager.player_moves_coords:
                    player_words[word] = coordinates
        return player_words

    def get_points(self, words_on_board):
        player_words = self.get_player_words(words_on_board)
        points = 0
        double_word = False
        triple_word = False

        # player_words {      <- coordinates ->
        #           'word1': [(1,2), (1,3) ...],
        #           'word2': [(8,3), (9,3) ...]
        # }                     ^ coordinate

        for word, coordinates in player_words:
            for coordinate in coordinates:
                row = coordinate[0]
                col = coordinate[1]
                letter = board_manager.board[row][col] # find letter in position
                letter_Points = DEFAULT_TILES[letter]['points'] # find letter value
                
                # BONUS_SQUARES = {  spaces ->
                #       'TW': [[0,0], [1,1], ...]
                # }              ^ space

                for multiplier, spaces in BONUS_SQUARES:
                    for space in spaces:
                        if coordinate == space: 
                            if multiplier.startswith('D'):
                                if multiplier.endswith('L'):
                                    points += letter_Points * 2
                                elif multiplier.endswith('W'):
                                    double_word = True
                            elif multiplier.startswith('T'): 
                                if multiplier.endswith('L'):
                                    points += letter_Points * 3
                                elif multiplier.endswith('W'):
                                    triple_word = True
            if double_word:
                points *= 2
            elif triple_word:
                points *= 3
            double_word = False
            triple_word = False
        return self.points

class BoardManager:
    def __init__(self, size=11): # Generate board
        self.board = [['_' for _ in range(size)] for _ in range(size)]
        self.player_moves = []          # [(10, 7, 'L6')]
        self.player_moves_coords = []   # [(10, 7)]
        self.existing_words = {}

    def clear_board(self, size=11):
        self.board = [['_' for _ in range(size)] for _ in range(size)]
        self.player_moves = []

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
        # Check if this tileID already exists in player_moves
        for i in range(len(self.player_moves)):
            if self.player_moves[i][2] == tileID:
                # If it does, replace the old move with the new one and return
                self.player_moves[i] = (row-1, col-1, tileID)
                self.player_moves_coords[i] = (row-1, col-1)
                return
                
        # If we didn't find the tileID in player_moves, append it as a new move
        self.player_moves.append((row-1, col-1, tileID))
        self.player_moves_coords.append((row-1, col-1))
    
    def erase_player_moves(self):
        for move in self.player_moves:
            row, col, tileID = move
            tile_manager.player_rack.append(tileID)
            self.board[row][col] = '_'
        self.player_moves = []
        self.player_moves_coords = []
    
    def remove_tile_from_board(self, tileID):
        # remove tileID from board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == tileID:
                    self.board[i][j] = '_'
        # erase tileID from player move
        for i in range(len(self.player_moves)):
            if self.player_moves[i][2] == tileID:
                self.player_moves.remove(self.player_moves[i])
                break
    
    def get_move_coordinates(self):
        for coords in self.player_moves:
            self.player_moves_coords.append((coords[0], coords[1]))
        return self.player_moves_coords

    def display(self):
        for row in self.board:
            print(' '.join(cell[0] for cell in row))

board_manager = BoardManager()
word_manager = WordManager()
tile_manager = TileManager()

# Only run code when imported as script, not a module
if __name__ == '__main__':
    app.run(debug=True)

# DID: "Fix issue with intercept function check."

# TODO: Add valid words to existing words dictionary
# TODO: Add points functionality. Bonus squares, etc.
# TODO: Make header text unselectable
# TODO: Update hiscore if player passes it.
# TODO: End game when timer runs out
# TODO: Fix aesthetics of ingame buttons
# TODO: Add a way to exit the game
# TODO: Make drag and drop smoother. Try to remove copy.
# TODO: Add sound effects
# TODO: Fix loading lag of image in main menu.

# lsof -i :5000
# kill -9 {num}