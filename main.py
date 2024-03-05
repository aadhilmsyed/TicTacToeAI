import argparse
import random
from board import TicTacToe
from players import Human, SimpleAI, RandomAI, MonteCarloAI, MinimaxAI, AlphaBetaAI

parser = argparse.ArgumentParser(description='Run Tic Tac Toe game')
parser.add_argument('-w', default=3, type=int, help='Rows of game')
parser.add_argument('-l', default=3, type=int, help='Columns of game')
parser.add_argument('-p1', default='human', type=str, help='Player 1 agent. Use any of the following: [human, stupidAI, randomAI, monteCarloAI, minimaxAI, alphaBetaAI]')
parser.add_argument('-p2', default='human', type=str, help='Player 2 agent. Use any of the following: [human, stupidAI, randomAI, monteCarloAI, minimaxAI, alphaBetaAI]')
parser.add_argument('-seed', default=0, type=int, help='Seed for Randomization. Enter an Integer Value.')

args = parser.parse_args()

w = args.w
l = args.l
random.seed(args.seed)

agents = {'human': Human, 'simpleAI': SimpleAI, 'randomAI': RandomAI, 'monteCarloAI': MonteCarloAI, 'minimaxAI': MinimaxAI, 'alphaBetaAI': AlphaBetaAI}

if __name__ == '__main__':
    player1 = agents[args.p1]('X')
    player2 = agents[args.p2]('O')
    tic_tac_toe = TicTacToe(player1, player2, board_shape=(w,l))
    tic_tac_toe.play()
