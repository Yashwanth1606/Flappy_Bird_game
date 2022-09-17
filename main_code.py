# This is the first game code i am creating 
# Flappy Bird Game

import random  # for genrating random numbers
import sys  # 
import pygame # to create game 
from pygame.locals import *

# global variable for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511

SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8 

GAME_SPRITES = {}

GAME_SOUNDS = {}

PLAYER = 'gallery/sprites/bird.png'

BACKGROUND = 'gallery/sprites/background2.png'

PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():
    # shows welcome screen on the screen

    playerx = int(SCREENWIDTH/5) # here we set for the width for were the player image(bird) has to shown
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2) #here we set the height of the player by sub the birds height and divding by 2 to center the bird
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2) #here we displaying the image to center
    messagey = int(SCREENHEIGHT * 0.10) #here display image to some center
    basex = 0

    while True:
        for event in pygame.event.get():
            # if user clicks on the cross button close the game
            if event.type ==  QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                # in above line event.type is to check the what event does he user has inputed
                # KEYDOWN is check that user presssed any key
                # K_ESCAPE IS BUILT IN FUNCTOION IN THE pygame module to chech weather escape keyword is pressed
                pygame.quit()
                sys.exit()
            # if the user clicks on upword key and sapcebar starts the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0)) # here display the backgrond image again and again at (0,0 ) cordinates
                SCREEN.blit(GAME_SPRITES['player'], (playerx,playery)) # here display the player image again and again 
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey)) # here display the message image again and again
                SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY)) # here display the base image again and again
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0
# here we are writing code to generate and bliting  of random pipes in the game
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2) , 'y':newPipe2[0]['y']},

    ]
    
    # my list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2) , 'y':newPipe2[1]['y']},

    ]

    pipeVelX = -4 # to make the pipe move left that is -x direction

    playerVelY = -9
    playerMaxY = 10
    playerMinY = -8
    playeraccY = 1

    playerFlapAcc = -8 # velocity while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        
        crashtest = isCollide(playerx, playery, upperPipes, lowerPipes) # this funtion will return true if player is crashed
        if crashtest:
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipes in upperPipes:
            pipeMidPos = pipes['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score +=1
                print(f"your score is{score}")
                GAME_SOUNDS['point'].play()


        if playerVelY < playerMaxY and not playerFlapped:
            playerVelY += playeraccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)


        # move pipes to left
        for upperPipe , lowerPipe  in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to leave the screen
        if 0 < upperPipes[0]['x'] < 5 :
            newpipe = getRandomPipe ( )
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if pipe is out of the screen , remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe , lowerPipe  in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
        
        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))

        mydigts = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigts:
            width += GAME_SPRITES['numbers'][digit].get_width()
        xoffset = (SCREENWIDTH - width)/2

        for digit in mydigts:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset,SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY -25 or playery <0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes :
        if ( playery + GAME_SPRITES ['player'].get_height()>pipe['y']) and abs(playerx - pipe ['x']) < GAME_SPRITES ['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False

def getRandomPipe():
    # genrating postions of two pipes for bliting on the screen (bottom and up (rotated))
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset)) 
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX , 'y' : -y1}, # upper pipes
        {'x': pipeX , 'y' : y2} # lower pipes
    ]
    return pipe

if __name__ == '__main__' : # This line is ensure that the file is being executed from the main file and not being imported
    # Main code to start the game startsfrom here
    pygame.init() # this line intializes all the modules in the py game
    FPSCLOCK = pygame.time.Clock() # here we can control the frames per second 
    pygame.display.set_caption('Flappybird by Yashwanth') # here we creating the caption for game window
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
     ) # here we loaded the images of 0 to 9 numbers to the GAME_SPRITES dictionaries

    GAME_SPRITES['message'] =  pygame.image.load('gallery/sprites/message1.png') # this is dispaly a message before game starts
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png') # this crestes the base of the game

    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180), # this is to create backwards pipe 
        pygame.image.load(PIPE).convert_alpha(),
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND)
    GAME_SPRITES['player'] = pygame.image.load(PLAYER)

    # here intilize the game sounds for the game 
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

while True:
    welcomeScreen() # this will dispaly welcome sreen until play is pressed any button in the keyboard
    mainGame() # this is the main function