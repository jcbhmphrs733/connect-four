import numpy as np
import pygame
import sys
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

def winning_move(board, piece):
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


def draw_board(board):
    pass

board = create_board()
print(board)
game_over = False
turn = 0

pygame.init()

pygame.display.set_caption('Connect 4')
pygame.display.set_mode((700, 600))

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # ask for player 1 input
            if turn == 0:
                col = int(input("Player 1 Make your Selection (0-6): "))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    

            # ask for player 2 input
            else:
                col = int(input("Player 2 Make your Selection (0-6): "))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
            

    print(board)

    # Check for winning move
    if winning_move(board, 1):
        game_over = True
        print("Player 1 wins.")
    elif winning_move(board, 2):
        game_over = True
        print("Player 2 wins.")

    turn += 1
    turn = turn % 2