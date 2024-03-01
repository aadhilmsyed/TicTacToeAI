# Tic Tac Toe AI

This project is an implementation of the classic game Tic Tac Toe with AI players, built using Python and Pygame. It allows playing against different AI strategies, including Random AI, Minimax AI, Alpha-Beta Pruning AI, and Monte Carlo Tree Search AI, or simply enjoying a game between two humans.

## Features

- Play against AI or another human player.
- Different AI opponents:
  - Random AI: Makes moves at random.
  - Simple AI: Follows a predefined set of moves.
  - Monte Carlo AI: Uses Monte Carlo simulations to decide moves.
  - Minimax AI: Implements the Minimax algorithm for optimal play.
  - Alpha-Beta AI: Optimizes Minimax with Alpha-Beta pruning for faster decision-making.
- Customizable board size (default is 3x3).
- Graphical interface using Pygame.

## Installation

To run this game, you need Python and Pygame installed on your system. If you don't have Python installed, download and install it from [python.org](https://www.python.org/downloads/). All dependencies can be installed using:

```
pip install -r requirements.txt
```

## Usage

Navigate to the directory containing the files on your terminal and run the following command:

```
python main.py -p1 <player1> -p2 <player2>
```

Be sure to replace `<player1>` and `<player2>` with one of the following: `human`, `simpleAI`, `randomAI`, `monteCarloAI`, `minimaxAI`, or `alphaBetaAI`.
When playing as a human, simply click on the tile that you'd like to play your move on, and the game will update the tile accordingly.

Note: Player 1 will always be 'X' and Player 2 will always be 'O'


## Example Usage

```
python main.py -p1 human -p2 human
```
```
python main.py -p1 human -p2 monteCarloAI
```
```
python main.py -p1 monteCarloAI -p2 alphaBetaAI
```

