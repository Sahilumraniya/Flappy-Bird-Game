from random import randint
import pygame
import pygame.locals
import sys

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Brid by Sahil Umraniya")
pygame.display.set_icon(pygame.image.load("images/bird.png"))

GAME_IMGES = {
    "background": pygame.image.load("images/Background.png").convert_alpha(),
    "bird": pygame.image.load("images/bird.png").convert_alpha(),
    "lossBird": pygame.image.load("images/loss_bird.png").convert_alpha(),
    "ground": pygame.image.load("images/ground.png").convert_alpha(),
    "digits" : (
        pygame.image.load("images/0.png").convert_alpha(),
        pygame.image.load("images/1.png").convert_alpha(),
        pygame.image.load("images/2.png").convert_alpha(),
        pygame.image.load("images/3.png").convert_alpha(),
        pygame.image.load("images/4.png").convert_alpha(),
        pygame.image.load("images/5.png").convert_alpha(),
        pygame.image.load("images/6.png").convert_alpha(),
        pygame.image.load("images/7.png").convert_alpha(),
        pygame.image.load("images/8.png").convert_alpha(),
        pygame.image.load("images/9.png").convert_alpha()
    ),
    "pipe": (
        pygame.transform.rotate(pygame.image.load("images/pipe.png").convert_alpha(),180),
        pygame.image.load("images/pipe.png").convert_alpha()
    )
}

baseX = 0
baseY = SCREEN_HEIGHT - GAME_IMGES["ground"].get_height()
bridX = SCREEN_WIDTH/5
bridY = SCREEN_HEIGHT/2

def welcome():
    while True:
        SCREEN.blit(GAME_IMGES["background"],(0,0))
        SCREEN.blit(GAME_IMGES["ground"],(baseX,baseY))
        welcomeText = pygame.font.SysFont("comicsansms", 30)
        welTextSurf = welcomeText.render("Welcome to Flappy Brid game (By Sahil Umraniya) ", True, (0,0,255))
        welTextRect =  welTextSurf.get_rect()
        welTextRect.midtop = (SCREEN_WIDTH/2, 10)
        SCREEN.blit( welTextSurf,  welTextRect)
        welTextSurf = welcomeText.render("Hit Space Key to Play", True, (0,0,255))
        welTextRect =  welTextSurf.get_rect()
        welTextRect.midtop = (SCREEN_WIDTH/2, 50)
        SCREEN.blit( welTextSurf,  welTextRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    return
                
def getpipe():
    gap = GAME_IMGES["bird"].get_height()*3
    y2=randint(gap,baseY)
    y1=(y2-gap-GAME_IMGES["pipe"][0].get_height())
    pipeX=SCREEN_WIDTH
    pipes=[
        {"x":pipeX , "y":y1},
        {"x":pipeX , "y":y2}
    ]
    return pipes

def game():
    pipe1 = getpipe()
    pipe2 = getpipe()
    pipe3 = getpipe()

    upperpipes = [
        {"x":SCREEN_WIDTH, "y":pipe1[0]["y"]},
        {"x":SCREEN_WIDTH +SCREEN_WIDTH/3, "y":pipe2[0]["y"]},
        {"x":SCREEN_WIDTH +SCREEN_WIDTH/3+350, "y":pipe3[0]["y"]}
    ]

    lowerpipes = [
        {"x":SCREEN_WIDTH, "y":pipe1[1]["y"]},
        {"x":SCREEN_WIDTH +SCREEN_WIDTH/3, "y":pipe2[1]["y"]},
        {"x":SCREEN_WIDTH +SCREEN_WIDTH/3+350, "y":pipe3[1]["y"]}
    ]

    score = 0
    pipeSpeedX = -15
    birdGravityY = -9.8
    birdMaxSpeed = 15
    birdFlySpeed = -8.5
    bridAccretionarySpeed = 1
    bridFlying = False 
    pipeHeight = GAME_IMGES["pipe"][0].get_height()
    bridX = SCREEN_WIDTH/5
    bridY = SCREEN_HEIGHT/2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if bridY > 0 and bridFlying==False:
                        birdGravityY = birdFlySpeed
                        bridFlying = True

        #move brid to up
        bridY = bridY + birdGravityY
        if bridFlying == True:
            bridFlying = False

        #move brid to down
        if birdGravityY < birdMaxSpeed and not bridFlying:
            birdGravityY = birdGravityY + bridAccretionarySpeed

        # move pipes
        for upperpipe , lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe["x"] = upperpipe["x"] + pipeSpeedX
            lowerpipe["x"] = lowerpipe["x"] + pipeSpeedX

        # add new Pipes
        if 0 < upperpipes[0]["x"] <= abs(pipeSpeedX):
            newpipe = getpipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])
        
        # remove old pipes
        if upperpipes[0]["x"] < 0:
            upperpipes.pop(0)
            lowerpipes.pop(0)

        # score
        bridCenterX = (GAME_IMGES["bird"].get_width()/2) + bridX
        for pipe in upperpipes:
            pipeCenterX = GAME_IMGES["pipe"][0].get_width()/2 + pipe["x"]
            if pipeCenterX <= bridCenterX < pipeCenterX + abs(pipeSpeedX):
                score = score + 1

        if isHit(bridX,bridY,upperpipes,lowerpipes):
            SCREEN.blit(GAME_IMGES["lossBird"],(bridX,bridY+abs(birdGravityY)))
            pygame.display.update()
            pygame.time.wait(1000)
            gameover(score)
        
        SCREEN.blit(GAME_IMGES["background"],(0,0))
        digits = [int(x) for x in str(score)]
        scoreX = 1000
        scoreY = baseY-160
        for digit in digits:
            SCREEN.blit(GAME_IMGES["digits"][digit],(scoreX,scoreY))
            scoreX += GAME_IMGES["digits"][digit].get_width()

        for upperpipe , lowerpipe in zip(upperpipes,lowerpipes):
            SCREEN.blit(GAME_IMGES["pipe"][0],(upperpipe["x"],upperpipe["y"]))
            SCREEN.blit(GAME_IMGES["pipe"][1],(lowerpipe["x"],lowerpipe["y"]))
        SCREEN.blit(GAME_IMGES["bird"],(bridX,bridY))
        SCREEN.blit(GAME_IMGES["ground"],(baseX,baseY))
        pygame.display.update()
        pygame.time.Clock().tick(30)

