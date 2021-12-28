from graphics2 import *


class Piece:
    def __init__(self, type, image, centerPoint):
        self.type = type
        self.image = Image(Point(centerPoint.getX(), centerPoint.getY()), image)

    def draw(self, win):
        self.image.draw(win)

    def move(self):
        pass


def main():
    window = GraphWin("Piece", WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setCoords(0, 8, 8, 0)
    bp = Piece("b", "p", "assets/pieces/bp.png")
    bp.draw(window)


if __name__ == "__main__":
    main()
