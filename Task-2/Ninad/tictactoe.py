import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 800
LINE_WIDTH = 20
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

# Fonts
pygame.font.init()
font = pygame.font.SysFont("Arial", 48, bold=True)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(BG_COLOR)

# Board
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]


def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                          int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS,
                                   CIRCLE_WIDTH)
            elif board[row][col] == "X":
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)


def check_winner(b, player):
    for row in range(BOARD_ROWS):
        if all(cell == player for cell in b[row]):
            return True
    for col in range(BOARD_COLS):
        if all(b[row][col] == player for row in range(BOARD_ROWS)):
            return True
    if all(b[i][i] == player for i in range(BOARD_ROWS)):
        return True
    if all(b[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False


def check_draw(b):
    return all(b[row][col] != " " for row in range(BOARD_ROWS) for col in range(BOARD_COLS))


def minimax(b, is_ai):
    if check_winner(b, "O"):
        return 1
    elif check_winner(b, "X"):
        return -1
    elif check_draw(b):
        return 0

    if is_ai:
        best = -math.inf
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if b[i][j] == " ":
                    b[i][j] = "O"
                    score = minimax(b, False)
                    b[i][j] = " "
                    best = max(score, best)
        return best
    else:
        best = math.inf
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if b[i][j] == " ":
                    b[i][j] = "X"
                    score = minimax(b, True)
                    b[i][j] = " "
                    best = min(score, best)
        return best


def best_move():
    best_score = -math.inf
    move = None
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


def restart():
    global board
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    screen.fill(BG_COLOR)
    draw_lines()


def show_message(text):
    msg = font.render(text, True, (255, 255, 255))
    rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(msg, rect)
    pygame.display.update()
    pygame.time.wait(2000)
    restart()


draw_lines()
player_turn = True
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if player_turn and not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if board[clicked_row][clicked_col] == " ":
                    board[clicked_row][clicked_col] = "X"
                    draw_figures()
                    if check_winner(board, "X"):
                        show_message("You Win!")
                        game_over = True
                    elif check_draw(board):
                        show_message("Draw!")
                        game_over = True
                    else:
                        player_turn = False

        if not player_turn and not game_over:
            pygame.time.wait(500)
            move = best_move()
            if move:
                board[move[0]][move[1]] = "O"
                draw_figures()
                if check_winner(board, "O"):
                    show_message("AI Wins!")
                    game_over = True
                elif check_draw(board):
                    show_message("Draw!")
                    game_over = True
                else:
                    player_turn = True

    pygame.display.update()
