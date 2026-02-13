import copy


class Orientation:
    """
        clasas Orientation: performs orientation-related opreations

        Functions:
        get_offsets(x, y, direction): returns the orientation-adjusted coordinates for the L piece

    """

    # all possible orientations for the L piece
    orientations = ["N", "E", "S", "W", "FN", "FE", "FS", "FW"]

    # coordinate offsets for each orientation
    offsets = {
        "N": [(0, 0), (0, -1), (-1, 0), (-2, 0)],
        "E": [(0, 0), (1, 0), (0, -1), (0, -2)],
        "S": [(0, 0), (0, 1), (1, 0), (2, 0)],
        "W": [(0, 0), (-1, 0), (0, 1), (0, 2)],
        "FN": [(0, 0), (0, -1), (1, 0), (2, 0)],
        "FE": [(0, 0), (1, 0), (0, 1), (0, 2)],
        "FS": [(0, 0), (0, 1), (-1, 0), (-2, 0)],
        "FW": [(0, 0), (-1, 0), (0, -1), (0, -2)]
    }


    # get orientation-adjusted coordinates
    @staticmethod
    def get_offsets(x, y, direction):

        # check if the direction is valid
        if direction not in Orientation.offsets:
            return []
        
        return [(x + dx, y + dy) for dx, dy in Orientation.offsets[direction]]
        

