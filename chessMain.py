from chessEngine import *
from piece import Piece

from graphics2 import *

WIDTH = HEIGHT = 800
DIMENSION = 8 # 8x8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    """
    Initialize a global directory of images.
    This will be called exactly once in the main.
    """
    pieces = ['wp', 'wr', 'wn', 'wb', 'wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        IMAGES[piece] = f"assets/{piece}.png"
    

def createGameWindow(name):
    window = GraphWin(name, WIDTH, HEIGHT, autoflush=False)
    window.setCoords(0, DIMENSION, DIMENSION, 0)

    return window

def drawGameState(window, gameState, validMoves, squareSelected):
    '''
    Responsible for all the graphics within a current state
    '''
    drawBoard(window) # draw squares on the board
    #TODO: pieces highlighting or move suggestion
    highlightSquares(window, gameState, validMoves, squareSelected)
    drawPieces(window, gameState.board)

def drawBoard(window):
    global colors
    colors = [color_rgb(240, 217, 181), color_rgb(181, 136, 99)] # light brown, dark brown
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col) % 2]
            rectangle = Rectangle(Point(row, col), Point(row + 1, col + 1))
            rectangle.setFill(color)
            rectangle.setOutline(color)
            rectangle.draw(window)

def drawPieces(window, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != ".": #not empty square
                # draw pieces
                # pieces = ["bp", "br", "bn", "bb", "bk", "bq", "bp",
                #           "wp", "wr", "wn", "ww", "wk", "wq", "wp",
                #           ]
                pieceObj = Piece(piece, f"assets/{piece}.png", Point(col+0.5, row+0.5))
                pieceObj.draw(window)

# def animateMove(move, window, board):
#     '''
#         Animate a move
#     '''
#     global colors
#     dR = move.endRow - move.startRow # change in row
#     dC = move.endCol - move.startCol # change in col
#     framesPerSquare = 0.1 #frames to move one square
#     frameCount = (abs(dR) + abs(dC)) * framesPerSquare

#     for frame in range(frameCount + 1):
#         row, col = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
#         drawBoard(window)
#         drawPieces(window, board)
#         #erase the piece moved from its ending square
#         color = colors[(move.endRow+move.endCol) %2]
#         endSquare = Rectangle(Point(move.endCol, move.endRow), Point(move.endCol+1, move.endRow+1))
#         endSquare.setFill(color)
#         endSquare.draw(window)
#         #draw captured piece onto rectangle
#         if move.pieceCaptured != '.':
#             Image(Point(endSquare.getCenter().getX(), endSquare.getCenter().getY()), IMAGES[move.pieceMoved]).draw(window)
#         #draw moving piece
#         Image(Point(col+0.5,row+0.5), IMAGES[move.pieceMoved]).draw(window)

def drawText(window, text):
    pass
    # TODO: Draw Text to screen

def highlightSquares(window, gameState, validMoves, squareSelected):
    '''
        Highlight square selected and moves for piece selected
    '''
    if squareSelected != ():
        row, col = squareSelected # 6, 2
        if gameState.board[row][col][0] == ('w' if gameState.whiteToMove else 'b'): # squareSelected is a piece that can be moved
            #highlight selected square
            print(row, col)
            square = Rectangle(Point(col, row), Point(col+1, row+1))
            square.setFill('blue')
            square.draw(window)
            #highlight moves from that square
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    square = Rectangle(Point(move.endCol, move.endRow), Point(move.endCol+1, move.endRow+1))
                    square.setFill('yellow')
                    square.draw(window)



def main():
    window = createGameWindow("Chess")

    gameState = GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False # flag variable for when a move is made
    
    loadImages()  # do this only once before while loop
    running = True
    squareSelected = () # no square is selected, keep track of the last click of the user tuple: (row, col)
    playerClicks = [] # keep track of player clicks (2 tuples: [(6,4), (4,4)])
    gameOver = False
    
    
    drawGameState(window, gameState, validMoves, squareSelected)

    while running:
        if not gameOver:
            keyPressed = window.checkKey()
            clickPt = window.getMouse()
            colX,rowY = int(clickPt.getX()),int(clickPt.getY()) # (x, y) location of mouse click
            if squareSelected == (rowY, colX): #user click same square twice
                squareSelected = () #deselect
                playerClicks = [] # clear player clicks
            else:
                squareSelected = (rowY, colX)
                playerClicks.append(squareSelected) # append for both 1st and 2nd clicks
            if len(playerClicks) == 2: # is 2nd click
                move = Move(playerClicks[0], playerClicks[1], gameState.board)
                print(move.getChessNotation())
                for i in range(len(validMoves)):
                    if move == validMoves[i]:
                        gameState.makeMove(validMoves[i])
                        print(move.getChessNotation())
                        moveMade = True
                        squareSelected = () # reset userClick
                        playerClicks = [] # clear player clicks
                if not moveMade:
                    playerClicks = [squareSelected]

        if moveMade:
            # animateMove(gameState.moveLog[-1], window, gameState.board) abandon for now
            validMoves = gameState.getValidMoves()
            moveMade = False
            
        # key handlers
        if keyPressed == "z":
            gameState.undoMove()
            moveMade = True

        if keyPressed == 'r':
            gameState = GameState()
            validMoves = gameState.getValidMoves()
            squareSelected = ()
            playerClicks = []
            moveMade = False
        
        if keyPressed == "Escape":
            running = False
        
        drawGameState(window, gameState, validMoves, squareSelected)
        if gameState.checkMate:
            gameOver = True
            if gameState.whiteToMove:
                Text(Point(3,3), "Black wins by checkmate").draw(window)
            else:
                Text(Point(3,3), "White wins by checkmate").draw(window)
        elif gameState.staleMate:
            gameOver = True
            Text(Point(3,3), "Stalemate").draw(window)

        
        
        update(30)
        
        
        #TODO: If user quit, running == false

        
        

if __name__ == "__main__":
    main()