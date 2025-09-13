#imports
import numpy as np
import pygame
import sys
import math
import random

#constants
ROWS = 6
COLUMNS = 7
SQUARESIZE = 75
CIRCLE_RADIUS = int(SQUARESIZE/2 - 5)
global IS_WINNER
IS_WINNER = False

#helper functions
def create_board(): #instantiates a numpy matrix of zeros
    if ROWS < 4 or COLUMNS < 4:
        raise ValueError("Board must be at least 4 rows and 4 columns for a valid game.")
    board = np.zeros((ROWS, COLUMNS))
    return board

def drop_piece(board, row, col, piece): #change the value in the matrix to the player's number (1 or 2)
    board[row][col] = piece 
    
def is_valid_location(board, col): #if the top row of a column is 0, then the column is not full yet.
    return board[0][col] == 0 

def get_next_open_row(board, col): #loops over rows in col and if it finds a 0, it returns that row's index
    for r in range(ROWS-1, -1, -1): #starts checking from the bottom row to teh top row
        if board[r][col] == 0: 
            return r
    return None

def is_winning_move(board, piece): #check all possible winning combinations for a given piece (1 or 2)
    # Check horizontal locations for win
    for c in range(COLUMNS - 3):  # Need at least 4 columns for horizontal win
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS - 3):  # Need at least 4 rows for vertical win
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMNS - 3):  # Need at least 4 columns
        for r in range(3, ROWS):  # Start from row 3 to have space above
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMNS - 3):  # Need at least 4 columns
        for r in range(ROWS - 3):  # Need at least 4 rows below
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    return False

def play_rand_drop_sound(drop_sfx): #plays a random drop sound effect from the list
    drop_sfx = random.choice(drop_sfx) #choose a random sound from the list
    drop_sfx.play()

def draw_text(text, font, text_col, x, y): #
    img = font.render(text, True, text_col) 
    screen.blit(img, (x, y))

def track_mouse(): #tracks the mouse position and draws the current player's piece above the columns
    screen.fill((0,0,0))
    mouseX = pygame.mouse.get_pos()[0]
    if turn == 0:
        pygame.draw.circle(screen, (255, 0, 0), (mouseX, 0), CIRCLE_RADIUS)
    else:
        pygame.draw.circle(screen, (255, 255, 0), (mouseX, 0), CIRCLE_RADIUS)
    draw_board(board)

def restart_game(): #restarts the game
    global IS_WINNER, board, turn
    IS_WINNER = False
    turn = 0
    screen.fill((0,0,0))
    board = create_board()
    pygame.display.update()
    draw_board(board)
    spill_sfx.play()

def handle_win(player_num): # handles the win condition
    global IS_WINNER
    IS_WINNER = True
    game_over_sfx.play()
    if player_num == 1:
        draw_text("Player One Wins!", text_font, (255, 0, 0), 25, CIRCLE_RADIUS + 5)
    else:
        draw_text("Player Two Wins!", text_font, (255, 255, 0), 25, CIRCLE_RADIUS + 5)
    draw_text("Press R to Restart!", text_font, (0, 255, 0), 250, CIRCLE_RADIUS + 5)
    pygame.display.update()

def handle_player_move(event): # handles a player's move when they click a column
    global turn
    col = math.floor(event.pos[0] / SQUARESIZE)
    if is_valid_location(board, col):
        play_rand_drop_sound(drop_sfx)
        row = get_next_open_row(board, col)
        current_player = 1 if turn == 0 else 2
        drop_piece(board, row, col, current_player)
        draw_board(board)
        
        # Check for winning move
        if is_winning_move(board, current_player):
            handle_win(current_player)
        
        # Always increment turn after a valid move
        turn += 1
        turn = turn % 2
    else:
        pass # Column is full, ignore the click

def draw_board(board): # draw the board and pieces on the screen
    for c in range(COLUMNS):
        for r in range(ROWS):
            # Draw row r at screen position r (top row is board[0], bottom row is board[ROWS-1])
            cell_x = c * SQUARESIZE
            cell_y = r * SQUARESIZE + SQUARESIZE  # Offset by SQUARESIZE to account for top row
            center_x = int(cell_x + SQUARESIZE/2)
            center_y = int(cell_y + SQUARESIZE/2) 
            if board[r][c] == 0:
                pygame.draw.rect(screen, (0, 0, 255), (cell_x, cell_y, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), CIRCLE_RADIUS)
            elif board[r][c] == 1:
                pygame.draw.rect(screen, (0, 0, 255), (cell_x, cell_y, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), CIRCLE_RADIUS)
            elif board[r][c] == 2:
                pygame.draw.rect(screen, (0, 0, 255), (cell_x, cell_y, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), CIRCLE_RADIUS)
    pygame.display.update()

#create game instance
pygame.init()
pygame.display.set_caption('Connect 4')
screen_size = (COLUMNS * SQUARESIZE, ROWS * SQUARESIZE + SQUARESIZE)
screen = pygame.display.set_mode(screen_size)

board = create_board()
turn = 0

#sound effects
drop_sfx = []
for i in range(6):
    drop_sfx.append(pygame.mixer.Sound(f'dropSounds/drop-sound{i+1}.mp3'))

spill_sfx = pygame.mixer.Sound('game-start-spill.mp3')
game_over_sfx = pygame.mixer.Sound('game-over-winner.mp3')
pygame.mixer.music.load('background-music.mp3')
pygame.mixer.music.set_volume(0.25)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play the music indefinitely
spill_sfx.play()

#fonts
text_font = pygame.font.SysFont("Arial", 30)


#main game loop
while True:

    if not IS_WINNER:
        track_mouse()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and IS_WINNER:
            restart_game()
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and IS_WINNER == False:
            handle_player_move(event)
    
    pygame.display.update()