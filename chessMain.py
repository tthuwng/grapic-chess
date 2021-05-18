from chessEngine import *
from piece import Piece

from graphics2 import *

WIDTH = HEIGHT = 512
DIMENSION = 8 # 8x8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


# def loadImages():
    

def createGameWindow(name):
    window = GraphWin(name, WIDTH, HEIGHT, autoflush=False)
    window.setCoords(0, DIMENSION, DIMENSION, 0)

    return window

def drawGameState(window, gameState):
    '''
    Responsible for all the graphics within a current state
    '''
    drawBoard(window) # draw squares on the board
    #TODO: pieces highlighting or move suggestion
    drawPieces(window, gameState.board)

def drawBoard(window):
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


def main():
    window = createGameWindow("Chess")

    gameState = GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False # flag variable for when a move is made
    
    
    running = True
    squareSelected = () # no square is selected, keep track of the last click of the user tuple: (row, col)
    playerClicks = [] # keep track of player clicks (2 tuples: [(6,4), (4,4)])
    drawGameState(window, gameState)
    while running:
        keyPressed = window.checkKey()
        # key handlers
        
            

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
            if move in validMoves:
                gameState.makeMove(move)
                print(move.getChessNotation())
                moveMade = True
                squareSelected = () # reset userClick
                playerClicks = [] # clear player clicks
            else:
                playerClicks = [squareSelected]

        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False

        if keyPressed == "z":
            gameState.undoMove()
            moveMade = True

        
        if keyPressed == "Escape":
            running = False
        drawGameState(window, gameState)
        update(30)
        
        
        #TODO: If user quit, running == false

        
        

if __name__ == "__main__":
    main()