class Board:

    """
        Board: represents the game board
        
        Attributes:
            - size: the size of the board (default 4)
            - game_state: the current state of the game board
            - L_pieces: dictionary mapping to L_piece objects
            - neutral_pieces: dictionary mapping to Neutral_Piece objects
            - neutral_positions: list of neutral piece positions
            
        Functions:
            init_board(): initializes the game board
            init_game_state(): initializes the game state
            update_grid(): updates the grid with the current game state
            clear_L_piece(self, player_label): removes the given player's L piece from the board
            clear_neutral_piece (self, neutral_coordinate): removes the neutral piece from the board
            move_neutral_piece (self, old_coordinate, new_coordinate): updates the neutral piece's attribute coordinate

    """

    def __init__(self, size = 4):

        self.size = size
        self.game_state = []
        self.L_pieces = {}
        self.neutral_pieces = {}
        self.neutral_positions = []


    def init_board(self):
        """
        initializes the game board with a 4x4 grid.

        """

        # _ is a placeholder for the index; used when we don't need the index value
        self.game_state = [["." for _ in range(self.size)] for _ in range(self.size)]


    def init_game_state(self, L1_coordinate = (1,3), L1_orientation = "E", L2_coordinate = (2, 0), L2_orientation = "W", neutral_positions = [(0,0), (3,3)]):
        """
        initializes the game state with the given positions and orientations; if none are given, defaults are set

        """

        # initialize the L pieces
        self.L_pieces["L1"] = L_Piece(L1_coordinate, L1_orientation, "L1")
        self.L_pieces["L2"] = L_Piece(L2_coordinate, L2_orientation, "L2")

        # initialize the neutral pieces
        self.neutral_positions = neutral_positions
        self.neutral_pieces ["N1"] = Neutral_Piece (neutral_positions [0], "N1")
        self.neutral_pieces ["N2"] = Neutral_Piece (neutral_positions [1], "N2")

        # update the grid
        self.update_grid()


    def update_grid(self):
        """
        updates the grid with the current game state

        """

        # Place L pieces
        for piece in self.L_pieces.values():
            piece.place_on_board(self.game_state)

        # Place neutral pieces
        for piece in self.neutral_pieces.values():
            piece.place_on_board(self.game_state)


    def clear_L_piece(self, player_label):
        """
        removes the given player's L piece from the board.

        """
        
        for i in range (4):
            for j in range(4):

                # if position contains the player's L piece, clear it
                if self.game_state[i][j] == player_label:
                    self.game_state[i][j] = "."


    def clear_neutral_piece (self, neutral_coordinate):
        """
        removes the neutral piece from the board.

        """

        # clear the position of the neutral piece
        x, y = neutral_coordinate
        self.game_state[y][x] = "."
    

    def move_neutral_piece (self, old_coordinate, new_coordinate):
        """
        update the neutral piece's attribute coordinate

        """

        # loop through the neutral pieces to find the one to move and update its coordinate
        for piece in self.neutral_pieces.values():
            if piece.coordinate == old_coordinate:
                piece.coordinate = new_coordinate


    def get_legal_moves(self, L_piece):
        """
        returns all the legal moves of a given L piece

        """

        def is_within_grid(x, y):
            """ helper function to check if a position is within the grid """
            return 0 <= x < self.size and 0 <= y < self.size
        

        def simulate_clear_L_piece (sim_state, player_label):
            """ helpr function to clear the L piece from the simulated state """
            for i in range(len(sim_state)):
                for j in range(len(sim_state[i])):
                    if sim_state[i][j] == player_label:
                        sim_state[i][j] = "."


        def simulate_place_L_piece (sim_state, sim_move, player_label):
            """ helper function to place the L piece in the simulated state """

            # unpack the move to simulate
            (x, y), orientation = sim_move
            
            # get its offsets
            sim_L_positions = Orientation.get_offsets (x, y, orientation)

            # place the L piece in the simulated state
            for x, y in sim_L_positions:
                if 0 <= y < len(sim_state) and 0 <= x < len(sim_state[0]):
                    sim_state[y][x] = player_label
                else:
                    print(f"Error: Position ({x}, {y}) is out of bounds for simulated L_Piece {player_label}.")
        

        legal_moves = []
        legal_L_moves = []
        curr_game_state = self.game_state

        # get current L piece positions
        curr_positions = L_piece.get_current_positions()

        # get all possible L moves
        for x in range(self.size):
            for y in range(self.size):
                for orientation in Orientation.orientations:

                    positions = Orientation.get_offsets (x, y, orientation)

                    # add all valid moves (conditions: within grid, unoccupied, and at least one new position)
                    if (
                        all(is_within_grid(L_x, L_y) for L_x, L_y in positions) and
                        all((curr_game_state[L_y][L_x] == "." or curr_game_state[L_y][L_x] == L_piece.label) for L_x, L_y in positions) and
                        any(pos not in curr_positions for pos in positions)
                    ):

                        # add the move to the list of legal L moves
                        legal_L_moves.append( ((x, y) , orientation) )


        # ------- simulate the state after the move (in order to get the corresponding legal neutral moves) -------

        for L_move in legal_L_moves:

            # copy the game state to simulate the move
            simulated_state = [row[:] for row in curr_game_state]

            # clear the L piece from the simulated state
            simulate_clear_L_piece (simulated_state, L_piece.label)

            # place the L piece in the simulated state
            simulate_place_L_piece (simulated_state, L_move, L_piece.label)

            # get the positions of neutral and empty squares in the simulated state
            sim_neutral_positions = [(x, y) for y in range(4) for x in range(4) if simulated_state[y][x] == "N"]
            sim_empty_positions = [(x, y) for y in range(4) for x in range(4) if simulated_state[y][x] == "."]

            legal_neutral_moves = []

            # get all the legal neutral moves
            for neutral_pos in sim_neutral_positions:
                for empty_pos in sim_empty_positions:
                    legal_neutral_moves.append ((neutral_pos, empty_pos))

            # add option to not move the neutral piece
            legal_neutral_moves.append (None)

            # assemble the legal moves (combine L move with neutral move)
            for neutral_move in legal_neutral_moves:
                legal_moves.append ((L_move, neutral_move))


        # legal_moves element format = ( L_move , neutral_move )
        # L_move format         =   ( (L_x, L_y) , L_orientation)
        # neutral_move format   =   ( (old_x, old_y), (new_x, new_y) )


        return legal_moves


    def generate_successor (self, move, L_label):
        """
        returns the successor board after the given move is executed

        """

        # create a deep copy of the current board
        successor_board = copy.deepcopy(self)

        # clear the current player's L piece from the successor board
        for i in range(4):
            for j in range(4):
                if successor_board.game_state[i][j] == L_label:
                    successor_board.game_state[i][j] = "."

        # unpack the move
        L_move, neutral_move = move

        # unpack the L move
        new_L_coordinate, new_orientation = L_move

        # get L piece positions
        L_positions = Orientation.get_offsets(new_L_coordinate[0], new_L_coordinate[1], new_orientation)

        # place the L piece on the successor board
        for i in range (4):
            for j in range (4):
                if (i, j) in L_positions:
                    successor_board.game_state[j][i] = L_label
        

        if neutral_move:

            # unpack the neutral move
            old_neutral_coordinate, new_neutral_coordinate = neutral_move
            new_x, new_y = new_neutral_coordinate

            # clear the old neutral piece from the board
            for i in range(4):
                for j in range(4):
                    if (i, j) == old_neutral_coordinate:
                        successor_board.game_state[j][i] = "."

            # place the neutral piece on the successor board
            successor_board.game_state [new_y][new_x] = "N"
        
        # return the successor board
        return successor_board

    
    def is_terminal (self):
        """
        checks is the game is over by checking if either player has no legal moves

        """

        # check if the game is over by checking if either player has no legal moves
        player1_legal_moves = self.get_legal_moves (self.L_pieces["L1"])
        player2_legal_moves = self.get_legal_moves (self.L_pieces["L2"])

        return len(player1_legal_moves) == 0 or len(player2_legal_moves) == 0


    def display_board(self):
        """
        displays the current game board

        """

        col_widths = [max(len(str(self.game_state[row][col])) for row in range(len(self.game_state))) for col in range(len(self.game_state[0]))]
        for row in self.game_state:
            print("   ".join(str(cell).center(col_widths[col]) for col, cell in enumerate(row)))
        print()


