import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Tic Tac Toe (AI)")
board = [" "] * 9
buttons = []

def check_win(b, c):
    win_pos = [(0,1,2),(3,4,5),(6,7,8),
               (0,3,6),(1,4,7),(2,5,8),
               (0,4,8),(2,4,6)]
    return any(b[a]==b[b1]==b[c1]==c for a,b1,c1 in win_pos)

def click(i):
    if board[i] == " ":
        board[i] = "X"
        buttons[i].config(text="X", state="disabled")
        if check_game(): return
        ai_move()

def ai_move():
    empty = [i for i in range(len(board)) if board[i]==" "]
    if not empty: return
    for c in ["O","X"]:
        for i in empty:
            board[i]=c
            if check_win(board,c):
                board[i]="O"
                buttons[i].config(text="O", state="disabled")
                if check_game(): return
                return
            board[i]=" "
    i = random.choice(empty)
    board[i] = "O"
    buttons[i].config(text="O", state="disabled")
    check_game()

def check_game():
    if check_win(board,"X"):
        messagebox.showinfo("Result","You Win!")
        messagebox.showinfo("Next Level","Welcome to Level 2 (5x5 Board)")
        new_level()
        return True
    elif check_win(board,"O"):
        messagebox.showinfo("Result","AI Wins!")
        reset(); return True
    elif " " not in board:
        messagebox.showinfo("Result","It's a Tie!")
        reset(); return True
    return False

def reset():
    global board
    board = [" "] * 9
    for b in buttons:
        b.config(text=" ", state="normal")

def new_level():
    global board, buttons
    for b in buttons:
        b.destroy()
    buttons.clear()
    board = [" "] * 25
    for i in range(25):
        b = tk.Button(root, text=" ", font=('Arial', 20), width=3, height=1,
                      command=lambda i=i: click_level2(i))
        b.grid(row=i//5, column=i%5)
        buttons.append(b)

def click_level2(i):
    if board[i] == " ":
        board[i] = "X"
        buttons[i].config(text="X", state="disabled")
        # You can later add 5x5 win logic here or just random AI
        ai_move_level2()

def ai_move_level2():
    empty = [i for i in range(len(board)) if board[i]==" "]
    if not empty: return
    i = random.choice(empty)
    board[i] = "O"
    buttons[i].config(text="O", state="disabled")

for i in range(9):
    b = tk.Button(root, text=" ", font=('Arial',24), width=5, height=2,
                  command=lambda i=i: click(i))
    b.grid(row=i//3, column=i%3)
    buttons.append(b)

tk.Button(root, text="Restart", font=('Arial',14), command=reset).grid(row=3, column=0, columnspan=3, sticky="nsew")

root.mainloop()
