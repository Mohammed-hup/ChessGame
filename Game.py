# Constants
EMPTY = "-"
AI_PLAYER = "AI"
HUMAN_PLAYER = "Human"
# Evaluation function to assign a score to a given chess position
def evaluate_position(board):
    # Define the piece values
    piece_values = {
        "P": 1,  # Pawn
        "N": 3,  # Knight
        "B": 3,  # Bishop
        "R": 5,  # Rook
        "Q": 9,  # Queen
        "K": 0,  # King (not considered for material balance)
        "p": -1,  # Black Pawn
        "n": -3,  # Black Knight
        "b": -3,  # Black Bishop
        "r": -5,  # Black Rook
        "q": -9,  # Black Queen
        "k": 0  # Black King (not considered for material balance)
    }

    # Compute the material balance for each player
    ai_score = 0
    human_score = 0
    for row in board:
        for piece in row:
            if piece != EMPTY:
                if piece.isupper():
                    ai_score += piece_values[piece]
                else:
                    human_score += piece_values[piece]

    # Return the difference in material balance
    return ai_score - human_score


# Function to check if the game is over
def game_over(board):
    # Check for checkmate or stalemate
    if is_checkmate(board, AI_PLAYER) or is_checkmate(board, HUMAN_PLAYER):
        return True
    if is_stalemate(board):
        return True
    return False


# Function to check if the game is in a stalemate
def is_stalemate(board):
    # Check if the current player has any legal moves
    current_player = AI_PLAYER if current_player == HUMAN_PLAYER else HUMAN_PLAYER
    for move in get_possible_moves(board):
        make_move(board, move)
        if not is_check(board, current_player):
            undo_move(board, move)
            return False
        undo_move(board, move)

    return True


# Function to check if the game is in checkmate for the given player

def is_checkmate(board, player):
    # Check if the player's king is in check
    if is_check(board, player):
        # Iterate through all possible moves for the player
        for move in get_possible_moves(board):
            make_move(board, move)
            if not is_check(board, player):
                # The player has a legal move, not in checkmate
                undo_move(board, move)
                return False
            undo_move(board, move)

        # The player has no legal moves, in checkmate
        return True

    # The player's king is not in check, not in checkmate
    return False

# Function to check if the player's king is in check
def is_check(board, player):
    # Find the position of the player's king
    king_position = find_king(board, player)

    # Check if any opponent's piece can attack the king's position
    opponent = HUMAN_PLAYER if player == AI_PLAYER else AI_PLAYER
    for move in get_possible_moves(board):
        if move[0].islower() and move[0].isalpha() and move[0].lower() != "k":
            if move[3:] == king_position:
                return True

    return False

# Helper function to find the position of the player's king
def find_king(board, player):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col].lower() == "k" and (player == AI_PLAYER and board[row][col].isupper() or player == HUMAN_PLAYER and board[row][col].islower()):
                return f"{row}{col}"

# Function to get all possible moves for the current player
def get_possible_moves(board):
    possible_moves = []

    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row][col]
            if piece != EMPTY and piece.isupper():
                moves = generate_moves(board, piece, row, col)
                possible_moves.extend(moves)

    return possible_moves

# Helper function to generate moves for a specific piece at a given position
def generate_moves(board, piece, row, col):
    moves = []

    if piece.lower() == "p":
        moves.extend(get_pawn_moves(board, piece, row, col))
    elif piece.lower() == "r":
        moves.extend(get_rook_moves(board, piece, row, col))
    elif piece.lower() == "n":
        moves.extend(get_knight_moves(board, piece, row, col))
    elif piece.lower() == "b":
        moves.extend(get_bishop_moves(board, piece, row, col))
    elif piece.lower() == "q":
        moves.extend(get_queen_moves(board, piece, row, col))
    elif piece.lower() == "k":
        moves.extend(get_king_moves(board, piece, row, col))

    return moves

def get_pawn_moves(board, piece, row, col):
    moves = []
    player = HUMAN_PLAYER if piece.islower() else AI_PLAYER
    direction = -1 if player == HUMAN_PLAYER else 1

    # Move one square forward
    new_row = row + direction
    if is_valid_square(new_row, col) and board[new_row][col] == EMPTY:
        moves.append((piece, row, col, new_row, col))

    # Move two squares forward on the first move
    if ((player == HUMAN_PLAYER and row == 6) or (player == AI_PLAYER and row == 1)) and board[new_row][col] == EMPTY and board[new_row + direction][col] == EMPTY:
        moves.append((piece, row, col, new_row + direction, col))

    # Capture diagonally
    for col_offset in [-1, 1]:
        new_col = col + col_offset
        if is_valid_square(new_row, new_col) and board[new_row][new_col] != EMPTY and board[new_row][new_col].isupper() != piece.isupper():
            moves.append((piece, row, col, new_row, new_col))

    return moves