class L_Piece:
    """
    L_Piece: represents an L piece on the board

    Attributes:
        - coordinate: the current position of the L piece
        - orientation: the current orientation of the L piece
        - label: the label of the L piece

    Functions:
        get_current_positions(): returns the current positions of the L piece
        place_on_board(game_state): places the L piece on the game board
        move(new_coordinate, new_orientation): updates the L piece's position and orientation
    """

    def __init__(self, coordinate, orientation, label):
        self.coordinate = coordinate
        self.orientation = orientation
        self.label = label


    def get_current_positions(self):
        # define the offsets from coordinate for each orientation
        x, y = self.coordinate
        return Orientation.get_offsets(x, y, self.orientation)


    def place_on_board(self, game_state):

        # get the L piece positions
        positions = Orientation.get_offsets(self.coordinate[0], self.coordinate[1], self.orientation)

        # place the L piece on the board
        for x, y in positions:
            if 0 <= y < len(game_state) and 0 <= x < len(game_state[0]):  # Check for bounds
                game_state[y][x] = self.label
            else:
                print(f"Error: Position ({x}, {y}) is out of bounds for L_Piece {self.label}.")


    def move(self, new_coordinate, new_orientation):
        # update the L piece's position and orientation
        self.coordinate = new_coordinate
        self.orientation = new_orientation



class Neutral_Piece:
    """
    Neutral_Piece: represents a neutral piece on the board

    Attributes:
        - coordinate: the current position of the neutral piece
        - label: the label of the neutral piece

    Functions:
        place_on_board(game_state): places the neutral piece on the game board
    """

    def __init__(self, coordinate, label):
        self.coordinate = coordinate
        self.label = label


    def place_on_board(self, game_state):
        # place the neutral piece on the board
        x, y = self.coordinate
        game_state[y][x] = "N"
    

