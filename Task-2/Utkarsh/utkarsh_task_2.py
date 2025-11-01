import math
import time

def print_board(board):
    print()
    print(f"{board[0]} | {board[1]} | {board[2]}        1 | 2 | 3")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}        4 | 5 | 6")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}        7 | 8 | 9")
    print()

def check_winner(board, player):
    win_combos = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for combo in win_combos:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_draw(board):
    return ' ' not in board

def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

def minimax(board, depth, is_maximizing):
    if check_winner(board, 'O'):
        return 1    
    if check_winner(board, 'X'):
        return -1     
    if is_draw(board):
        return 0     

    if is_maximizing:
        best_score = -math.inf
        for i in available_moves(board):
            board[i] = 'O'
            score = minimax(board, depth + 1, False)
            board[i] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in available_moves(board):
            board[i] = 'X'
            score = minimax(board, depth + 1, True)
            board[i] = ' '
            best_score = min(score, best_score)
        return best_score

def ai_move(board):
    best_score = -math.inf
    best_move = None

    for i in available_moves(board):
        board[i] = 'O'
        score = minimax(board, 0, False)
        board[i] = ' '
        if score > best_score:
            best_score = score
            best_move = i

    board[best_move] = 'O'

def player_move(board):
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if move in range(9) and board[move] == ' ':
                board[move] = 'X'
                break
            else:
                print("Invalid move! Try again.")
        except ValueError:
            print("Please enter a number between 1 and 9.")

def play_game():
    board = [' '] * 9
    print("\n=== Tic Tac Toe (Human vs Unbeatable AI) ===")
    print_board(board)

    while True:
        player_move(board)
        print_board(board)
        if check_winner(board, 'X'):
            print("You win! (That’s rare!)")
            return "Player"
        if is_draw(board):
            print("It's a draw!")
            return "Draw"

        print("AI is thinking...")
        time.sleep(1)
        ai_move(board)
        print_board(board)
        if check_winner(board, 'O'):
            print("AI wins!")
            return "AI"
        if is_draw(board):
            print("It's a draw!")
            return "Draw"

def main():
    player_wins = 0
    ai_wins = 0
    draws = 0

    while True:
        result = play_game()

        if result == "Player":
            player_wins += 1
        elif result == "AI":
            ai_wins += 1
        else:
            draws += 1

        print("\nCurrent Scoreboard")
        print(f"You: {player_wins}   |   AI: {ai_wins}   |   Draws: {draws}")

        again = input("\nPlay again? (y/n): ").lower()
        if again != 'y':
            print("\nFinal Scoreboard:")
            print(f"You: {player_wins}   |   AI: {ai_wins}   |   Draws: {draws}")
            print("\nThanks for playing!")
            break

if _name_ == "_main_":
    main()
