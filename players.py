import random
import numpy as np
import pygame
import sys
import math
from copy import deepcopy

class Player:
    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = 'X' if self.symbol == 'O' else 'O'

    def play(self, env):
        pass

class Human(Player):
    def play(self, env):
    
        # Wait until the user has played a valid move
        while True:
            for event in pygame.event.get():
            
                # If the User quits the game, quit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    print("User Termianted the Game")
                    sys.exit()
                    
                # If the User has clicked on a position on the board, check it
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    row = mouseY // env.cell_size
                    col = mouseX // env.cell_size
                    
                    # If the move is valid, return it
                    if env.getBoard()[row, col] == '':
                        return row, col

class SimpleAI(Player):
    def play(self, env):
        
        # Get the Current Game Board
        board = env.getBoard()
        
        # List of moves to play
        moves = [(1,1), (0,0), (0,2), (2,0), (2,2), (0,1), (1,0), (1,2), (2,1)]
        
        # Find a Valid Move and Return it
        for row, col in moves:
            if board[row, col] == '': return row, col


class RandomAI(Player):
    def play(self, env):
        
        # Get the Current Game Board
        board = env.getBoard()
        
        # Get the List of Possible Moves
        possible = [(row, col) for row in range(3) for col in range(3) if board[row, col] == '']
            
        # Select a Random Move and Play it
        row, col = random.choice(possible)
        return row, col


class MonteCarloAI(Player):

    def play(self, env):
    
        # Deepcopy environment to avoid mutating original game state
        board = env.getBoard()
        
        # Find legal moves
        possible_moves = [(row, col) for row in range(3) for col in range(3) if board[row, col] == '']
        
        # Init fitness trackers
        scores = np.zeros(len(possible_moves))

        # Simulate games
        num_simulations = 1000
        for i in range(num_simulations):
            for move_index, (row, col) in enumerate(possible_moves):
            
                # Simulate a random game starting with this move
                board = env.getBoard()
                score = self.playRandomGame(board, (row, col))
                scores[move_index] += score

        # Choose the move with the highest score
        best_move_index = np.argmax(scores)
        return possible_moves[best_move_index]


    def playRandomGame(self, board, first_move):
    
        # Make the first move
        switch = {'X': 'O', 'O': 'X'}
        symbol = self.symbol
        row, col = first_move
        board[row, col] = symbol

        # While the Game has not Ended
        while True:
        
            # Switch players
            symbol = switch[symbol]
            
            # Get current board state
            possible = [(row, col) for row in range(3) for col in range(3) if board[row, col] == '']
            if not possible: return 0

            # Select a Random Move and Play It
            row, col = random.choice(possible)
            board[row, col] = symbol
            
            # If there is a Winner, End the Game and Return Results
            winner = self.check_winner(board, symbol)
            if winner == self.symbol: return 1
            elif winner == switch[self.symbol]: return -1
            elif winner == 'Tie': return 0
            else: continue
            
        
    def check_winner(self, board, symbol):
        
        # Check the rows and columns
        for i in range(3):
            if np.all(board[i,:] == symbol) or np.all(board[:,i] == symbol): return symbol

        # Check diagonals
        if np.all(np.diag(board) == symbol) or np.all(np.diag(np.fliplr(board)) == symbol): return symbol

        # Check for a tie (if there are no empty cells left)
        if np.all(board != ''): return 'Tie'

        # If no winner and no tie, the game continues
        return None
        

class MinimaxAI(Player):

    def play(self, env):
        board = env.getBoard()
        _, row, col = self.maxValue(board)
        return row, col
        
    
    def maxValue(self, board):
        
        # Get the List of Possible Moves
        possible = [(row, col) for row in range(3) for col in range(3) if board[row, col] == '']
        
        # Initialize the Maximum Value to Negative Infinity
        max_val = -math.inf
        max_row, max_col = None, None
        symbol = self.symbol
        
        # Find the Best Move
        for row, col in possible:
            
            # Simulate the Move
            new_board = deepcopy(board)
            new_board[row, col] = symbol
            
            # Check if player has won
            winner = self.check_winner(new_board, symbol)
            if winner == 'Win': return 50, row, col
            if winner == 'Tie': return self.evaluate(new_board), row, col
            
            # Get the Maximum Value
            value, _, _ = self.minValue(new_board)
            if value > max_val: max_val, max_row, max_col = value, row, col
            
        return max_val, max_row, max_col
        
    
    def minValue(self, board):
    
        # Get the List of Possible Moves
        possible = [(row, col) for row in range(3) for col in range(3) if board[row, col] == '']
        
        # Initialize the Maximum Value to Negative Infinity
        min_val = math.inf
        min_row, min_col = None, None
        symbol = self.opponent_symbol
        
        # Find the Best Move
        for row, col in possible:
            
            # Simulate the Move
            new_board = deepcopy(board)
            new_board[row, col] = symbol
            
            # Check if player has won
            winner = self.check_winner(new_board, symbol)
            if winner == 'Win': return -50, row, col
            if winner == 'Tie': return self.evaluate(new_board), row, col
            
            # Get the Maximum Value
            value, _, _ = self.maxValue(new_board)
            if value < min_val: min_val, min_row, min_col = value, row, col
            
        return min_val, min_row, min_col


    def evaluate(self, board):
        
        # Initialize Utility for Self Player and Opponent Player
        self_util, opp_util = 0, 0
        
        # Utility of Middle Piece
        for row, col in [(1,1)]:
            if board[row, col] == self.symbol: self_util += 10
            else: opp_util += 10
            
        # Utility of Corner Pieces
        for row, col in [(0,0), (0,2), (2,0), (2,2)]:
            if board[row, col] == self.symbol: self_util += 5
            else: opp_util += 5
            
        # Utility of Corner Pieces
        for row, col in [(0,1), (1,0), (1,2), (2,1)]:
            if board[row, col] == self.symbol: self_util += 1
            else: opp_util += 1
            
        # Return the Overall Utility
        return self_util - opp_util
        
            
    def check_winner(self, board, symbol):
        
        # Check the rows and columns
        for i in range(3):
            if np.all(board[i,:] == symbol) or np.all(board[:,i] == symbol): return 'Win'

        # Check diagonals
        if np.all(np.diag(board) == symbol) or np.all(np.diag(np.fliplr(board)) == symbol): return 'Win'

        # Check for a tie (if there are no empty cells left)
        if np.all(board != ''): return 'Tie'

        # If no winner and no tie, the game continues
        return None
            
        

