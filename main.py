from graphics2 import *
import random
import time


from button import Button

from game_state import *
from move import *
from piece import Piece
import chess_AI as chessAI

WIDTH = HEIGHT = 700
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
    """
    Crate graphic window of the game
    """
    window = GraphWin(name, WIDTH, HEIGHT, autoflush=False)
    window.setCoords(0, DIMENSION, DIMENSION, 0)

    return window

def drawGameState(window, gameState, validMoves, squareSelected):
    """
    Responsible for all the graphics within a current state
    """
    drawBoard(window) # draw squares on the board
    highlightSquares(window, gameState, validMoves, squareSelected)
    drawPieces(window, gameState.board)

def drawBoard(window):
    global colors
    colors = [color_rgb(238, 238, 210), color_rgb(118, 150, 86)] # light brown, dark brown
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


def drawText(window, point, text, color = 'black', size = 16):
    """
    Draw the text with color, size to window
    """
    text = Text(point, text)
    text.setTextColor(color)
    text.setSize(size)
    text.draw(window)

def highlightSquares(window, gameState, validMoves, squareSelected):
    """
        Highlight square selected and moves for piece selected
    """
    if squareSelected != ():
        row, col = squareSelected # 6, 2
        if gameState.board[row][col][0] == ('w' if gameState.whiteToMove else 'b'): # squareSelected is a piece that can be moved
            #highlight selected square
            square = Rectangle(Point(col, row), Point(col+1, row+1))
            square.setFill(color_rgb(226, 151, 85))
            square.setOutline(color_rgb(226, 151, 85))
            square.draw(window)
            #highlight moves from that square
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    square = Rectangle(Point(move.endCol, move.endRow), Point(move.endCol+1, move.endRow+1))
                    square.setFill(color_rgb(247, 247, 106))
                    # square.setOutline(color_rgb(247, 247, 106))
                    square.draw(window)


def displayOpeningScreenAndSettings():
    """
        Opening And Settings Screen
    """
    window = GraphWin("Graphic Chess", WIDTH, HEIGHT)
    backgroundImg = Image(Point(50, 50), "assets/backdrop.png")
    backgroundImg.draw(window)
    window.setCoords(0, 100, 100, 0)

    drawText(window, Point(50,14), "Welcome to Graphic Chess!", "green", 36)

    drawText(window, Point(50,30), "Use MOUSE to move your piece\n(Hit Z to undo move, Hit ESCAPE to quit)" , "black", 15)

    drawText(window, Point(50,40), "Choose your option:" , "green", 16)

    startButton1 = Button(Point(25, 55), 35, 12, "Human vs Human")
    startButton1.draw(window)
    startButton1.activate()

    startButton2 = Button(Point(70, 55), 35, 12, "Human vs AI")
    startButton2.draw(window)
    startButton2.activate()

    startButton3 = Button(Point(48, 70), 35, 12, "AI vs AI")
    startButton3.draw(window)
    startButton3.activate()

    ready = False
    playOption = None

    while not ready:
        clickPt = window.getMouse()
        if startButton1.isClicked(clickPt):
            playOption = 1
            ready = True
        elif startButton2.isClicked(clickPt):
            playOption = 2
            ready = True
        elif startButton3.isClicked(clickPt):
            playOption = 3
            ready = True
        
    window.close()

    return playOption

def playGame(playChoice):
    """
        Main Playscreen
    """
    window = createGameWindow("Chess")

    gameState = GameState()
    validMoves = gameState.getValidMoves()
    moveMade = False # flag variable for when a move is made
    
    loadImages()  # do this only once before while loop
    running = True
    squareSelected = () # no square is selected, keep track of the last click of the user tuple: (row, col)
    playerClicks = [] # keep track of player clicks (2 tuples: [(6,4), (4,4)])
    gameOver = False
    
    playerOne = None # if a human is playing white, this will be True. If an AI is playing False
    playerTwo = None # same as above but for black

    if playChoice == 1: # Human vs Human
        playerOne = True
        playerTwo = True
    elif playChoice == 2: # Human vs AI
        randomChoice = random.randint(0,2)
        if randomChoice == 1:
            playerOne = True
            playerTwo = False
        else:
            playerOne = False
            playerTwo = True
    else: # AI vs AI
        playerOne = False
        playerTwo = False
    
    drawGameState(window, gameState, validMoves, squareSelected)
    playerWon = None
    while running:
        keyPressed = window.checkKey()
        humanTurn = (gameState.whiteToMove and playerOne) or (not gameState.whiteToMove and playerTwo)

        if not gameOver and humanTurn:
            
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
                for i in range(len(validMoves)):
                    if move == validMoves[i]:
                        gameState.makeMove(validMoves[i])
                        print(validMoves[i].getChessNotation())
                        moveMade = True
                        squareSelected = () # reset userClick
                        playerClicks = [] # clear player clicks
                if not moveMade:
                    playerClicks = [squareSelected]
        
        #AI move finder
        if not gameOver and not humanTurn:
            AIMove = chessAI.findRandomMove(validMoves)
            gameState.makeMove(AIMove)
            moveMade = True

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
        update(30)
        drawGameState(window, gameState, validMoves, squareSelected)
        
        if gameState.checkMate or gameState.staleMate:
            running = False
            gameOver = True
        
    if gameState.checkMate:
        if gameState.whiteToMove:
            drawText(window, Point(4,4), "Black wins by checkmate", "black", 25)
            playerWon = ("Black", "Human" if playerTwo else "AI")
        else:
            drawText(window, Point(4,4), "White wins by checkmate", "black", 25)
            playerWon = ("White", "Human" if playerOne else "AI")
    elif gameState.staleMate:
        drawText(window, Point(4,4), "Stalemate!", "black", 25)
        playerWon = "Draw"
    
    update(30)
    time.sleep(3)
    window.close()
    return playerWon

def displayGameOverScreen(playerWon):
    """Displays the "Game Over" screen, with an appropriate message depending whether
    the playerWon parameter is can be a string or tuple"""

    # Loop until the user clicks on one of them, or closes the window.
    # close the window, and return True if the user wants to play again...
    window = GraphWin("Game Over", WIDTH, HEIGHT)
    backgroundImg = Image(Point(50, 50), "assets/backdrop.png")
    backgroundImg.draw(window)
    window.setCoords(0, 100, 100, 0)


    if playerWon:
        finalText = Text(
            Point(50, 30),
            "Good Game!\nCongratulations! " + ("It's a Draw!" if len(playerWon) == 1 else f"{playerWon[0]} {playerWon[1]} win!"),
        )
        finalText.setTextColor("black")
        finalText.setSize(25)
        finalText.draw(window)
    else:
        finalText = Text(
            Point(50, 30),
            "Oops! You cancel the game",
        )
        finalText.setTextColor("brown")
        finalText.setSize(30)
        finalText.draw(window)            


    playAgainButton = Button(Point(30, 70), 30, 12, "Play Again!")
    playAgainButton.draw(window)
    playAgainButton.activate()

    quitButton = Button(Point(70, 70), 30, 12, "Quit.")
    quitButton.draw(window)
    quitButton.activate()

    click = window.getMouse()
    if playAgainButton.isClicked(click):
        window.close()
        return True
    if quitButton.isClicked(click):
        window.close()
        return False



def main():
    """
    main method of the game
    """
    playAgain = True

    while playAgain:
        playChoice = displayOpeningScreenAndSettings()
        playerWon = playGame(playChoice)

        playAgain = displayGameOverScreen(playerWon)


if __name__ == "__main__":
    main()