class Player:

    def __init__(self, name, L_piece):
        self.name = name
        self.L_piece = L_piece
    

    def make_move (self, board):
        """
        Executes a move for the player by interacting with the board.

        """
        print(f"{self.name}'s turn to make a move'")

        # Display the current board before the move
        board.display_board()

        # check that the move is valid
        legal_moves = board.get_legal_moves (self.L_piece)
        legal_L_moves = [move[0] for move in legal_moves]
        
        # get user input for the L piece move and validate until it is valid
        while True:
            try:
                # get user input for the L piece move
                while True:
                    try:
                        new_x = input("Enter the new x coordinate for your L piece: ").strip()
                        if new_x == "":
                            raise ValueError ("empty input")
                        new_x = int(new_x)
                        break
                    except ValueError as e:
                        print (f"Input Error: {e}. Please enter a valid x coordinate.")
                
                while True:
                    try:
                        new_y = input ("Enter the new y coordinate for your L piece: ").strip()
                        if new_y == "":
                            raise ValueError ("empty input")
                        new_y = int(new_y)
                        break
                    except ValueError as e:
                        print (f"Input Error: {e}. Please enter a valid y coordinate.")

                while True:
                    try:
                        new_orientation = input("Enter the new orientation for your L piece (N, E, S, W; FN = Flipped North): ").strip().upper()
                        if new_orientation not in Orientation.orientations:
                            raise ValueError
                        break
                    except ValueError as e:
                        print (f"Invalid orientation input: {e}. Please enter a valid move.")


                # validate the inputted move
                if ( (new_x, new_y), new_orientation) not in legal_L_moves:
                    
                    raise ValueError ((new_x, new_y), new_orientation)

                break

            except ValueError as e:
                print (f"Invalid move: {e}. Please try another move.")


        # Clear the player's L piece from the board
        board.clear_L_piece(self.L_piece.label)

        # Update the L piece
        self.L_piece.move((new_x, new_y), new_orientation)

        # Place the L piece on the board
        self.L_piece.place_on_board(board.game_state)

        # display board after L piece move
        board.display_board()

        # get legal moves for the neutral piece after the L piece move
        legal_neutral_moves = [(move[1]) for move in legal_moves if move[0] == ((new_x, new_y), new_orientation)]
        move_neutral = ""


        while True:
            try:
                # validate user input for option to move a neutral piece and neutral piece move
                while True:
                    try:
                        move_neutral = input("Move a neutral piece? (yes/no): ").strip().lower()
                        if move_neutral not in ["yes", "no"]:
                            raise ValueError

                        break

                    except ValueError as e:
                        print (f"Invalid input: {e}. Please enter 'yes' or 'no'.")


                if move_neutral == "yes":

                    # validate the inputted neutral piece move
                    while True:
                        try:
                            old_neutral_x = input("x coordinate of the neutral piece to move: ").strip()

                            if old_neutral_x == "":
                                raise ValueError ("empty input")
                            
                            old_neutral_x = int (old_neutral_x)

                            break

                        except ValueError as e:
                            print (f"Invalid input: {e}.")

                    while True:
                        try:
                            old_neutral_y = input("y coordinate of the neutral piece to move: ").strip()

                            if old_neutral_y == "":
                                raise ValueError ("empty input")
                            
                            old_neutral_y = int (old_neutral_y)

                            break

                        except ValueError as e:
                            print (f"Invalid input: {e}.")

                    while True:
                        try:
                            new_neutral_x = input("new x coordinate for the neutral piece: ").strip()

                            if new_neutral_x == "":
                                raise ValueError ("empty input")
                            
                            new_neutral_x = int (new_neutral_x)

                            break

                        except ValueError as e:
                            print (f"Invalid input: {e}.")

                    while True:
                        try:
                            new_neutral_y = input("new y coordinate for the neutral piece: ").strip()

                            if new_neutral_y == "":
                                raise ValueError ("empty input")
                            
                            new_neutral_y = int (new_neutral_y)

                            break

                        except ValueError as e:
                            print (f"Invalid input: {e}.")


                # check if the move is legal
                if move_neutral == "yes" and ((old_neutral_x, old_neutral_y), (new_neutral_x, new_neutral_y)) not in legal_neutral_moves:
                    raise ValueError ((old_neutral_x, old_neutral_y), (new_neutral_x, new_neutral_y))

                break

            except ValueError as e:
                print (f"Invalid move: {e}. Please try another move.")

        
        if move_neutral == "yes":

            # clear the selected neutral piece from the board
            board.clear_neutral_piece ( (old_neutral_x, old_neutral_y) )

            # move the selected neutral piece. find it by accessing the dictionary neutral_pieces in board
            board.move_neutral_piece ( (old_neutral_x,old_neutral_y), (new_neutral_x, new_neutral_y))

        # Update and display the board after the move
        board.update_grid()
        print("Updated board after move:")
        board.display_board()


