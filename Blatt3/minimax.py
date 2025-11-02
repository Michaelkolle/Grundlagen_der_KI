def check_winner(board):
    winning_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "draw"
    return None

def print_board(board):
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print()

def get_available_moves(board):
    return [i for i in range(9) if board[i] == " "]

def minmax(board, depth, is_max):
    global nodes_minimax
    nodes_minimax += 1

    winner = check_winner(board)
    if winner == "X":
        return 1
    if winner == "O":
        return -1
    if winner == "draw":
        return 0

    if is_max:
        best = -999
        for move in get_available_moves(board):
            board[move] = "X"
            best = max(best, minmax(board, depth + 1, False))
            board[move] = " "
        return best
    else:
        best = 999
        for move in get_available_moves(board):
            board[move] = "O"
            best = min(best, minmax(board, depth + 1, True))
            board[move] = " "
        return best

def alphabeta(board, depth, alpha, beta, is_max):
    global nodes_alpha_beta
    nodes_alpha_beta += 1

    winner = check_winner(board)
    if winner == "X": return 1
    if winner == "O": return -1
    if winner == "draw": return 0

    if is_max:
        value = -999
        for move in get_available_moves(board):
            board[move] = "X"
            value = max(value, alphabeta(board, depth + 1, alpha, beta, False))
            board[move] = " "
            alpha = max(alpha, value)
            if alpha >= beta: break
        return value
    else:
        value = 999
        for move in get_available_moves(board):
            board[move] = "O"
            value = min(value, alphabeta(board, depth + 1, alpha, beta, True))
            board[move] = " "
            beta = min(beta, value)
            if alpha >= beta: break
        return value

def best_move(board, player):
    best_val = -999
    best_move = None

    for move in get_available_moves(board):
        board[move] = player
        move_val = minmax(board, 0, player == "O")  # O nach X dran
        board[move] = " "
        if move_val > best_val:
            best_val = move_val
            best_move = move
    return best_move

def best_move_ab(board, player):
    best_val = -999
    best_move = None

    for move in get_available_moves(board):
        board[move] = player
        move_val = alphabeta(board, 0, -999, 999, player == "O")
        board[move] = " "
        if move_val > best_val:
            best_val = move_val
            best_move = move
    return best_move

def minimax_simple(board, player):
    winner = check_winner(board)
    if winner == "X": return 1
    if winner == "O": return -1
    if winner == "draw": return 0

    best = -999
    for move in get_available_moves(board):
        board[move] = player
        score = -minimax_simple(board, "O" if player=="X" else "X")
        board[move] = " "
        best = max(best, score)
    return best


board = [" "] * 9

nodes_minimax = 0
nodes_alpha_beta = 0

move1 = best_move(board, "X")
nodes1 = nodes_minimax

move2 = best_move_ab(board, "X")
nodes2 = nodes_alpha_beta

print("Best move Minimax:", move1, "Nodes explored:", nodes1)
print("Best move AlphaBeta:", move2, "Nodes explored:", nodes2)
