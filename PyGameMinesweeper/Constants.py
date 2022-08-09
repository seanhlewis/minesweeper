import pygame.font
from pygame import transform, image, USEREVENT, event, font
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
pygame.font.init()


def _getPath(path: str):
    """Gets the current path to runtime directory."""
    pt = os.path.join(dir_path, path)
    return pt


class CONSTANTS:
    """List of miscellaneous constants."""
    SCREEN_WIDTH = 6 + 50 * 10
    SCREEN_HEIGHT = 6 + 50 * 10 + 100
    SCREEN_PADDING = 3
    BTN_DIM = BTN_WIDTH, BTN_HEIGHT = 50, 50
    BOARD_DIM = BOARD_WIDTH, BOARD_HEIGHT = 10, 10
    MINES_DEFAULT = 30


class IMAGES:
    """A bunch of resized images."""
    FACING_DOWN = transform.scale(image.load(_getPath("res/facingDown.png")), CONSTANTS.BTN_DIM)
    FLAG = transform.scale(image.load(_getPath("res/flagged.png")), CONSTANTS.BTN_DIM)
    MINE = transform.scale(image.load(_getPath("res/bomb.png")), CONSTANTS.BTN_DIM)
    RESET = transform.scale(image.load(_getPath("res/resetButton.png")), CONSTANTS.BTN_DIM)
    _0 = transform.scale(image.load(_getPath("res/0.png")), CONSTANTS.BTN_DIM)
    _1 = transform.scale(image.load(_getPath("res/1.png")), CONSTANTS.BTN_DIM)
    _2 = transform.scale(image.load(_getPath("res/2.png")), CONSTANTS.BTN_DIM)
    _3 = transform.scale(image.load(_getPath("res/3.png")), CONSTANTS.BTN_DIM)
    _4 = transform.scale(image.load(_getPath("res/4.png")), CONSTANTS.BTN_DIM)
    _5 = transform.scale(image.load(_getPath("res/5.png")), CONSTANTS.BTN_DIM)
    _6 = transform.scale(image.load(_getPath("res/6.png")), CONSTANTS.BTN_DIM)
    _7 = transform.scale(image.load(_getPath("res/7.png")), CONSTANTS.BTN_DIM)
    _8 = transform.scale(image.load(_getPath("res/8.png")), CONSTANTS.BTN_DIM)
    EXPLOSION = transform.scale(image.load(_getPath("res/explosion.png")), (280, 280))
    CAKE = transform.scale(image.load(_getPath("res/cake.png")), (280, 280))
    CREDITS = transform.scale(image.load(_getPath("res/people.png")), CONSTANTS.BTN_DIM)
    CREDITS_SIGNATURES = transform.scale(image.load(_getPath("res/credits.png")), (500, 500))
    STATS = transform.scale(image.load(_getPath("res/stats.png")), CONSTANTS.BTN_DIM)

    @staticmethod
    def getFromString(item: str):
        return {"FACING_DOWN": IMAGES.FACING_DOWN,
                "FLAG": IMAGES.FLAG,
                "MINE": IMAGES.MINE,
                "_0": IMAGES._0,
                "_1": IMAGES._1,
                "_2": IMAGES._2,
                "_3": IMAGES._3,
                "_4": IMAGES._4,
                "_5": IMAGES._5,
                "_6": IMAGES._6,
                "_7": IMAGES._7,
                "_8": IMAGES._8}.get(item, None)


class COLORS:
    """A bunch of color constants."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BG = (185, 185, 185)
    RED = (255, 0, 0)
    GREEN = (0, 159, 42)


class EVENTS:
    """A list of custom user events."""
    RESET_CLICKED = event.Event(USEREVENT + 1)
    MINE_LABEL_CLICKED = event.Event(USEREVENT + 2)
    INCREMENT_LABEL = event.Event(USEREVENT + 3)
    DECREMENT_LABEL = event.Event(USEREVENT + 4)
    RESET_OPTIONS_CLICKED = event.Event(USEREVENT + 5)
    MINE_CLICKED = event.Event(USEREVENT + 6)
    GENERATE_BOARD = event.Event(USEREVENT + 7)
    WIN_GAME = event.Event(USEREVENT + 8)
    LOSE_GAME = event.Event(USEREVENT + 9)
    GROW_EXPLOSION = event.Event(USEREVENT + 10)
    KILL_EXPLOSION = event.Event(USEREVENT + 11)
    GROW_CAKE = event.Event(USEREVENT + 12)
    KILL_CAKE = event.Event(USEREVENT + 13)
    CREDITS_CLICKED = event.Event(USEREVENT + 14)
    KILL_CREDITS = event.Event(USEREVENT + 15)
    STATS_CLICKED = event.Event(USEREVENT + 16)
    WRITE_STATS = event.Event(USEREVENT + 17)
    KILL_STATS = event.Event(USEREVENT + 18)


class FONTS:
    """List of fonts used in this project."""
    IMPACT = font.Font(_getPath("res/IMPACT.TTF"), 60)
