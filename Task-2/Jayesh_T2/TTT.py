import math

# Numpad-style mapping (1 bottom-left → 9 top-right)
NUMPAD_TO_INDEX = {
    1: 6, 2: 7, 3: 8,
    4: 3, 5: 4, 6: 5,
    7: 0, 8: 1, 9: 2
}

def draw_board(board):
    """Prints the board with numpad numbers for empty cells."""
    def cell_repr(i):
        if board[i] == ' ':
            for k, v in NUMPAD_TO_INDEX.items():
                if v == i:
                    return str(k)
        return board[i]

    print(f" {cell_repr(0)} | {cell_repr(1)} | {cell_repr(2)} ")
    print("---+---+---")
    print(f" {cell_repr(3)} | {cell_repr(4)} | {cell_repr(5)} ")
    print("---+---+---")
    print(f" {cell_repr(6)} | {cell_repr(7)} | {cell_repr(8)} ")

def is_winner(board, mark):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    return any(board[a]==mark and board[b]==mark and board[c]==mark for (a,b,c) in wins)

def is_board_full(board):
    return ' ' not in board

def evaluate(board, ai_mark, human_mark):
    if is_winner(board, ai_mark):
        return 1
    elif is_winner(board, human_mark):
        return -1
    return 0

def minimax(board, depth, is_maximizing, ai_mark, human_mark):
    score = evaluate(board, ai_mark, human_mark)
    if score != 0:
        return score
    if is_board_full(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = ai_mark
                best = max(best, minimax(board, depth + 1, False, ai_mark, human_mark))
                board[i] = ' '
        return best
    else:
        best = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = human_mark
                best = min(best, minimax(board, depth + 1, True, ai_mark, human_mark))
                board[i] = ' '
        return best

def best_move(board, ai_mark, human_mark):
    best_val = -math.inf
    best_idx = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = ai_mark
            move_val = minimax(board, 0, False, ai_mark, human_mark)
            board[i] = ' '
            if move_val > best_val:
                best_val = move_val
                best_idx = i
    return best_idx

def get_human_move(board):
    while True:
        raw = input("Enter your move (numpad 1-9): ").strip()
        if not raw.isdigit():
            print("Please enter a number 1–9.")
            continue
        key = int(raw)
        if key < 1 or key > 9:
            print("Number must be 1–9.")
            continue
        idx = NUMPAD_TO_INDEX[key]
        if board[idx] != ' ':
            print("That cell is already taken.")
            continue
        return idx

def tic_tac_toe():
    print("Welcome to Unbeatable Tic Tac Toe (AI uses Minimax)!")
    print("Layout uses numpad keys (1 = bottom-left, 9 = top-right).")
    board = [' ' for _ in range(9)]
    human_mark, ai_mark = 'X', 'O'

    # Choose who goes first
    first = input("Who goes first? (H)uman or (A)I [default H]: ").strip().lower() or 'h'
    current = 'Human' if first.startswith('h') else 'AI'

    draw_board(board)
    while True:
        if current == 'Human':
            move = get_human_move(board)
            board[move] = human_mark
            draw_board(board)
            if is_winner(board, human_mark):
                print("🎉 You win! (That’s rare!)")
                break
            if is_board_full(board):
                print("It's a draw.")
                break
            current = 'AI'
        else:
            print("AI is thinking...")
            move = best_move(board, ai_mark, human_mark)
            board[move] = ai_mark
            draw_board(board)
            if is_winner(board, ai_mark):
                print("AI wins! You can’t beat perfection 😎")
                break
            if is_board_full(board):
                print("It's a draw.")
                break
            current = 'Human'

if __name__ == "__main__":
    tic_tac_toe()
