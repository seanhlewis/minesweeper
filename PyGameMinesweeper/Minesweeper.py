import sys
import pygame
from pygame.sprite import RenderUpdates
from PyGameMinesweeper.Constants import *
from PyGameMinesweeper.Constructs import OrderedSet
import PyGameMinesweeper.Sprites as Sprites


def revealAdjacentOpenSpaces(clickedBoardButton: Sprites.BoardButtonSprite,
                             boardOfSprites: [[Sprites.BoardButtonSprite]]):
    """Reveals adjacent empty buttons and the numbers around those empty squares."""
    checkedEmpty = set()
    checkedEdge = set()
    unchecked = OrderedSet()
    unchecked.add((clickedBoardButton.x, clickedBoardButton.y))
    # iterator variables
    uncheckedLength = len(unchecked)
    while uncheckedLength > 0:
        point = unchecked[0]
        for r in range(-1, 2):
            for c in range(-1, 2):
                x, y = point[0] + c, point[1] + r
                if r == 0 and c == 0:
                    continue
                if 0 <= y < CONSTANTS.BOARD_HEIGHT and 0 <= x < CONSTANTS.BOARD_WIDTH:
                    # print(f"Checking {x}, {y} with a value of {boardOfSprites[y][x]}")
                    if boardOfSprites[y][x].number == 0 and (x, y) not in checkedEmpty:
                        unchecked.add((x, y))
                    elif boardOfSprites[y][x].number > 0 and (x, y) not in checkedEmpty:
                        checkedEdge.add((x, y))
        checkedEmpty.add(unchecked.pop(0))
        uncheckedLength = len(unchecked)
    # Reveal all
    for x, y in checkedEmpty:
        boardOfSprites[y][x].setRevealed(True)
    for x, y in checkedEdge:
        boardOfSprites[y][x].setRevealed(True)
    return None


def revealBoard(sprites: [[Sprites.BoardButtonSprite]]):
    """Reveals the entire board. Used for debugging."""
    for row in sprites:
        for sprite in row:
            sprite.setRevealed(True)


def resetBoard(sprites: [[Sprites.BoardButtonSprite]]):
    """Resets the gui of all the sprites"""
    for row in sprites:
        for sprite in row:
            sprite.reset()


def drawStartingBoard(rows: int, cols: int, screen_, vOffset: int = 100) \
        -> (RenderUpdates, [[Sprites.BoardButtonSprite]]):
    """Draws the starting board onto the given screen. Returns the renderer and sprite_list."""
    renderer = RenderUpdates()
    sprite_list = []
    CONSTANTS.BOARD_WIDTH = cols
    CONSTANTS.BOARD_HEIGHT = rows
    for r in range(rows):
        row = []
        for c in range(cols):
            x = CONSTANTS.BTN_WIDTH * c + CONSTANTS.SCREEN_PADDING
            y = CONSTANTS.BTN_WIDTH * r + CONSTANTS.SCREEN_PADDING + vOffset
            row.append(Sprites.BoardButtonSprite((x, y), x=c, y=r))
        sprite_list.append(row)
    renderer.add(*sprite_list)
    renderer.draw(screen_)
    return renderer, sprite_list


def boardIsWin(sprites: [[Sprites.BoardButtonSprite]]):
    """Checks the board for a win."""
    for row in sprites:
        for sprite in row:
            if (sprite.revealed != True and sprite.flagged != True) or (sprite.number > 0 and sprite.flagged):
                # print(f"Failed at {sprite.x} {sprite.y}: {sprite}")
                return False
    # At this point, all mines should be flagged and non-mine sprites should be revealed
    for row in sprites:
        for sprite in row:
            if sprite.number == -1 and not sprite.flagged:
                # print(f"Mine check failed at {sprite.x} {sprite.y}")
                return False
    return True


