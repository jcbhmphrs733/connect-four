import numpy as np
import pygame
import sys
import math
import random


def create_board():
    board = np.zeros((6, 7))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece
    

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(5, -1, -1):
        if board[r][col] == 0:
            return r
    return None

def is_winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(4):
        for r in range(6):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(7):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(4):
        for r in range(3, 6):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(4):
        for r in range(3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    return False

def play_rand_drop_sound(drop_sfx):
    drop_sfx = random.choice(drop_sfx)
    drop_sfx.play()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def track_mouse():
    screen.fill((0,0,0))
    mouseX = pygame.mouse.get_pos()[0]
    if turn == 0:
        pygame.draw.circle(screen, (255, 0, 0), (mouseX, 0), 45)
    else:
        pygame.draw.circle(screen, (255, 255, 0), (mouseX, 0), 45)
    draw_board(board)

def draw_board(board):
    for c in range(7):
        for r in range(6):
            # Draw row r at screen position r (top row is board[0], bottom row is board[5])
            cell_x = c * 100
            cell_y = r * 100
            center_x = int(cell_x + 50)
            center_y = int(cell_y + 50)
            if board[r][c] == 0:
                if r == 0:
                    continue
                pygame.draw.rect(screen, (0, 0, 255), (cell_x, cell_y, 100, 100))
                pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), 45)
            elif board[r][c] == 1:
                pygame.draw.rect(screen, (0, 0, 255), (cell_x, cell_y, 100, 100))
                pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), 45)
            elif board[r][c] == 2:
                pygame.draw.rect(screen, (0, 0, 255), (cell_x, cell_y, 100, 100))
                pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), 45)

board = create_board()
game_over = False
turn = 0


pygame.init()
drop_sfx = []
for i in range(6):
    drop_sfx.append(pygame.mixer.Sound(f'dropSounds/drop-sound{i+1}.mp3'))
spill_sfx = pygame.mixer.Sound('game-start-spill.mp3')
game_over_sfx = pygame.mixer.Sound('game-over-winner.mp3')
pygame.mixer.music.load('background-music.mp3')
pygame.mixer.music.set_volume(0.25)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music indefinitely
spill_sfx.play()

text_font = pygame.font.SysFont("Arial", 30)

pygame.display.set_caption('Connect 4')
screen = pygame.display.set_mode((700, 600))
draw_board(board)
pygame.display.update()

is_winner = False

while True:
    if not is_winner:
        track_mouse()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            is_winner = False
            screen.fill((0,0,0))
            board = create_board()
            draw_board(board)
            pygame.display.update()
            spill_sfx.play()
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and is_winner == False:
            play_rand_drop_sound(drop_sfx)
            # ask for player 1 input
            if turn == 0:
                mouseX = event.pos[0]
                col = math.floor(mouseX / 100)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    draw_board(board)
                    pygame.display.update()

            # ask for player 2 input
            else:
                mouseX = event.pos[0]
                col = math.floor(mouseX / 100)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    draw_board(board)
                    pygame.display.update()

  
            # Check for winning move
            if is_winning_move(board, 1):
                is_winner = True
                game_over_sfx.play()
                draw_text("Player One Wins!", text_font, (255, 0, 0), 50, 50)
                draw_text("Press R to Restart!", text_font, (0, 255, 0), 350, 50)
                pygame.display.update()

            elif is_winning_move(board, 2):
                is_winner = True
                game_over_sfx.play()
                draw_text("Player Two Wins!", text_font, (255, 255, 0), 50, 50)
                draw_text("Press R to Restart!", text_font, (0, 255, 0), 350, 50)
                pygame.display.update()

            turn += 1
            turn = turn % 2
    
    pygame.display.update()