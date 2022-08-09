import pygame
from pygame.sprite import Sprite
from pygame import event
from PyGameMinesweeper.Constants import *
import random


def generateBoard(firstClickCoords: (int, int), width: int, height: int, numBombs: int) -> [[int]]:
    """Generates a 2d list of numbers corresponding to board state"""
    board = [[0 for _ in range(width)] for _ in range(height)]

    def calcNum():
        """Calculates all the numbers for the board"""
        # for each point in matrix board
        for r_, row in enumerate(board):
            for c_, pnt in enumerate(row):
                # pnt: int, c: int
                minesAround = 0
                # Find number of mines around initial
                if pnt != -1:
                    for rr in range(-1, 2):
                        for cc in range(-1, 2):
                            if 0 <= r_ + rr < width and 0 <= c_ + cc < height:
                                if board[r_ + rr][c_ + cc] == -1:
                                    minesAround += 1
                    board[r_][c_] = minesAround

    # Continue populating board with bombs until no bombs are left
    while numBombs > 0:
        # iterate through board and column placing bombs as a -1 value
        r = random.randint(0, height - 1)
        c = random.randint(0, width - 1)
        x, y = firstClickCoords
        if (y - 1 <= r <= y + 1 and x - 1 <= c <= x + 1) or board[r][c] == -1:
            pass
        elif numBombs > 0:
            board[r][c] = -1
            numBombs -= 1
    calcNum()
    return board


class BoardButtonSprite(Sprite):
    """Sprite of a button on the minesweeper grid. Default image and state is unclicked, looking up."""

    def __init__(self, tl_point: (int, int), number: int = -3, x=0, y=0):
        super(BoardButtonSprite, self).__init__()
        # GUI, required by the renderer
        self.image = IMAGES.FACING_DOWN
        self.rect = self.image.get_rect().move(*tl_point)
        # Fields
        self.number = number
        self.revealed = False
        self.flagged = False
        self.x = x
        self.y = y

    def setFlagged(self):
        """Changes the image property to a flag and sets the flagged value to true."""
        self.image = IMAGES.FLAG
        self.flagged = True

    def setRevealed(self, doReveal: bool):
        """Changes the image property to the corresponding number value if doReveal is True and changes the revealed
        property."""
        self.revealed = doReveal
        if not doReveal:
            self.image = IMAGES.FACING_DOWN
            self.flagged = False
        else:
            if self.number >= 0:
                self.image = IMAGES.getFromString(f"_{self.number}")
            elif self.number == -1:
                self.image = IMAGES.MINE
            elif self.number == -2:
                self.image = IMAGES.FLAG
            elif self.number == -3:
                self.image = IMAGES.FACING_DOWN
            else:
                raise ValueError("Not a valid integer. Must be between -3 and 8.")

    def reset(self):
        self.image = IMAGES.FACING_DOWN
        self.number = -3
        self.revealed = False
        self.flagged = False

    def onClick(self, mouseButton: int, firstClick: bool, num_mines=30):
        """Modifies the BoardButton based on the mouseButton type. Returns a boardState if firstClick is true,
        otherwise returns None. """
        # firstClick Generation
        if firstClick and mouseButton == 1:
            newBoard = generateBoard((self.x, self.y), CONSTANTS.BOARD_WIDTH, CONSTANTS.BOARD_HEIGHT, num_mines)
            self.number = newBoard[self.y][self.x]
            self.setRevealed(True)
            return num_mines, newBoard
        elif mouseButton == 3:
            # on right click
            if self.flagged:
                event.post(EVENTS.INCREMENT_LABEL)
                self.setRevealed(False)
            elif self.revealed:
                pass
            else:
                event.post(EVENTS.DECREMENT_LABEL)
                self.setFlagged()
        elif mouseButton == 1 and not self.flagged and not self.revealed:
            self.setRevealed(True)
            if self.number == -1:
                event.post(EVENTS.MINE_CLICKED)
        return None

    def __str__(self):
        return f"BoardButton{self.__dict__.items()}"


