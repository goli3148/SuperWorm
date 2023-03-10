import random
import pygame
import sys
from pygame.locals import *
import threading
from random import randrange

FPS = 4.65
WINDOWWIDTH = 720
WINDOWHEIGHT = 480
CELLSIZE = 20
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE = (255, 255, 255)
DARKGRAY = (40,  40,  40)
BLACK = (0,   0,   0)
ROSE = (255, 170, 200)
RED = (255,   0,   0)
ORANGE = (255, 130, 40)
GOLD = (255, 200, 10)
YELLOW = (255, 240, 0)
GREEN = (0,  255,   0)
DARKGREEN = (0,   150,   0)
TAEL = (0,   200,   160)
DARKTAEL = (0,   175,   150)
AQUA = (0,   200,   200)
DARKAQUA = (0,   150,   150)
BLUE = (0,  0,  255)
PURPLE = (160,  70,  160)
LAVENDER =(200, 190, 230)
BGCOLOR = WHITE

COLOR_ARRAY = [(255, 170, 200), (40,  40,  40), (0,   0,   0), (255,   0,   0), (255, 130, 40), (255, 200, 10),
               (255, 240, 0), (0,  255,   0), (0,   150,   0), (0,   200,   160), (0,   175,   150),
               (0,   200,   200), (0,   150,   150), (0,  0,  255), (160,  70,  160), (200, 190, 230)]

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # syntactic sugar: index of the worm's head

# SCORE AND LEVEL GLOBAL
SCORE_WORM_COORDS = 0
LEVEL = 1

# Variable for thread termination
TERMINATE = False

# Variables for fruit and worm color
FRUIE_COLOR = RED
SNAKE_COLOR = GREEN

# Max Score Saving
MAX_SCORE = 0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('ITCKRIST.TTF', 20)
    pygame.display.set_caption('Super Worm')

    showStartScreen()
    while True:
        RunGame()
        showGameOverScreen()


def RunGame():
    global SCORE_WORM_COORDS, LEVEL
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    pygame.mixer.music.load('Game theme.wav')
    pygame.mixer.music.play(-1, 0.0)
        
    
    # Start the fruit in a random place.
    fruit = getRandomLocation()

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
          if event.type == QUIT:
              terminate()
          elif event.type == KEYDOWN:
            if (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
            elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
            elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
            elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return  # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == fruit['x'] and wormCoords[HEAD]['y'] == fruit['y']:
            # don't remove worm's tail segment
            fruit = getRandomLocation()  # set a new fruit somewhere
        else:
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'],
                       'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'],
                       'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]
                       ['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]
                       ['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        # drawGrid()
        drawWorm(wormCoords)
        drawfruit(fruit)
        
        # SCORE AND LEVEL CALAULATIONS
        score = len(wormCoords)-3
        SCORE_WORM_COORDS = score
        level = LEVEL
        drawScore(score)
        drawLevel(level)
        drawMaxScore()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        

def drawPressKeyMsg():
    pressKey = pygame.font.Font('ITCKRIST.TTF', 11)
    pressKeySurf = pressKey.render('Press key P to play or Press key -end- to Exit.', True, DARKGRAY, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 250, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def drawPressKeyinTheScreenGameOverMsg():
    pressKey = pygame.font.Font('ITCKRIST.TTF', 11)
    pressKeySurf = pressKey.render('Press key P to play Again or Press key -end- to Exit.', True, DARKGRAY, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 260, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_END:
        terminate()
    return keyUpEvents[0].key

def showStartScreen():
    titleFont = pygame.font.Font('ITCKRIST.TTF', 70)
    titleSurf1 = titleFont.render('Super Worm', True, AQUA, BGCOLOR)
    pygame.mixer.music.load('Start Screen.mp3')
    pygame.mixer.music.play(-1, 0.0)
    
    degrees1 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH/2, WINDOWHEIGHT/8)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)
        # startimg = pygame.image.load('Botton.jpg')
        # startimgrect = startimg.get_rect()
        # startimgrect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/1.25)
        # DISPLAYSURF.blit(startimg, startimgrect)
        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        
def terminate():
    global TERMINATE
    pygame.quit()
    TERMINATE = True
    sys.exit(0)


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('ITCKRIST.TTF', 90)
    gameOverSurf = gameOverFont.render('Game Over', True, WHITE, BLACK)
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('Game over.wav')
    music.play()

    degrees2 = 0
    
    while True:
        rotatedSurf2 = pygame.transform.rotate(gameOverSurf, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)
        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
 
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawLevel(level):
    levelSurf = BASICFONT.render('Level: %s' % (level), True, BLACK)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 120, 30)
    DISPLAYSURF.blit(levelSurf, levelRect)
    
def drawMaxScore():
    global MAX_SCORE
    mxS = BASICFONT.render('MAX SCORE: %s' % (MAX_SCORE), True, BLACK)
    mxR = mxS.get_rect()
    mxR.topleft = (WINDOWWIDTH-300, 10)
    DISPLAYSURF.blit(mxS, mxR)

def drawWorm(wormCoords):
    global SNAKE_COLOR
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, SNAKE_COLOR, wormInnerSegmentRect)


def drawfruit(coord):
    global FRUIE_COLOR
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    fruitRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, FRUIE_COLOR, fruitRect)


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0, y), (WINDOWWIDTH, y))


# thread for score and level calculation
def SCORE_LEVEL_CALC__THREAD():
    global SCORE_WORM_COORDS, LEVEL, TERMINATE, FRUIE_COLOR, SNAKE_COLOR, COLOR_ARRAY, FPS, MAX_SCORE
    score = SCORE_WORM_COORDS
    while not TERMINATE:
        if not score == SCORE_WORM_COORDS:
            score = SCORE_WORM_COORDS
            # Exponential function for leveling the game
            # Color and Fruit gets random color after level up
            # Game gets more speed after level up
            if score==int(pow(LEVEL, 1.2)*2):
                LEVEL+=1
                FRUIE_COLOR = COLOR_ARRAY[randrange(len(COLOR_ARRAY))]
                SNAKE_COLOR = COLOR_ARRAY[randrange(len(COLOR_ARRAY))]
                FPS+=1
            if score == 0:
                FPS = 4.65
            if score > MAX_SCORE:
                MAX_SCORE = score
            
        
    
    
threading.Thread(target=SCORE_LEVEL_CALC__THREAD).start()
if __name__ == '__main__':
    main()