class MinimaxAgent:
    """
    MinimaxAgent: represents an AI agent that uses the minimax algorithm to make moves

    Attributes:
        - name: the name of the AI agent
        - L_piece: the L piece controlled by the AI agent
        - depth: the depth to search in the minimax tree

    Functions:
        evaluation_function(L_piece): evaluates game state to return a score
        get_action(board): returns the minimax action from the current game state
        find_max_score(board, depth, player_L_labels, alpha, beta): returns the maximum score for the current player
        find_min_score(board, depth, player_L_labels, alpha, beta): returns the minimum score for the opponent player
    """

    def __init__(self, name, L_piece, depth):
        
        self.name = name
        self.L_piece = L_piece
        self.depth = depth


    def evaluation_function (self, L_piece):
        """
        evaluates game state to return a score
        """
        # evaluate game state based on number of middle 4 squares occupied by an L piece
        middle_squares = [(1, 1), (1, 2), (2, 1), (2, 2)]
        L_piece_positions = L_piece.get_current_positions()
        return sum(1 for x, y in middle_squares if (x, y) in L_piece_positions)


    def get_action(self, board):
        """
        returns the minimax action from the current game state
        """

        alpha = float('-inf')
        beta = float('inf')
        
        # which L piece is the max player
        max_player_L_piece_label = self.L_piece.label
        if max_player_L_piece_label == "L1":
            min_player_L_piece_label = "L2"
        elif max_player_L_piece_label == "L2":
            min_player_L_piece_label = "L1"

        else: 
            raise ValueError (f"invalid label: {max_player_L_piece_label}")

        # dictionary to map player labels to L piece labels
        player_L_labels = {"max": max_player_L_piece_label, "min": min_player_L_piece_label}

        # initialize list of legal moves & scores
        moves = board.get_legal_moves (self.L_piece)
        successor_boards = [board.generate_successor (move, player_L_labels["max"]) for move in moves]

        # list of scores
        scores = [self.find_min_score (board, self.depth, player_L_labels, alpha, beta) for board in successor_boards]     # list of scores for each move

        # pick action w/ max score
        best_score = max (scores)
        best_action = moves[scores.index(best_score)]

        # print(f"Scores for each move:", scores)
        # print(f"Best action chosen: {best_action}, Best score: {best_score}")

        return best_action


    def find_max_score(self, board, depth, player_L_labels, alpha, beta):
        # check if the game is over or if the depth limit is reached
        if depth == 0 or board.is_terminal():
            return self.evaluation_function(board.L_pieces[player_L_labels["max"]])

        max_score = float('-inf')

        # get the max score for each successor
        for move in board.get_legal_moves(board.L_pieces[player_L_labels["max"]]):     
            successor = board.generate_successor(move, player_L_labels["min"])
            max_score = max(max_score, self.find_min_score(successor, depth, player_L_labels, alpha, beta))

        # alpha-beta pruning
        if max_score >= beta:
            return max_score
        alpha = max(alpha, max_score)

        return max_score


    def find_min_score(self, board, depth, player_L_labels, alpha, beta):

        if depth == 0 or board.is_terminal():
            return self.evaluation_function(board.L_pieces[player_L_labels["min"]])

        min_score = float('inf')

        for action in board.get_legal_moves(board.L_pieces[player_L_labels["min"]]):       # agent_index = L_piece (object)

            successor = board.generate_successor(action, player_L_labels["min"])  # agent_index = player_name ("AI", "AI1", etc.)

            # need this for l game? this was for ghosts in pacman\
            min_score = min(min_score, self.find_max_score(successor, depth - 1, player_L_labels, alpha, beta))

        if min_score <= alpha:
            return min_score
        beta = min(beta, min_score)

        return min_score

