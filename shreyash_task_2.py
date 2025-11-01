import math

# Initialize board
board = [" " for _ in range(9)]

def print_board():
    print("\n")
    for i in range(3):
        print(" " + board[3*i] + " | " + board[3*i + 1] + " | " + board[3*i + 2])
        if i < 2:
            print("---+---+---")
    print("\n")

def available_moves():
    return [i for i, spot in enumerate(board) if spot == " "]

def is_winner(player):
    win_positions = [
        [0,1,2], [3,4,5], [6,7,8], # rows
        [0,3,6], [1,4,7], [2,5,8], # cols
        [0,4,8], [2,4,6]           # diagonals
    ]
    return any(all(board[pos] == player for pos in combo) for combo in win_positions)

def is_draw():
    return " " not in board

# Minimax AI
def minimax(is_maximizing):
    if is_winner("O"):
        return 1
    if is_winner("X"):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best = -math.inf
        for move in available_moves():
            board[move] = "O"
            score = minimax(False)
            board[move] = " "
            best = max(score, best)
        return best
    else:
        best = math.inf
        for move in available_moves():
            board[move] = "X"
            score = minimax(True)
            board[move] = " "
            best = min(score, best)
        return best

def ai_move():
    best_score = -math.inf
    move = None
    for i in available_moves():
        board[i] = "O"
        score = minimax(False)
        board[i] = " "
        if score > best_score:
            best_score = score
            move = i
    board[move] = "O"

def player_move():
    while True:
        try:
            move = int(input("Enter a move (1-9): ")) - 1
            if move in available_moves():
                board[move] = "X"
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Enter a valid number!")

def play_game():
    print("Welcome to Tic Tac Toe!")
    print("You are X. AI is O.")
    print_board()

    while True:
        player_move()
        print_board()
        if is_winner("X"):
            print("🎉 You win!")
            break
        if is_draw():
            print("🤝 It's a draw!")
            break

        print("AI is thinking...")
        ai_move()
        print_board()

        if is_winner("O"):
            print("💻 AI wins!")
            break
        if is_draw():
            print("🤝 It's a draw!")
            break

if __name__ == "__main__":
    play_game()
