

class GameState():
    def __init__(self):
        # board 8x8 2D list, lowercase - Black, upperCase - White, "." means empty space
        self.board = [
            ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            [".",  ".",  ".",  ".",  ".",  ".",  ".",  "."],
            [".",  ".",  ".",  ".",  ".",  ".",  ".",  "."],
            [".",  ".",  ".",  ".",  ".",  ".",  ".",  "."],
            [".",  ".",  ".",  ".",  ".",  ".",  ".",  "."],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
        ]
        self.moveFunctions = {'p': self.getPawnMoves,
                              'r': self.getRookMoves,
                              'n': self.getKnightMoves,
                              'b': self.getBishopMoves,
                              'q': self.getQueenMoves,
                              'k': self.getKingMoves
                              }
        self.whiteToMove = True
        self.moveLog = []
    
    def makeMove(self, move):
        '''
        take a move as a parameter and executes it (this will not work for castling & en-passant)
        '''
        if self.board[move.startRow][move.startCol] != '.':
            self.board[move.startRow][move.startCol] = "."
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move) # log the move so we can undo it later
            self.whiteToMove = not self.whiteToMove #swap player
    def undoMove(self):
        if len(self.moveLog) != 0: # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switch turns back
    
    def getValidMoves(self):
        '''
        All moves considering checks
        for each possible move, check to see if it's a valid move:
            make the move
            generate all possible moves for the opposing player
            see if any of the moves attack your king
            if your king is safe, it's a valid move and add it to list
        return the list of valid moves only
        '''
        return self.getAllPossibleMoves() 

    def getAllPossibleMoves(self):
        '''
        All moves without considering checks
        '''
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0] # generate first character of the piece
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):

                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row,col,moves)
        return moves

    def getPawnMoves(self, row, col, moves):
        '''
        Get all the pawn moves for the pawn located at row, col and add these moves to the list
        '''
        if self.whiteToMove: #white pawn moves
            if self.board[row-1][col] == ".": # 1 square pawn advance
                moves.append(Move((row, col) , (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == '.': # 2 square pawn advance
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col-1>=0: #capture to the left
                if self.board[row-1][col-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row, col) , (row-1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row-1][col+1][0] == 'b': #enemy piece to capture
                    moves.append(Move((row, col) , (row-1, col+1), self.board))

        else: #black pawn moves
            if self.board[row+1][col] == ".":
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == '.':
                    moves.append(Move((row,col), (row+2, col), self.board))
            if col-1 >= 0: #capture to the left
                if self.board[row+1][col-1][0] == 'w': #enemy piece to capture
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col+1 <= 7:
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))
        #TODO: add pawn promotion
            

    def getRookMoves(self, row, col, moves):
        '''
        Get all the rook moves for the pawn located at row, col and add these moves to the list
        '''
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) #up, left, down, right
        enemy_color = "b" if self.whiteToMove else "w"
        for direction in directions:
            for i in range(1,8):
                endRow = row + direction[0] * i
                endCol = col + direction[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <= 7: #check for possible moves only in boundries of the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == ".": #empty space is valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy_color: #capture enemy piece
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else: #friendly piece
                        break
                else: #off board
                    break

    def getKnightMoves(self, row, col, moves):
        '''
        Get all the knight moves for the pawn located at row, col and add these moves to the list
        '''
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2)) #up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.whiteToMove else "b"
        for move in knight_moves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally_color: #so it's either enemy piece or empty equare 
                    moves.append(Move((row, col), (endRow, endCol), self.board))

    def getBishopMoves(self, row, col, moves):
        '''
        Get all the bishop moves for the pawn located at row, col and add these moves to the list
        '''
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1)) #digaonals: up/left up/right down/right down/left
        enemy_color = "b" if self.whiteToMove else "w"    
        for direction in directions:
            for i in range(1, 8):
                endRow = row + direction[0] * i
                endCol = col + direction[1] * i
                if 0 <= endRow <= 7 and 0 <= endCol <=7: #check if the move is on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space is valid
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    elif endPiece[0] == enemy_color: #capture enemy piece
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break
                    else: #friendly piece
                        break
                else: #off board
                    break

    def getQueenMoves(self, row, col, moves):
        '''
        Get all the queen moves for the pawn located at row, col and add these moves to the list
        '''
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        '''
        Get all the king moves for the pawn located at row, col and add these moves to the list
        '''
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        ally_color = "w" if self.whiteToMove else "b"
        for move in king_moves:
            endRow = row + move[0]
            endCol = col + move[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != ally_color:
                    moves.append(Move((row, col), (endRow, endCol), self.board))
class Move():
    '''
    '''

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k,v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        '''
        Param: startSq - tuple
        Param: endSq - tuple
        Param: board (make sure the move is valid)
        '''
        self.startRow = startSq[0] # 3
        self.startCol = startSq[1] # 6
        self.endRow = endSq[0] # 3
        self.endCol = endSq[1] # 4
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] # could be "."
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        '''
        Make chess move to real chess notation

        '''
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, row, col):
        '''
        Helper function to convert row, col to rank file
        0, 0 -> a8

        '''
        return self.colsToFiles[col] + self.rowsToRanks[row]