class Game:

    def __init__(self, mode='human_vs_human', depth=0):
        
        self.mode = mode
        self.board = Board()
        self.board.init_board()
        self.board.init_game_state()
        self.current_player_index = 0
        self.players = []


        if self.mode == 'human_vs_human':
            self.players = [
                Player("player1", self.board.L_pieces["L1"]),
                Player("player2", self.board.L_pieces["L2"])
            ]
        elif self.mode == 'human_vs_ai':
            self.players = [
                Player("human", self.board.L_pieces["L1"]),
                MinimaxAgent("AI", self.board.L_pieces["L2"], depth)
            ]
        elif self.mode == 'ai_vs_ai':
            self.players = [
                MinimaxAgent("AI1", self.board.L_pieces["L1"], depth),
                MinimaxAgent("AI2", self.board.L_pieces["L2"], depth)
            ]
        else:
            raise ValueError("Invalid game mode. Choose from 'human_vs_human', 'human_vs_ai', or 'ai_vs_ai'.")


    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    # returns the current player object
    def get_current_player(self):
        return self.players[self.current_player_index]


    def play_turn (self):
        """
        Executes a turn for the current player.
        """
        current_player = self.get_current_player()

        print (f"{current_player.name}'s turn.")

        # if current player is a human, make a move
        if isinstance(current_player, Player):
            current_player.make_move (self.board)
        
        # if current player is AI, get the maximizing action and apply it
        elif isinstance(current_player, MinimaxAgent):
            action = current_player.get_action(self.board)
            self.apply_action(current_player, action)

    def apply_action(self, current_player, action):
        """
        Apply the AI's action to the board (updates L piece or neutral piece positions).
        """
        L_move, neutral_move = action

        # Clear the current player's L piece from the board
        self.board.clear_L_piece(current_player.L_piece.label)

        # Update the L piece
        current_player.L_piece.move(L_move[0], L_move[1])

        # Place the L piece on the board
        current_player.L_piece.place_on_board(self.board.game_state)

        # Optionally move a neutral piece
        if neutral_move:
            # Unpack the neutral move
            old_neutral_coordinate, new_neutral_coordinate = neutral_move
            old_neutral_x, old_neutral_y = old_neutral_coordinate
            new_neutral_x, new_neutral_y = new_neutral_coordinate


            self.board.display_board()


            # Clear the neutral piece to move from the board
            self.board.clear_neutral_piece((old_neutral_x, old_neutral_y))

            # Move the neutral piece to the new position
            self.board.move_neutral_piece((old_neutral_x, old_neutral_y), (new_neutral_x, new_neutral_y))

        # Update and display the board after the move
        self.board.update_grid()
        print("Updated board after move:")
        self.board.display_board()

        

    def is_game_over(self):
        """
        Determines if the game is over by checking if the current player has no legal moves.
        """
        current_player = self.get_current_player()
        legal_moves = self.board.get_legal_moves(current_player.L_piece)
        return len(legal_moves) == 0

    def play(self):

        while not self.is_game_over():
            self.play_turn()
            self.switch_player()

        # fix winner name
        current_player = self.get_current_player()
        print ( f"Game over! {current_player.name} wins!")

class Menu:
    @staticmethod
    def display_menu():
        print("Welcome to the L Game!")
        print("You can play in one of the following modes:")
        print("1: Human vs Human")
        print("2: Human vs AI")
        print("3: AI vs AI")

    @staticmethod
    def get_mode():
        while True:
            try:
                mode_choice = int(input("Select game mode (1, 2, or 3): ").strip())
                if mode_choice in [1, 2, 3]:
                    return mode_choice
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number (1, 2, or 3).")

if __name__ == "__main__":
    Menu.display_menu()
    mode_choice = Menu.get_mode()

    mode_mapping = {1: 'human_vs_human', 2: 'human_vs_ai', 3: 'ai_vs_ai'}
    selected_mode = mode_mapping[mode_choice]

    print(f"Starting game in mode: {selected_mode.replace('_', ' ').title()})")

    game = Game(mode=selected_mode)
    game.play()