class AlphaBetaAI(Player):

    def play(self, env):
        board = env.getBoard()
        alpha, beta = -math.inf, math.inf
        value, row, col = self.maxValue(board, alpha, beta)
        return row, col
        
    
    def maxValue(self, board, alpha, beta):
        
        # Get the List of Possible Moves
        possible = [(row, col) for row in range(3) for col in range(3) if board[row, col] == '']
        
        # Initialize the Maximum Value to Negative Infinity
        max_val = -math.inf
        max_row, max_col = None, None
        symbol = self.symbol
        
        # Find the Best Move
        for row, col in possible:
            
            # Simulate the Move
            new_board = deepcopy(board)
            new_board[row, col] = symbol
            
            # Check if player has won
            winner = self.check_winner(new_board, symbol)
            if winner == 'Win': return 50, row, col
            if winner == 'Tie': return self.evaluate(new_board), row, col
            
            # Get the Maximum Value
            value, _, _ = self.minValue(new_board, alpha, beta)
            if value > max_val: max_val, max_row, max_col = value, row, col
            
            # Alpha-Beta Pruning
            if value >= beta: return value, row, col
            alpha = max(alpha, value)
            
        return max_val, max_row, max_col
        
    
    def minValue(self, board, alpha, beta):
    
        # Get the List of Possible Moves
        possible = [(row, col) for row in range(3) for col in range(3) if board[row, col] == '']
        
        # Initialize the Maximum Value to Negative Infinity
        min_val = math.inf
        min_row, min_col = None, None
        symbol = self.opponent_symbol
        
        # Find the Best Move
        for row, col in possible:
            
            # Simulate the Move
            new_board = deepcopy(board)
            new_board[row, col] = symbol
            
            # Check if player has won
            winner = self.check_winner(new_board, symbol)
            if winner == 'Win': return -50, row, col
            if winner == 'Tie': return self.evaluate(new_board), row, col
            
            # Get the Maximum Value
            value, _, _ = self.maxValue(new_board, alpha, beta)
            if value < min_val: min_val, min_row, min_col = value, row, col
            
            # Alpha-Beta Pruning
            if value <= alpha: return value, row, col
            beta = min(beta, value)
            
        return min_val, min_row, min_col


    def evaluate(self, board):
        
        # Initialize Utility for Self Player and Opponent Player
        self_util, opp_util = 0, 0
        
        # Utility of Middle Piece
        for row, col in [(1,1)]:
            if board[row, col] == self.symbol: self_util += 10
            else: opp_util += 10
            
        # Utility of Corner Pieces
        for row, col in [(0,0), (0,2), (2,0), (2,2)]:
            if board[row, col] == self.symbol: self_util += 5
            else: opp_util += 5
            
        # Utility of Corner Pieces
        for row, col in [(0,1), (1,0), (1,2), (2,1)]:
            if board[row, col] == self.symbol: self_util += 1
            else: opp_util += 1
            
        # Return the Overall Utility
        return self_util - opp_util
        
            
    def check_winner(self, board, symbol):
        
        # Check the rows and columns
        for i in range(3):
            if np.all(board[i,:] == symbol) or np.all(board[:,i] == symbol): return 'Win'

        # Check diagonals
        if np.all(np.diag(board) == symbol) or np.all(np.diag(np.fliplr(board)) == symbol): return 'Win'

        # Check for a tie (if there are no empty cells left)
        if np.all(board != ''): return 'Tie'

        # If no winner and no tie, the game continues
        return None