def isHit(bridX,bridY,upperPipes,lowerPipes):
    # upper and lower
    if bridY < 0 or bridY+GAME_IMGES["bird"].get_height()-25 > baseY:
        return True
    
    # upper pipe
    for upperpipe in upperPipes:
        if bridY < upperpipe["y"]+GAME_IMGES["pipe"][0].get_height() and (upperpipe["x"]-GAME_IMGES["bird"].get_width()-5 < bridX < upperpipe["x"]+GAME_IMGES["pipe"][0].get_width()):
            return True
    # lower pipe
    for lowerpipe in lowerPipes:
        if bridY+GAME_IMGES["bird"].get_height()-25 > lowerpipe["y"] and (lowerpipe["x"]-GAME_IMGES["bird"].get_width()-5 < bridX < lowerpipe["x"]+GAME_IMGES["pipe"][0].get_width()):
            return True
    
    return False

def gameover(score):
    while True:
        SCREEN.blit(GAME_IMGES["background"],(0,0))
        SCREEN.blit(GAME_IMGES["ground"],(baseX,baseY))
        welcomeText = pygame.font.SysFont("comicsansms", 45)
        welTextSurf = welcomeText.render(f"Game Over Your Score is {score} ", True, (255,0,0))
        welTextRect =  welTextSurf.get_rect()
        welTextRect.midtop = (SCREEN_WIDTH/2-120, SCREEN_HEIGHT/2-65)
        SCREEN.blit( welTextSurf,  welTextRect)
        welTextSurf = welcomeText.render("Hit Space Key to Play", True, (255,0,0))
        welTextRect =  welTextSurf.get_rect()
        welTextRect.midtop = (SCREEN_WIDTH/2-120, SCREEN_HEIGHT/2-25)
        SCREEN.blit( welTextSurf,  welTextRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    game()


welcome()
game()