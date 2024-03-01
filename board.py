import numpy as np
import pygame
import sys
import random
from copy import deepcopy
import players

class TicTacToe:
    def __init__(self, player1, player2, board_shape=(3,3)):
        """
        Description:
            - Initialization Function for Game of TicTacToe
        
        Parameters:
            - player1 : The player agent object for Player 1
            - player2 : The player agent object for Player 2
            - board_shape : The shape of the board. 3x3 by default
        """
        self.board = np.full(board_shape, '', dtype=str)
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.game_over = False
        self.size = 300  # Size of the Pygame window
        self.cell_size = self.size // 3
        self.bg_color = (255, 255, 255)  # White
        self.line_color = (0, 0, 0)  # Black
        self.x_color = (255, 0, 0) # Red
        self.o_color = (0, 0, 255) # Blue
        pygame.init()
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Tic Tac Toe")
        self.screen.fill(self.bg_color)
        self.draw_board()

    def draw_board(self):
        """
        Description:
            - Creates the TicTacToe Game Board
        
        Parameters:
            - None
            
        Returns:
            - None
        """
        for x in range(1, 3):
            pygame.draw.line(self.screen, self.line_color, (0, x * self.cell_size), (self.size, x * self.cell_size), 2)
            pygame.draw.line(self.screen, self.line_color, (x * self.cell_size, 0), (x * self.cell_size, self.size), 2)
        pygame.display.update()

    def draw_move(self, row, col):
        """
        Description:
            - Draws a Move on the Pygame Board
        
        Parameters:
            - row (int) : The row to make the move on
            - col (int) : The column to make the move on
            
        Returns:
            - None
        """
        centerX = col * self.cell_size + self.cell_size // 2
        centerY = row * self.cell_size + self.cell_size // 2
        if self.current_player.symbol == 'X':
            pygame.draw.line(self.screen, self.x_color, (centerX - 40, centerY - 40), (centerX + 40, centerY + 40), 5)
            pygame.draw.line(self.screen, self.x_color, (centerX + 40, centerY - 40), (centerX - 40, centerY + 40), 5)
        else:
            pygame.draw.circle(self.screen, self.o_color, (centerX, centerY), 40, 5)
        pygame.display.update()

    def check_winner(self):
        """
        Description:
            - Checks if a Player Has Won the TicTacToe Game
        
        Parameters:
            - None
            
        Returns:
            - 'Tie' if game ends in a tie
            - self.current_player if the current player has won the game
            - None otherwise
        """
        # Check the rows and columns
        for i in range(3):
            if np.all(self.board[i,:] == self.current_player.symbol): self.game_over = True; return self.current_player
            if np.all(self.board[:,i] == self.current_player.symbol): self.game_over = True; return self.current_player

        # Check diagonals
        if np.all(np.diag(self.board) == self.current_player.symbol) or np.all(np.diag(np.fliplr(self.board)) == self.current_player.symbol):
            self.game_over = True; return self.current_player

        # Check for a tie (if there are no empty cells left)
        if np.all(self.board != ''): self.game_over = True; return 'Tie'

        # If no winner and no tie, the game continues
        return None

    def make_move(self, row, col):
        """
        Description:
            - Draws a Move on the TicTacToe Game Board
        
        Parameters:
            - row (int) : The row to make the move on
            - col (int) : The column to make the move on
            
        Returns:
            - None
        """
        self.board[row, col] = self.current_player.symbol
        self.draw_move(row, col)
        
    def make_random_move(self):
        """
        Description:
            - Makes a Random Move on the TicTacToe Game Board
        
        Parameters:
            - row (int) : The row to make the move on
            - col (int) : The column to make the move on
            
        Returns:
            - None
        """
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row, col] == '']
        row, col = random.choice(empty_cells)
        self.make_move(row, col)
            
    def switch_player(self):
        """
        Description:
            - Switches the Current Player
        
        Parameters:
            - None
            
        Returns:
            - None
        """
        self.current_player = self.player2 if self.current_player is self.player1 else self.player1
    
    def play(self):
        """
        Description:
            - Main Game Loop. Gets Move from the player agents and plays it until the game has concluded.
        
        Parameters:
            - Nonoe
            
        Returns:
            - None
        """

        while not self.game_over:
        
            # Check if the Game was Quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    print("User Terminated the Game")
                    sys.exit()
            
            # Get a Move from the Player Agent
            row, col = self.current_player.play(self)

            # Play the Move from the Player if it is Valid, otherwise play random move
            if 0 <= row < 3 and 0 <= col < 3 and self.board[row, col] == '':  # Assume valid move is returned
                self.make_move(row, col)
            else:
                self.make_random_move()
            
            # Print the Current State of the Board
            print(self.board)
            
            # Check if there is a Winner
            winner = self.check_winner()
            if winner == None:
                self.switch_player()
            elif winner == 'Tie':
                self.game_over = True
                print("The game is a tie!")
                pygame.display.set_caption("Tic Tac Toe - Tie!")
            else:
                self.game_over = True
                print(f"{winner.symbol} wins!")
                pygame.display.set_caption(f"Tic Tac Toe - {winner.symbol} Wins!")
        
        # If the Game Loop has Broken, Quit the Game
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    break
        
    def getBoard(self):
        """
        Description:
            - Returns a copy of the board for foreign classes to use
        
        Parameters:
            - Nonoe
            
        Returns:
            - None
        """
        return deepcopy(self.board)
                    

