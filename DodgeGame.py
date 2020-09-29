# Raymond Mei    6/2/2020
import pygame, sys, io, random

pygame.init()
clock = pygame.time.Clock()

global playerImage, bulletImage, laserImage, playerSpriteSheet, walkCount


#COLORS
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Black = (0, 0, 0)
White = (255, 255, 255)
Desert = (237, 201, 175) # Temp background


screenWidth = 1024
screenHeight = 768
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Dodging Game")



# to have images when running code on different computer (dont have to download them)
from urllib.request import urlopen, Request
imgUrls = ["https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/b5c8fc60-64f7-4bb9-a25d-4d2bef9ec716/dbjtqjh-2e13db3c-982a-4f53-90ac-91280613a2c3.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvYjVjOGZjNjAtNjRmNy00YmI5LWEyNWQtNGQyYmVmOWVjNzE2XC9kYmp0cWpoLTJlMTNkYjNjLTk4MmEtNGY1My05MGFjLTkxMjgwNjEzYTJjMy5wbmcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.W6XBt1KGz9O-9Md7tGaH59GXF9ee3mOW7wZL9en1Xjg",
           "https://donaldcarling.files.wordpress.com/2016/03/mine-bullet.png?w=417&h=302",
            "https://res.cloudinary.com/mirukusheku/image/upload/v1495140035/Red_laser-ConvertImage_votu8o.png",
            "https://webstockreview.net/images/coin-clipart-sprite-14.png"]
imgFiles = []
for n in imgUrls:
    req = Request(url=n, headers={"User-Agent": "Mozilla/5.0"})
    imgStr = urlopen(req).read()
    imgFile = io.BytesIO(imgStr)
    imgFiles.append(imgFile)
playerImage = pygame.image.load(imgFiles[0]).convert_alpha()

playerSpriteSheet = []
for i in range(4):
    for j in range(4):
        playerSpriteSheet.append(playerImage.subsurface(pygame.Rect(j * 64, i * 64, 64, 64)))

bulletImage = pygame.transform.scale(pygame.image.load(imgFiles[1]).convert_alpha(), (50, 35))
laserImage = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(imgFiles[2]), (100, 1200)), 90)
coinImage = pygame.image.load(imgFiles[3]).convert_alpha()

coinSpriteSheet = []
for i in range(6):
    coinSpriteSheet.append(coinImage.subsurface(pygame.Rect(i * 62 + 140, 24, 60, 60)))



playerSprite = pygame.sprite.Group()

