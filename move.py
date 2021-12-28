"""
move
Determining valid moves at current state.
"""

class Move():
    """
    Board is an 8x8 2d list, each element in list has 2 characters.
    The first character represents the color of the piece: 'b' or 'w'.
    The second character represents the type of the piece: 'r', 'n', 'b', 'q', 'k' or 'p'.
    "." represents an empty space with no piece.
    """

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k,v in filesToCols.items()}
    def __init__(self, startSq, endSq, board, isEnpassantMove = False):
        """
        Param: startSq - tuple
        Param: endSq - tuple
        Param: board (make sure the move is valid)
        """
        self.startRow = startSq[0] # 3
        self.startCol = startSq[1] # 6
        self.endRow = endSq[0] # 3
        self.endCol = endSq[1] # 4
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] # could be "."
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        self.isEnpassantMove =  isEnpassantMove #self.pieceMoved[1] == 'p' and (self.endRow, self.endCol) == isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved =='bp' else 'bp'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    """
    Overriding the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        """
        Make chess move to real chess notation

        """
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        """
        Helper function to convert row, col to rank file
        0, 0 -> a8

        """
        return self.colsToFiles[col] + self.rowsToRanks[row]