class ResetButtonSprite(Sprite):
    """Reset button. Calls RESET_CLICKED when clicked."""

    def __init__(self):
        super(ResetButtonSprite, self).__init__()
        self.image = IMAGES.RESET
        self.rect = self.image.get_rect().move(CONSTANTS.SCREEN_WIDTH / 2.25, 20)

    @staticmethod
    def onClick():
        # print("Reset btn was clicked!")
        event.post(EVENTS.RESET_CLICKED)


class CreditButtonSprite(Sprite):
    """Credits button."""

    def __init__(self):
        super(CreditButtonSprite, self).__init__()
        self.image = IMAGES.CREDITS
        self.rect = self.image.get_rect().move(CONSTANTS.SCREEN_WIDTH / 3.25, 20)

    @staticmethod
    def onClick():
        event.post(EVENTS.CREDITS_CLICKED)


class CreditPageSprite(Sprite):
    """Credits page of the creators."""

    def __init__(self):
        super(CreditPageSprite, self).__init__()
        self.image = IMAGES.CREDITS_SIGNATURES
        self.rect = self.image.get_rect().move(0, 100)

    @staticmethod
    def onClick():
        event.post(EVENTS.KILL_CREDITS)


class StatsButtonSprite(Sprite):
    """High score button"""

    def __init__(self):
        super(StatsButtonSprite, self).__init__()
        self.image = IMAGES.STATS
        self.rect = self.image.get_rect().move(CONSTANTS.SCREEN_WIDTH / 1.75, 20)

    @staticmethod
    def onClick():
        event.post(EVENTS.STATS_CLICKED)


class MinesLeftLabelSprite(Sprite):
    """Shows the number of labels left."""

    def __init__(self, numMines: str = "00"):
        super(MinesLeftLabelSprite, self).__init__()
        self.font = FONTS.IMPACT
        mineNumber = self.font.render(str(numMines), True, COLORS.RED, COLORS.BG)
        self.image = mineNumber
        self.rect = self.image.get_rect().move(CONSTANTS.SCREEN_WIDTH * (28 / 34), 10)

    def displayNum(self, num: int):
        """Given an int, displays the number."""
        # Zero in front of ones numbers
        if num < 10:
            num = "0" + str(num)
        self.image = self.font.render(str(num) + "    ", True, COLORS.RED, COLORS.BG)

    @staticmethod
    def onClick():
        pass


