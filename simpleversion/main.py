import pygame as pg, os, sys, time
from pygame.locals import *

# Ustwienia początkowe - najważniejsze zmienne
dir = os.path.dirname(__file__)
whoseTurn = 'Gracz 1 (X)'
whatSign = 'x'
whoseWin = None
draw = False
gameWidth = 600
gameHeight = 600
infoHeight = 300
deal = 1

colorWhite = (255, 255, 255)
colorBlack = (0, 0, 0)
colorRed = (255, 0, 0)
colorGrey = (130, 130, 130)

playerOneScore = 0
playerTwoScore = 0

# Ustwienia planszy
gameBoard = [[None]*3, [None]*3, [None]*3]

# Rysowanie okna gry
pg.init()  # Inicjalizacja biblioteki pygame
fps = 30
timer = pg.time.Clock()
gameScreen = pg.display.set_mode((gameWidth, gameHeight + infoHeight), 0, 32)

# Ustawienie tytułu okna
pg.display.set_caption("Gra 'Kółko i Krzyżyk'")

# Załadowanie obrazów do zmiennych
startingScreenPl = pg.image.load(dir + '/graphics/StartScreenPL.png')
xImage = pg.image.load(dir + '/graphics/krzyzyk.png')
oImage = pg.image.load(dir + '/graphics/kolo.png')

# Załadowanie dźwięków do zmiennych
markSound = pg.mixer.Sound(dir +'/audio/mark.wav')
winSound = pg.mixer.Sound(dir + '/audio/win.wav')

# Ustawienie skalowanie obrazów
startingScreenPl = pg.transform.scale(startingScreenPl, (gameWidth, gameHeight))
xImage = pg.transform.scale(xImage, (80, 80))
oImage = pg.transform.scale(oImage, (80, 80))


#Rysowanie eranu startowego
def draw_screen():
    gameScreen.fill(colorWhite)
    gameScreen.blit(startingScreenPl, (0, 100))
    pg.display.update()
    time.sleep(2)
    draw_deal()
    gameScreen.fill(colorWhite)
    draw_menu()

    
#Rysowanie menu
def draw_menu():
    gameScreen.fill(colorWhite)
    pg.draw.rect(gameScreen,colorGrey,[gameWidth/2,gameHeight/2,140,40])

# Rysowanie lini do podziału pola gry    
def draw_lines():
    # Rysowanie pionowych linii
    pg.draw.line(gameScreen, colorBlack, (gameWidth / 3, 0), (gameWidth / 3, gameHeight), 7)
    pg.draw.line(gameScreen, colorBlack, (gameWidth / 3 * 2, 0), (gameWidth / 3 * 2, gameHeight), 7)
    # Rysowanie poziomych linii
    pg.draw.line(gameScreen, colorBlack, (0, gameHeight / 3), (gameWidth, gameHeight / 3), 7)
    pg.draw.line(gameScreen, colorBlack, (0, gameHeight / 3 * 2), (gameWidth, gameHeight / 3 * 2), 7)
    pg.display.update()
    
 
 # Rysowanie okna z informacją o numarze rozdania   
def draw_deal():
    gameScreen.fill(colorWhite)
    pg.display.update()
    font = pg.font.Font(dir + '/fonts/MuseoSlab.ttf', 50)
    dealText = "ROZDANIE #" + str(deal)
    message = font.render(dealText, True, colorBlack)
    dealborders = message.get_rect(center=(gameWidth / 2, 450))
    gameScreen.blit(message, dealborders)
    pg.display.update()
    time.sleep(1)


# Rysowanie informacji o grze
def draw_info():
    global draw

    if whoseWin is None:
        infotext = "Twoja tura: " + whoseTurn
    else:
        if whoseWin == 'x':
            infotext = "Wygrał: Gracz 1 (X)! Gratulacje!"
        else:
            infotext = "Wygrał: Gracz 1 (O)! Gratulacje!"
    if draw:
        infotext = "Remis"

    font = pg.font.Font(dir + "/fonts/MuseoSlab.ttf", 30)
    message = font.render(infotext, True, colorWhite)
    scoreInfo = "PUNKTACJA"
    scoreInfoText = font.render(scoreInfo, True, colorBlack)
    score = "Gracz 1:   " + str(playerOneScore) + "     |     " + "Gracz 2:   " + str(playerTwoScore)
    scoretext = font.render(score, True, colorBlack)

    infoborders = message.get_rect(center=(gameWidth / 2, 700 - 50))
    scoreInfoBorders = scoreInfoText.get_rect(center=(gameWidth /2, 800 - 30))
    scoreborders = scoretext.get_rect(center=(gameWidth / 2, 900 - 75))

    gameScreen.fill((0, 0, 0), (0, 600, 600, 100))
    gameScreen.blit(message, infoborders)
    gameScreen.blit(scoreInfoText, scoreInfoBorders)
    gameScreen.blit(scoretext, scoreborders)
    pg.display.update()


