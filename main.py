import numpy as np
import pygame
import sys
import math
import random
# import os


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

drop_sfx = []

pygame.init()
for i in range(6):
    drop_sfx.append(pygame.mixer.Sound(f'dropSounds/drop-sound{i+1}.mp3'))
spill_sfx = pygame.mixer.Sound('game-start-spill.mp3')
pygame.mixer.music.load('background-music.mp3')
pygame.mixer.music.set_volume(0.25)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music indefinitely
spill_sfx.play()

pygame.display.set_caption('Connect 4')
pygame.display.set_mode((700, 600))
screen = pygame.display.set_mode((700, 600))
draw_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            play_rand_drop_sound(drop_sfx)
            # ask for player 1 input
            if turn == 0:
                mouseX = event.pos[0]
                col = math.floor(mouseX / 100)
                print(col)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    draw_board(board)
                    pygame.display.update()

            # ask for player 2 input
            else:
                mouseX = event.pos[0]
                col = math.floor(mouseX / 100)
                print(col)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    draw_board(board)
                    pygame.display.update()

  
            # Check for winning move
            if is_winning_move(board, 1):
                game_over = True
                print("Player 1 wins.")
            elif is_winning_move(board, 2):
                game_over = True
                print("Player 2 wins.")

            turn += 1
            turn = turn % 2