def get_rook_moves(board, piece, row, col):
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for direction in directions:
        for i in range(1, 8):
            new_row = row + direction[0] * i
            new_col = col + direction[1] * i

            if not is_valid_square(new_row, new_col):
                break

            if board[new_row][new_col] == EMPTY:
                moves.append((piece, row, col, new_row, new_col))
            elif board[new_row][new_col].isupper() != piece.isupper():
                moves.append((piece, row, col, new_row, new_col))
                break
            else:
                break

    return moves

def get_knight_moves(board, piece, row, col):
    moves = []
    offsets = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]

    for offset in offsets:
        new_row = row + offset[0]
        new_col = col + offset[1]

        if is_valid_square(new_row, new_col):
            if board[new_row][new_col] == EMPTY or board[new_row][new_col].isupper() != piece.isupper():
                moves.append((piece, row, col, new_row, new_col))

    return moves

def get_bishop_moves(board, piece, row, col):
    moves = []
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    for direction in directions:
        for i in range(1, 8):
            new_row = row + direction[0] * i
            new_col = col + direction[1] * i

            if not is_valid_square(new_row, new_col):
                break

            if board[new_row][new_col] == EMPTY:
                moves.append((piece, row, col, new_row, new_col))
            elif board[new_row][new_col].isupper() != piece.isupper():
                moves.append((piece, row, col, new_row, new_col))
                break
            else:
                break

    return moves

def get_queen_moves(board, piece, row, col):
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    for direction in directions:
        for i in range(1, 8):
            new_row = row + direction[0] * i
            new_col = col + direction[1] * i

            if not is_valid_square(new_row, new_col):
                break

            if board[new_row][new_col] == EMPTY:
                moves.append((piece, row, col, new_row, new_col))
            elif board[new_row][new_col].isupper() != piece.isupper():
                moves.append((piece, row, col, new_row, new_col))
                break
            else:
                break

    return moves

def get_king_moves(board, piece, row, col):
    moves = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

    for direction in directions:
        new_row = row + direction[0]
        new_col = col + direction[1]

        if is_valid_square(new_row, new_col):
            if board[new_row][new_col] == EMPTY or board[new_row][new_col].isupper() != piece.isupper():
                moves.append((piece, row, col, new_row, new_col))

    return moves

def is_valid_square(row, col):
    return 0 <= row < 8 and 0 <= col < 8


# Function to make a move on the board
def make_move(board, move):
    piece, start_row, start_col, end_row, end_col = move
    board[start_row][start_col] = EMPTY
    board[end_row][end_col] = piece

# Function to undo a move on the board
def undo_move(board, move):
    piece, start_row, start_col, end_row, end_col = move
    board[start_row][start_col] = piece
    board[end_row][end_col] = EMPTY

# Function to switch players
def switch_players(current_player):
    if current_player == AI_PLAYER:
        return HUMAN_PLAYER
    else:
        return AI_PLAYER

# Function to print the board
def print_board(board):
    for row in board:
        print(" ".join(row))

# Initialize the board
board = [
    ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["r", "n", "b", "q", "k", "b", "n", "r"]
]

# Variables
current_player = AI_PLAYER
depth = 3

# Minimax algorithm with Alpha-Beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_position(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in get_possible_moves(board):
            make_move(board, move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            undo_move(board, move)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_possible_moves(board):
            make_move(board, move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            undo_move(board, move)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Alpha-Beta pruning wrapper function
def alpha_beta_pruning(board, depth):
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in get_possible_moves(board):
        make_move(board, move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        undo_move(board, move)
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
    return best_move

# Game loop
while not game_over(board):
    print_board(board)
    print("Current player:", current_player)
    if current_player == AI_PLAYER:
        move = alpha_beta_pruning(board, depth)
        make_move(board, move)
        print("AI moves:", move)
    else:
        # Human player's turn, get their move and update the board
        print("Enter your move (piece, start row, start col, end row, end col):")
        move_input = input().split()
        move = (move_input[0], int(move_input[1]), int(move_input[2]), int(move_input[3]), int(move_input[4]))
        make_move(board, move)

    current_player = switch_players(current_player)

# Game is over
print_board(board)
print("Game over!")
