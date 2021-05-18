import main
from piece import Piece
from graphics2 import *


# p = Piece("b", "p", "assets/pieces/bp.png")
# P = Piece("w", "p", "assets/pieces/wp.png")

# k = Piece("b", "k", "assets/pieces/bk.png")
# K = Piece("w", "k", "assets/pieces/wk.png")

# r = Piece("b", "r", "assets/pieces/br.png")
# R = Piece("w", "r", "assets/pieces/wr.png")

# b = Piece("b", "b", "assets/pieces/bb.png")
# B = Piece("w", "b", "assets/pieces/wb.png")

# q = Piece("b", "q", "assets/pieces/bq.png")
# Q = Piece("w", "q", "assets/pieces/wq.png")

# n = Piece("b", "n", "assets/pieces/bn.png")
# N = Piece("w", "n", "assets/pieces/wn.png")

starting_order = {
    (0, 0): Piece("b", "r", "assets/br.png", Point(0, 0)),
    (1, 0): Piece("b", "n", "assets/bn.png", Point(1, 0)),
    (2, 0): Piece("b", "b", "assets/bb.png", Point(2, 0)),
    (3, 0): Piece("b", "k", "assets/bk.png", Point(3, 0)),
    (4, 0): Piece("b", "q", "assets/bq.png", Point(4, 0)),
    (5, 0): Piece("b", "b", "assets/bb.png", Point(5, 0)),
    (6, 0): Piece("b", "n", "assets/bn.png", Point(6, 0)),
    (7, 0): Piece("b", "r", "assets/br.png", Point(7, 0)),
    (0, 1): Piece("b", "p", "assets/bp.png", Point(0, 1)),
    (1, 1): Piece("b", "p", "assets/bp.png", Point(1, 1)),
    (2, 1): Piece("b", "p", "assets/bp.png", Point(2, 1)),
    (3, 1): Piece("b", "p", "assets/bp.png", Point(3, 1)),
    (4, 1): Piece("b", "p", "assets/bp.png", Point(4, 1)),
    (5, 1): Piece("b", "p", "assets/bp.png", Point(5, 1)),
    (6, 1): Piece("b", "p", "assets/bp.png", Point(6, 1)),
    (7, 1): Piece("b", "p", "assets/bp.png", Point(7, 1)),
    (0, 2): None,
    (1, 2): None,
    (2, 2): None,
    (3, 2): None,
    (4, 2): None,
    (5, 2): None,
    (6, 2): None,
    (7, 2): None,
    (0, 3): None,
    (1, 3): None,
    (2, 3): None,
    (3, 3): None,
    (4, 3): None,
    (5, 3): None,
    (6, 3): None,
    (7, 3): None,
    (0, 4): None,
    (1, 4): None,
    (2, 4): None,
    (3, 4): None,
    (4, 4): None,
    (5, 4): None,
    (6, 4): None,
    (7, 4): None,
    (0, 5): None,
    (1, 5): None,
    (2, 5): None,
    (3, 5): None,
    (4, 5): None,
    (5, 5): None,
    (6, 5): None,
    (7, 5): None,
    (0, 6): Piece("w", "p", "assets/pieces/wp.png", Point(0, 6)),
    (1, 6): Piece("w", "p", "assets/pieces/wp.png", Point(1, 6)),
    (2, 6): Piece("w", "p", "assets/pieces/wp.png", Point(2, 6)),
    (3, 6): Piece("w", "p", "assets/pieces/wp.png", Point(3, 6)),
    (4, 6): Piece("w", "p", "assets/pieces/wp.png", Point(4, 6)),
    (5, 6): Piece("w", "p", "assets/pieces/wp.png", Point(5, 6)),
    (6, 6): Piece("w", "p", "assets/pieces/wp.png", Point(6, 6)),
    (7, 6): Piece("w", "p", "assets/pieces/wp.png", Point(7, 6)),
    (0, 7): Piece("w", "r", "assets/pieces/wr.png", Point(0, 7)),
    (1, 7): Piece("w", "n", "assets/pieces/wn.png", Point(1, 7)),
    (2, 7): Piece("w", "b", "assets/pieces/wb.png", Point(2, 7)),
    (3, 7): Piece("w", "k", "assets/pieces/wk.png", Point(3, 7)),
    (4, 7): Piece("w", "q", "assets/pieces/wq.png", Point(4, 7)),
    (5, 7): Piece("w", "b", "assets/pieces/wb.png", Point(5, 7)),
    (6, 7): Piece("w", "n", "assets/pieces/wn.png", Point(6, 7)),
    (7, 7): Piece("w", "r", "assets/pieces/wr.png", Point(7, 7)),
}


def testEmptyBoard():
    # does it have all the lines in the right places?

    window = main.createGameWindow("Test")
    main.drawInitialBoard(window)


def drawInitialPieces():
    board = [["  " for i in range(8)] for i in range(8)]
    window = main.createGameWindow("Test")
    main.drawInitialBoard(window)
    for piece in starting_order.values():
        if piece != None:
            piece.draw(window)


drawInitialPieces()