class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerSpriteSheet[0]
        self.rect = pygame.Rect(0, 0, 30, 47)
        self.rect.centerx = screenWidth / 2
        self.rect.centery = screenHeight / 2
        self.walkCount = 0

    def update(self, playerPosX, playerPosY):
        global playerY
        speed = 7

        k = pygame.key.get_pressed()
        if k[pygame.K_w] or k[pygame.K_UP]:
            playerPosY -= speed
            self.image = playerSpriteSheet[12 + self.walkCount // 4]
            self.walkCount += 1
        elif k[pygame.K_s] or k[pygame.K_DOWN]:
            playerPosY += speed
            self.image = playerSpriteSheet[0 + self.walkCount // 4]
            self.walkCount += 1
        if k[pygame.K_a] or k[pygame.K_LEFT]:
            playerPosX -= speed
            self.image = playerSpriteSheet[4 + self.walkCount // 4]
            self.walkCount += 1
        elif k[pygame.K_d] or k[pygame.K_RIGHT]:
            playerPosX += speed
            self.image = playerSpriteSheet[8 + self.walkCount // 4]
            self.walkCount += 1

        self.rect.x += playerPosX
        self.rect.y += playerPosY

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screenHeight:
            self.rect.bottom = screenHeight
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screenWidth:
            self.rect.right = screenWidth

        if self.walkCount > 15:
            self.walkCount = 0

        # pygame.draw.rect(screen, Red, self.rect) #hitbox
        screen.blit(self.image, (self.rect.x-14, self.rect.y-15))
        playerY = self.rect.centery



bulletSprites = pygame.sprite.Group()

class bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletImage
        self.rect = pygame.Rect(0, 0, 17, 17)
        self.rect.centerx = random.randint(10, screenWidth-10)
        self.rect.centery = 0

    def update(self, difficulty):
        self.rect.y += 5 + difficulty
        if self.rect.top >= screenHeight:
            self.kill()
        # pygame.draw.rect(screen, Blue, self.rect) #hitbox
        screen.blit(bulletImage, (self.rect.x-16, self.rect.y-6))


laserSprites = pygame.sprite.Group()

class laser(pygame.sprite.Sprite):
    def __init__(self, n):
        pygame.sprite.Sprite.__init__(self)
        self.image = laserImage
        self.rect = pygame.Rect(0, n, 1024, 30)

    def delete(self):
        self.kill()

    def update(self):
        # pygame.draw.rect(screen, Blue, self.rect) #hitbox
        screen.blit(laserImage, (self.rect.x-75, self.rect.y-35))


coinSprites = pygame.sprite.Group()

class coin(pygame.sprite.Sprite):
    def __init__(self, randX, randY):
        pygame.sprite.Sprite.__init__(self)
        self.image = coinSpriteSheet[0]
        self.rect = self.image.get_rect()
        self.rect.x = randX
        self.rect.y = randY

    def delete(self):
        self.kill()

    def update(self, coinIndex):
        # pygame.draw.rect(screen, Green, self.rect) #hitbox
        self.image = coinSpriteSheet[coinIndex]
        screen.blit(self.image, (self.rect.x+1, self.rect.y+1))



def startScreen():

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                run = False

        screen.fill(Black)

        startFont = pygame.font.SysFont('Courier', 50, True)
        startTxt = startFont.render("Press any button to Start", True, White)
        startRect = startTxt.get_rect()
        screen.blit(startTxt, (screenWidth/2 - startRect.width/2, 300))

        infoFont = pygame.font.SysFont('Courier', 20, True)
        infoTxt = infoFont.render("bullet                        laser indicator                      laser", True, White)
        infoRect = infoTxt.get_rect()
        screen.blit(infoTxt, (screenWidth/2 - infoRect.width/2, 500))
        screen.blit(bulletImage, (35, 497))
        pygame.draw.rect(screen, Red, pygame.Rect(240, 500, 170, 20))
        screen.blit(pygame.transform.scale(laserImage, (170, 50)), (695, 488))

        coinTxt = infoFont.render("COIN!", True, White)
        screen.blit(pygame.transform.scale(coinSpriteSheet[0], (40, 40)), (screenWidth/2 - 25, 590))
        screen.blit(coinTxt, (screenWidth/2 + 25, 600))

        info2Font = pygame.font.SysFont('Courier', 15, True)
        info2Txt = info2Font.render("* Game Over if you hit a bullet or laser", True, White)
        info2Rect = info2Txt.get_rect()
        screen.blit(info2Txt, (screenWidth/2 - info2Rect.width/2, 670))

        nameTxt = info2Font.render("Raymond Mei ICS3U0", True, White)
        screen.blit(nameTxt, (screenWidth-175, screenHeight-30))

        pygame.display.flip()
        clock.tick(60)


def gameOverScreen(score):

    while True:
        screen.fill(Black)

        gameOverFont = pygame.font.SysFont('Courier', 50, True)
        gameOverTxt = gameOverFont.render("Game Over!", True, White)
        rect = gameOverTxt.get_rect()
        screen.blit(gameOverTxt, (screenWidth / 2 - rect.width/2, screenHeight / 2 - rect.height/2))

        scoreFont = pygame.font.SysFont('Courier', 35, True)
        scoreTxt = scoreFont.render("Score: " + str(score), True, Green)
        scoreRect = scoreTxt.get_rect()
        screen.blit(scoreTxt, (screenWidth/2 - scoreRect.width/2, 490))

        quitFont = pygame.font.SysFont('Calibri', 20, True)
        quitTxt = quitFont.render("Quit or press ESC", True, White)
        rect = quitTxt.get_rect()
        screen.blit(quitTxt, (screenWidth / 2 - rect.width/2, 600))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)


score = 0
loopCount = 0
runTime = 0 #Time in seconds
difficulty = 0
coinIndex = 0


sec = True #check if x # of seconds passed
sec2 = True
sec3 = True


# making player
playerObj = player()
playerSprite.add(playerObj)

#MAIN LOOP
startScreen()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    screen.fill(Desert)


    #loopCount runs 60 times a second
    if loopCount % 60 == 0:
        runTime += 1
        score += 1

    # every 20 sec, speeds up
    if sec and runTime % 20 == 0 and runTime != 0:
        difficulty += 1
        sec = False
    if runTime % 20 == 1 and runTime != 1:
        sec = True


    # limit bullet spawning to every 6 iterations
    if loopCount % 6 == 0:
        bulletObj = bullet()
        bulletSprites.add(bulletObj)

    # laser spawning
    if sec2 and runTime % 5 == 0 and runTime != 0:
        n = random.randint(playerY-80, playerY+80)
        laserObj = laser(n)
        sec2 = False
    if runTime % 5 == 0 and runTime != 0:
        pygame.draw.rect(screen, Red, pygame.Rect(0, n, 1024, 30))
    if runTime % 5 == 1 and runTime != 1:
        laserSprites.add(laserObj)
    if runTime % 5 == 2 and runTime != 2:
        laserObj.delete()
        sec2 = True

    # coin spawning
    if sec3 and runTime % 20 == 0 and runTime != 0:
        randX = random.randint(10, screenWidth-70)
        randY = random.randint(10, screenWidth-60)
        coinObj = coin(randX, randY)
        coinSprites.add(coinObj)
        sec3 = False
    if runTime % 20 == 3 and runTime != 3:
        coinObj.delete()
        sec3 = True


    loopCount += 1
    if loopCount == 1000000: #save memory i guess
        loopCount = 0



    spriteCollisions = pygame.sprite.spritecollide(playerObj, bulletSprites, True)
    spriteCollisions += pygame.sprite.spritecollide(playerObj, laserSprites, True)
    if spriteCollisions:
        gameOverScreen(score)

    coinCollisions = pygame.sprite.spritecollide(playerObj, coinSprites, True)
    if coinCollisions:
        score += 30
        coinObj.delete()
        coinCollisions.clear()

    bulletSprites.update(difficulty)
    laserSprites.update()
    coinSprites.update(coinIndex)
    playerObj.update(0, 0)

    #to animate coin
    if loopCount % 5 == 0:
        coinIndex += 1
    if coinIndex > 5:
        coinIndex = 0

    #display score
    arialFont = pygame.font.SysFont('Arial', 30, True)
    pScore = arialFont.render("Score: "+str(score), True, Black)
    screen.blit(pScore, (0, 0))

    pygame.display.flip()
    clock.tick(60)