def start_game_loop():
    """Main game loop that updates the GUI on the screen."""
    # Starting pygame
    pygame.init()

    # More window settings
    pygame.display.set_caption("Minesweeper")
    pygame.display.set_icon(IMAGES.MINE)
    screen_ = pygame.display.set_mode((CONSTANTS.SCREEN_WIDTH, CONSTANTS.SCREEN_HEIGHT), pygame.RESIZABLE)

    # Initial variables
    otherButtonRenderer = RenderUpdates()
    resetBtn = Sprites.ResetButtonSprite()
    resetOptions = Sprites.ResetOptionsSprite()
    minesLabel = Sprites.MinesLeftLabelSprite()
    timerLabel = Sprites.TimerLabelSprite()
    explosion = Sprites.Explosion(screen_)
    cake = Sprites.CakeSprite(screen_)
    creditsBtn = Sprites.CreditButtonSprite()
    creditsPg = Sprites.CreditPageSprite()
    statsBtn = Sprites.StatsButtonSprite()
    highscores = Sprites.HighScoresSprite()

    # Adding to the render
    otherButtonRenderer.add(timerLabel, resetBtn, resetOptions, minesLabel, creditsBtn, statsBtn)

    creds_showing = False
    stats_showing = False
    firstClick = True
    minesLeft = 0

    # todo :: comment these after you finish their respective classes
    resetOptions.kill()

    # Initial rendering
    screen_.fill(COLORS.BG)
    boardRenderer, boardOfSprites = drawStartingBoard(CONSTANTS.BOARD_HEIGHT, CONSTANTS.BOARD_WIDTH, screen_)
    # Blitting mine image for minesLeft
    sprite_mine = IMAGES.MINE
    screen_.blit(sprite_mine, (CONSTANTS.SCREEN_WIDTH * (24 / 34), 20))

    # Initial timer variables
    clock = pygame.time.Clock()
    current_time = 0
    start_time = 0
    elapsed_time = 0
    timerInst = False
    timerStop = False

    while True:
        for event_ in pygame.event.get():
            # Handling exiting program
            if event_.type == pygame.QUIT:
                sys.exit()

            # Handling window resize
            elif event_.type == pygame.VIDEORESIZE:
                screen_ = pygame.display.set_mode((event_.w, event_.h), pygame.RESIZABLE)
                boardRenderer.draw(screen_)
                screen_.fill(COLORS.BG)

            # Handling a losing board
            elif event_ == EVENTS.LOSE_GAME:
                print("lost")

            # Handling clicks
            elif event_.type == pygame.MOUSEBUTTONDOWN:
                x, y = event_.pos
                # Finding board button that was clicked
                clickedBoardButton = None
                for row in boardOfSprites:
                    for btn in row:
                        if btn.rect.collidepoint(x, y):
                            clickedBoardButton = btn
                # Find if other button was clicked instead
                for sprite in otherButtonRenderer.sprites():
                    if sprite.rect.collidepoint(x, y):
                        # Note: all of these sprites are from Sprites.py and have all implemented the onClick function
                        sprite.onClick()
                # If both clickedBoardButton and event.button exist
                if event_.button and clickedBoardButton and timerStop is False:
                    ans = clickedBoardButton.onClick(event_.button, firstClick, num_mines=20)
                    # If a board was given
                    if ans is not None:
                        num_mines, boardData = ans
                        firstClick = False
                        current_time = 0
                        minesLeft = num_mines
                        minesLabel.displayNum(minesLeft)
                        for r, row in enumerate(boardOfSprites):
                            for c, spriteBtn in enumerate(row):
                                spriteBtn.number = boardData[r][c]
                        # revealBoard(boardOfSprites)
                    if clickedBoardButton.number == 0 and clickedBoardButton.revealed is True:
                        revealAdjacentOpenSpaces(clickedBoardButton, boardOfSprites)
                    # Checking board is valid to check for a win
                    if boardIsWin(boardOfSprites):
                        pygame.event.post(EVENTS.WIN_GAME)

            # Handling custom events
            elif event_ == EVENTS.DECREMENT_LABEL:
                minesLeft -= 1
                minesLabel.displayNum(minesLeft)
            elif event_ == EVENTS.INCREMENT_LABEL:
                minesLeft += 1
                minesLabel.displayNum(minesLeft)
            elif event_ == EVENTS.RESET_CLICKED:
                resetBoard(boardOfSprites)
                firstClick = True
                minesLabel.displayNum(0)
                # Timer Reset
                current_time = 0
                timerStop = False
                timerLabel.__init__()
            elif event_ == EVENTS.MINE_CLICKED:
                # this is our lose condition
                otherButtonRenderer.add(explosion)
                pygame.event.post(EVENTS.DECREMENT_LABEL)
                pygame.time.set_timer(EVENTS.GROW_EXPLOSION, 1000 // 100, loops=10)
                pygame.time.set_timer(EVENTS.KILL_EXPLOSION, 1000, loops=1)
            elif event_ == EVENTS.GROW_EXPLOSION:
                explosion.increaseSize(screen_)
            elif event_ == EVENTS.KILL_EXPLOSION:
                explosion.kill()
                explosion.resetSize(screen_)
                # Need to fill screen because kill doesnt remove explosion from screen
                screen_.fill(COLORS.BG)
                screen_.blit(sprite_mine, (CONSTANTS.SCREEN_WIDTH * (24 / 34), 20))
                # reset board
                pygame.event.post(EVENTS.RESET_CLICKED)
            # Win Condition Event
            elif event_ == EVENTS.WIN_GAME:
                print("Winning game board!")
                otherButtonRenderer.add(cake)
                pygame.time.set_timer(EVENTS.GROW_CAKE, 1000 // 100, loops=10)
                pygame.time.set_timer(EVENTS.KILL_CAKE, 1000, loops=1)
                # Adding time to stats.txt for score
                timerStop = True
                with open("stats.txt", 'a') as scores:
                    # Converting elapsed_time into usable numbers
                    elapsed_time = elapsed_time / 1000
                    minute = int(elapsed_time // 60)
                    sec = int(elapsed_time % 60)
                    if sec < 10:
                        sec = "0" + str(sec)
                    scores.write(str(minute)+":"+str(sec) + "\n")
            # Deleting Win Sprite Event
            elif event_ == EVENTS.KILL_CAKE:
                cake.kill()
                cake.resetSize(screen_)
                # Need to fill screen because kill doesnt remove cake from screen
                screen_.fill(COLORS.BG)
                screen_.blit(sprite_mine, (CONSTANTS.SCREEN_WIDTH * (24 / 34), 20))
            # Size Modifier for Win Sprite Event
            elif event_ == EVENTS.GROW_CAKE:
                cake.increaseSize(screen_)
            # Credits Button Click Event
            elif event_ == EVENTS.CREDITS_CLICKED:
                otherButtonRenderer.add(creditsPg)
                # print("credits clicked!")
                # simple switch boolean to kill on second press of button
                if not creds_showing:
                    creds_showing = True
                else:
                    creditsPg.kill()
                    creds_showing = False
            # Deleting Credits Page Event
            elif event_ == EVENTS.KILL_CREDITS:
                # kills the credits page on clicking the image
                creditsPg.kill()
            # Stats Button Click Event
            elif event_ == EVENTS.STATS_CLICKED:
                highscores.sortScores()
                otherButtonRenderer.add(highscores)
                #print("stats clicked!")
                # simple switch boolean to kill on second press of button
                if not stats_showing:
                    stats_showing = True
                else:
                    highscores.kill()
                    stats_showing = False
            # Deleting Stats Page Event
            elif event_ == EVENTS.KILL_STATS:
                # kills the stats page on clicking the stats
                highscores.kill()

        # Update the screen
        boardRenderer.draw(screen_)
        otherButtonRenderer.draw(screen_)
        pygame.display.flip()

        # TIMER UPDATES
        # Runs once only when game has begun
        if not firstClick:
            if not timerInst:
                start_time = pygame.time.get_ticks()
                timerInst = True
            # Updating until the game is won
            elif not timerStop:
                elapsed_time = current_time - start_time
                timerLabel.displayNum(elapsed_time)
        else:
            start_time = pygame.time.get_ticks()

        # Update the timer
        current_time = pygame.time.get_ticks()
        # print(current_time)
        # 60fps clock
        clock.tick(60)
