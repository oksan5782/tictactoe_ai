"""
Tic Tac Toe Game
"""
import copy
import time


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Calculate presence of every player on the board
    count_x = 0
    count_o = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == "X":
                count_x += 1
            elif board[i][j] == "O":
                count_o += 1

    # Return player who's turn is now to move
    if count_x == count_o:
        return "X"
    return "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Create a set of tuples
    available_actions = set()

    # Iterate over the board to add empty cells to a set
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available_actions.add((i, j))

    # Return a set of all the possible actions
    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # If board cell already filled
    if board[i][j] != EMPTY:
        raise ValueError("Action cannot be performed on a non-empty cell")
    
    # Find out which player's turn it is
    move = player(board)

    # Make a deepcopy of the board to apply action
    copied_board = copy.deepcopy(board)

    # Perform an action on a copied board
    copied_board[i][j] = move

    return copied_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check rows
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        
        # Check columns
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    
    # If no winner with this state
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or all_slots_taken(board):
        return True
    return False   


def all_slots_taken(board):
    """
    Returns True is all slots are places, False otherwise.
    """
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Get a winner if there is one
    score = winner(board)
    if score:
        if score == "X":
            return 1
        else:
            return -1
        
    # Tie with no winner
    if all_slots_taken(board):
        return 0
    return None


def minimax(board):
    """
    Returns the optimal action for the current player on the board with Alpha-beta pruning optimization
    """

    # If board is terminal, return None
    if terminal(board):
        return None
    
    # Get current state 
    state = player(board)

    # Get all available actions
    available_actions = actions(board)
    
    # Find the highest-scored action considering min_player's move
    if state == "X":
        # Initialize alpha to negative infinity
        alpha = float('-inf')

        # Create a tuple with a game score, alpha, beta and move that leads to this score
        processed_results = ((min_value(result(board, a), alpha, float('inf')), a) for a in available_actions)

        # Find the tuple with the highest result 
        best_action = max(processed_results, key=lambda x: x[0])

        # Return selected tuple
        return best_action[1]
    
    # Find lowest-scored action considering max_player's move
    if state == "O":

        # Initialize beta to positive infinity
        beta = float('inf')
        
        # Create a tuple with a game score, alpha, beta and move that leads to this score
        processed_results = ((max_value(result(board, a), float('-inf'), beta), a) for a in available_actions)

        # Find the tuple with the lowest result using min
        best_action = min(processed_results, key=lambda x: x[0])

        # Return selected tuple
        return best_action[1]


def max_value(board, alpha, beta):
    """
    Takes a state and returns max value of it
    """
    # Check if the game is over
    if terminal(board):
        return utility(board)

    # Get the best possible result
    v = float('-inf')
    available_action = actions(board)
    for action in available_action:
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if beta <= alpha:
            break  # Beta cut-off
    return v

    
def min_value(board, alpha, beta):
    """
    Takes a state and returns min value of it
    """
    # Check if the game is over
    if terminal(board):
        return utility(board)

    # Get the best possible result
    v = float('inf')
    available_action = actions(board)
    for action in available_action:
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if beta <= alpha:
            break  # Alpha cut-off
    return v


def print_board(board):
    """
    Print out the board with spaces and delimiters.
    """
    for row in board:
        formatted_line = "| " + " | ".join(" " if c is None else c for c in row) + " |"
        print(formatted_line)


def play_tic_tac_toe():
    """
    Implementation of the game
    """

    # Draw an empty board
    board = initial_state()
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    # Get user player
    user_symbol = None
    while user_symbol not in ['X', 'O']:
        user_symbol = input("Choose your symbol (X or O): ").upper()

    while True:
        if user_symbol == 'X':

            valid_move = False
            available_moves = actions(board)

            # Keep prompting user for a move until its a valid one
            while not valid_move:
                position = input(user_symbol + "\'s turn. Input move (0-8):")
                row = None
                col = None
                try:
                    row = int(position) // 3
                    col = int(position) % 3
                    if (row, col) not in available_moves:
                        raise ValueError
                    valid_move = True
                except ValueError:
                    print("Invalid move. Try again.")

            # Make a move
            board[row][col] = 'X'
        else:
            # AI's move
            print("AI's move:")
            ai_row, ai_col = minimax(board)
            board[ai_row][ai_col] = 'O'
            time.sleep(0.5)
        print_board(board)

        # Check if the game has ended
        if terminal(board):
            if all_slots_taken(board):
                print("It's a tie!")
            else:
                win = winner(board)
                print(f" {win} wins!")
            break
        
        # Switch turns
        user_symbol = 'X' if user_symbol == 'O' else 'O'


if __name__ == "__main__":
    play_tic_tac_toe()