class TimerLabelSprite(Sprite):
    """Timer sprite."""

    def __init__(self, time="0:00"):
        super(TimerLabelSprite, self).__init__()
        self.font = FONTS.IMPACT
        timeNumber = self.font.render(str(time), True, COLORS.GREEN, COLORS.BG)
        self.image = timeNumber
        self.rect = self.image.get_rect().move(CONSTANTS.SCREEN_WIDTH * (2 / 34), 10)

    def displayNum(self, num: int):
        """Displays given number"""
        # Converting Ticks to Usable Numbers
        num = num / 1000
        minute = int(num // 60)
        sec = int(num % 60)
        # Zero in front of ones numbers
        if sec < 10:
            sec = "0" + str(sec)
        self.image = self.font.render(str(minute) + ":" + str(sec) + "   ", True, COLORS.GREEN, COLORS.BG)

    @staticmethod
    def onClick():
        pass


class HighScoresSprite(Sprite):
    """Shows the high scores."""

    def __init__(self, file="stats.txt", nullpoint="No scores yet"):
        super(HighScoresSprite, self).__init__()
        self.font = FONTS.IMPACT
        # Reading from file
        if not os.path.exists(file):
            open(file, 'w').close()
        emptyStat = self.font.render(str(nullpoint), True, COLORS.BLACK)
        self.image = emptyStat
        self.rect = self.image.get_rect().move(10, 100)

    def sortScores(self, file="stats.txt"):
        # opens scores as readable only
        if not os.path.exists(file):
            open(file, 'w').close()
        # Reading and writing to the stats file
        with open(file, 'r+') as stats:
            # print("In the file!")
            high_scores = sorted([x.strip() for x in stats])
            stats.seek(0)
            for line, value in enumerate(high_scores):
                stats.writelines(high_scores[line] + "\n")

        # Just reading for statistical purposes, not writing
        with open(file, 'r') as hiScores:
            high_scores = hiScores.readlines(20)
        # rendering doesnt recognize newline characters, we will have to blit positionals
        surfaceList = []

        if len(high_scores) > 0:
            for rank, score in enumerate(high_scores):
                score = str(rank + 1) + ".     " + str(score)
                surfaceList.append(self.font.render(score.strip(), True, COLORS.BLACK))
        else:
            # checking if file is empty
            if os.path.getsize(file) == 0:
                score = "No scores yet"
                # print("FILE IS EMPTY!")
                surfaceList.append(self.font.render(score, True, COLORS.BLACK))
            else:
                # print("This should never happen")
                raise ValueError

        newSurface = pygame.Surface((max(map(lambda item: item.get_width(), surfaceList)),
                                     sum(map(lambda item: item.get_height(), surfaceList))),
                                    pygame.SRCALPHA, 32)
        # Stacking rendered text vertically
        for i, surface in enumerate(surfaceList):
            newSurface.blit(surface, (0, i * surfaceList[0].get_height()))
        self.image = newSurface.convert_alpha()

    @staticmethod
    def onClick():
        event.post(EVENTS.KILL_STATS)


# This could be added in future development of this project
class ResetOptionsSprite(Sprite):
    """Shows reset options. Not used."""
    def __init__(self):
        super(ResetOptionsSprite, self).__init__()
        # todo :: write this
        # self.image =
        # self.rect =

    @staticmethod
    def onClick():
        print("Reset options clicked!")
        event.post(EVENTS.RESET_OPTIONS_CLICKED)


class Explosion(Sprite):
    """Shows the explosion on screen to signify a loss."""
    def __init__(self, screen):
        # todo :: reposition and overlay restart button under YOU LOSE! text
        super(Explosion, self).__init__()
        self.image = IMAGES.EXPLOSION
        x = (screen.get_width() - self.image.get_width()) // 2
        y = (screen.get_height() - self.image.get_height()) // 2
        self.rect = self.image.get_rect().move(x, y)

    def increaseSize(self, screen):
        self.image = pygame.transform.scale(self.image, (self.image.get_width() + 25, self.image.get_height() + 25))
        x = (screen.get_width() - self.image.get_width()) // 2
        y = (screen.get_height() - self.image.get_height()) // 2
        self.rect = self.image.get_rect().move(x, y)

    def resetSize(self, screen):
        self.image = IMAGES.EXPLOSION
        x = (screen.get_width() - self.image.get_width()) // 2
        y = (screen.get_height() - self.image.get_height()) // 2
        self.rect = self.image.get_rect().move(x, y)

    def onClick(self):
        pass


class CakeSprite(Sprite):
    """Shows a cake on screen to signify a win."""
    def __init__(self, screen):
        super(CakeSprite, self).__init__()
        self.image = IMAGES.CAKE
        x = (screen.get_width() - self.image.get_width()) // 2
        y = (screen.get_height() - self.image.get_height()) // 2
        self.rect = self.image.get_rect().move(x, y)

    def onClick(self):
        pass

    def resetSize(self, screen):
        self.image = IMAGES.CAKE
        x = (screen.get_width() - self.image.get_width()) // 2
        y = (screen.get_height() - self.image.get_height()) // 2
        self.rect = self.image.get_rect().move(x, y)

    def increaseSize(self, screen):
        self.image = pygame.transform.scale(self.image, (self.image.get_width() + 25, self.image.get_height() + 25))
        x = (screen.get_width() - self.image.get_width()) // 2
        y = (screen.get_height() - self.image.get_height()) // 2
        self.rect = self.image.get_rect().move(x, y)