#Rysowanie symbolów na tablicy
def draw_symbol(line, column):
    global gameBoard, whatSign, whoseTurn, markSound
    markSound.play()
    if line == 1:
        xposition = 50
    elif line == 2:
        xposition = gameWidth / 3 + 50
    elif line == 3:
        xposition = gameWidth / 3 * 2 + 50

    if column == 1:
        yposition = 50
    elif column == 2:
        yposition = gameHeight / 3 + 50
    elif column == 3:
        yposition = gameHeight / 3 * 2 + 50

    gameBoard[line - 1][column-1] = whatSign

    if whatSign == 'x':
        gameScreen.blit(xImage, (yposition, xposition))
        whatSign = 'o'
        whoseTurn = 'Gracz 2 (O)'
    elif whatSign== 'o':
        gameScreen.blit(oImage, (yposition, xposition))
        whatSign = 'x'
        whoseTurn = 'Gracz 1 (X)'
    pg.display.update()


# Sprawdzanie pozycji kursora względem tablicy
def check_board():
    # Zczytywanie pozycji kursora
    x, y = pg.mouse.get_pos()

    if x < gameWidth / 3:
        column = 1
    elif x < gameWidth / 3 * 2:
        column = 2
    elif x < gameWidth:
        column = 3
    else:
        column = None

    if y < gameHeight / 3:
        line = 1
    elif y < gameHeight / 3 * 2:
        line = 2
    elif y < gameHeight:
        line = 3
    else:
        line = None
    
    if line and column and gameBoard[line-1][column-1] is None:
        global whatSign
        draw_symbol(line, column)
        check_win()


# Sprawdzanie wygranej
def check_win():
    global gameBoard, whoseWin, draw, winSound

    for line in range(0, 3):
        if gameBoard[line][0] == gameBoard[line][1] == gameBoard[line][2] and gameBoard[line][0] is not None:
            whoseWin = gameBoard[line][0]
            winSound.play()
            pg.draw.line(gameScreen, colorRed, (0, (line + 1) * gameHeight/3 - gameHeight / 6), (gameWidth, (line + 1) * gameHeight / 3 - gameHeight / 6), 15)
            break

    for column in range(0, 3):
        if gameBoard[0][column] == gameBoard[1][column] == gameBoard[2][column] and gameBoard[0][column] is not None:
            whoseWin = gameBoard[0][column]
            winSound.play()
            pg.draw.line(gameScreen, colorRed, ((column + 1) * gameWidth / 3 - gameWidth / 6, 0), ((column + 1 ) * gameWidth / 3 - gameWidth / 6, gameWidth), 15)
            break

    if gameBoard[0][0] == gameBoard[1][1] == gameBoard[2][2] and gameBoard[0][0] is not None:
        whoseWin = gameBoard[0][0]
        winSound.play()
        pg.draw.line(gameScreen, colorRed, (0, 0), (600, 600), 15)
    if gameBoard[0][2] == gameBoard[1][1] == gameBoard[2][0] and gameBoard[0][2] is not None:
        whoseWin = gameBoard[0][2]
        winSound.play()
        pg.draw.line(gameScreen, colorRed, (600, 0), (0, 600), 15)

    if all([all(line) for line in gameBoard]) and whoseWin is None:
        draw = True
        winSound.play()

    draw_info()
    
    
# Funkcja restartująca rozdanie
def restart_game():
    global gameBoard, whoseWin, whatSign, draw, playerOneScore, playerTwoScore, whoseTurn, deal
    time.sleep(3)
    whatSign = 'x'
    whoseTurn = 'Gracz 1 (X)'
    deal += 1
    draw = False
    if whoseWin == 'x':
        playerOneScore += 1
    elif whoseWin == 'o':
        playerTwoScore += 1
    whoseWin = None
    gameBoard = [[None]*3, [None]*3, [None]*3]
    draw_deal()
    gameScreen.fill(colorWhite)
    draw_lines()
    draw_info()

# Pierwszwe wywołanie rysowania programu
draw_screen()

# Główna pętla gry
while True:
    for incident in pg.event.get():
        if incident.type == QUIT:
            pg.quit()
            sys.exit()
        elif incident.type == MOUSEBUTTONDOWN and incident.button == 1:
                check_board()
                if whoseWin or draw:
                    restart_game()
    pg.display.update()
    timer.tick(fps)
