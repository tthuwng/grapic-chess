  
"""
Handling the AI moves.
"""

import random


def findRandomMove(validMoves):
    """
    Handling the AI moves.
    """
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove():
    return