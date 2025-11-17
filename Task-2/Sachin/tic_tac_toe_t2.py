board = [" " for _ in range(9)]

def show_board():
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(mark):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] == mark:
            return True
    return False

def board_full():
    return " " not in board

def player_move():
    while True:
        move = input("Enter your move (1-9): ")
        if move.isdigit():
            move = int(move) - 1
            if move in range(9) and board[move] == " ":
                board[move] = "X"
                break
            else:
                print("Cell Occupied. Try again.")
        else:
            print("Enter a valid number 1-9.")

def ai_move():
    print("AI is thinking...\n")

  for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            if check_winner("O"):
                return
            board[i] = " "
    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if check_winner("X"):
                board[i] = "O"
                return
            board[i] = " "
    for pos in [4, 0, 2, 6, 8, 1, 3, 5, 7]:
        if board[pos] == " ":
            board[pos] = "O"
            return
def play():
    print("Tic Tac Toe - Human (X) vs AI (O)")
    show_board()

    while True:
        player_move()
        show_board()
        if check_winner("X"):
            print("🎉 You win!")
            break
        if board_full():
            print("It's a draw!")
            break

        ai_move()
        show_board()
        if check_winner("O"):
            print("💻 AI wins!")
            break
        if board_full():
            print("It's a draw!")
            break
play()
