import pygame as pg, os, sys, time, random
from pygame.display import update
from pygame.locals import *

#Ustwienia początkowe - najważniejsze zmienne

#Zmienna przechowująca ścieżkę do katalogu ze skryptem
dir = os.path.dirname(__file__) 

#Zmienne potrzebne to poprawnego działania gry
language = 'PL'
whoseTurn = ''
whatSign = 'x'
whoseWin = None
draw = False
menu = False
gameReady = False
credits = False
buttonPressed = 0
deal = 1
motion = 0
useLines = 0
useColumns = 0
pvc = False
allLines = [1,2,3]
allColumns = [1,2,3]
playerOneScore = 0
playerTwoScore = 0

#Zmienne zawierające wielkość okna gry
gameWidth = 600
gameHeight = 600
infoHeight = 300

#Zmienne przechowujące kolory
colorWhite = (255, 255, 255)
colorBlack = (0, 0, 0)
colorRed = (255, 0, 0)
colorGrey = (80, 80, 80)

# Ustwienie początkowej planszy
gameBoard = [[None]*3, [None]*3, [None]*3] 

# Rysowanie okna gry
pg.init()  # Inicjalizacja biblioteki pygame
fps = 30
timer = pg.time.Clock()
gameScreen = pg.display.set_mode((gameWidth, gameHeight + infoHeight), 0, 32)

# Ustawienie tytułu okna
pg.display.set_caption("Gra kółko i krzyżyk")

# Załadowanie obrazów do zmiennych
startingScreenPl = pg.image.load(dir + '/graphics/StartScreenPL.png')
xImage = pg.image.load(dir + '/graphics/krzyzyk.png')
oImage = pg.image.load(dir + '/graphics/kolo.png')

# Załadowanie dźwięków do zmiennych
markSound = pg.mixer.Sound(dir +'/audio/mark.wav')
winSound = pg.mixer.Sound(dir + '/audio/win.wav')
menuSound = pg.mixer.Sound(dir + '/audio/menuloop.wav')

# Ustawienie skalowanie obrazów
startingScreenPl = pg.transform.scale(startingScreenPl, (gameWidth, gameHeight))
xImage = pg.transform.scale(xImage, (80, 80))
oImage = pg.transform.scale(oImage, (80, 80))


#Rysowanie eranu startowego
def draw_screen():
    global menu
    gameScreen.fill(colorWhite)
    gameScreen.blit(startingScreenPl, (0, 100))
    pg.display.update()
    time.sleep(2)
    gameScreen.fill(colorWhite)
    menu= True

    
#Rysowanie menu
def draw_menu():
    global menu, buttonPressed, menuSound
    gameScreen.fill(colorWhite)
    menuSound.play(-1) 
    menuSound.set_volume(0.2)
    #Rysowanie przycisków menu
    fontMenu = pg.font.Font(dir + '/fonts/MuseoSlab.ttf', 100)
    fontButtons = pg.font.Font(dir + '/fonts/MuseoSlab.ttf', 20)
    menuText = fontMenu.render('MENU', True, colorBlack)
    menuBorders = menuText.get_rect(center=(gameWidth / 2, 100))
    gameScreen.blit(menuText, menuBorders)
    pg.draw.rect(gameScreen,colorGrey,[gameWidth/3,200,200,100])    
    #Napisy w zależnośi od zmiennej language odpowiadającej wybranemu językowi
    if language == 'ENG':
        pvpText = fontButtons.render('Player vs Player', True, colorWhite)
        gameScreen.blit(pvpText, (gameWidth/3+20,235))
    else:
        pvpText = fontButtons.render('Gracz vs Gracz', True, colorWhite)
        gameScreen.blit(pvpText, (gameWidth/3+25,235))
    pg.draw.rect(gameScreen,colorGrey,[gameWidth/3,330,200,100])
    if language == 'ENG':
        pvcText = fontButtons.render('Player vs CPU', True, colorWhite)
        gameScreen.blit(pvcText, (gameWidth/3+28,365))
    else:
        pvcText = fontButtons.render('Gracz vs CPU', True, colorWhite)
        gameScreen.blit(pvcText, (gameWidth/3+28,365))
    pg.draw.rect(gameScreen,colorGrey,[gameWidth/3,460,200,100])
    if language == 'ENG':
        authorsText = fontButtons.render('Authors', True, colorWhite)
        gameScreen.blit(authorsText, (gameWidth/3+58,495))
    else:
        authorsText = fontButtons.render('Autorzy', True, colorWhite)
        gameScreen.blit(authorsText, (gameWidth/3+55,495))
    pg.draw.rect(gameScreen,colorGrey,[gameWidth/3,590,200,100])
    if language == 'ENG':
        languageText = fontButtons.render('Polish', True, colorWhite)
        gameScreen.blit(languageText, (gameWidth/3+65,625))
    else:
        languageText = fontButtons.render('Angielski', True, colorWhite)
        gameScreen.blit(languageText, (gameWidth/3+50,625))
    pg.draw.rect(gameScreen,colorGrey,[gameWidth/3,720,200,100])
    if language == 'ENG':
        quitText = fontButtons.render('Quit', True, colorWhite)
        gameScreen.blit(quitText, (gameWidth/3+75,755))
    else:
        quitText = fontButtons.render('Wyjście', True, colorWhite)
        gameScreen.blit(quitText, (gameWidth/3+55,755))
    pg.display.update();
    
    
# Rysowanie lini do podziału pola gry    
def draw_lines():
    gameScreen.fill(colorWhite)
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
    if language == 'ENG':
        dealText = "GAME #" + str(deal)
    else:
        dealText = "ROZDANIE #" + str(deal)
    message = font.render(dealText, True, colorBlack)
    dealborders = message.get_rect(center=(gameWidth / 2, 450))
    gameScreen.blit(message, dealborders)
    pg.display.update()
    time.sleep(1)


# Rysowanie informacji o grze
def draw_info():
    global draw, gameReady, whoseTurn, pvc
    if motion == 0:
        if language == 'ENG':
            if  pvc == True:
                whoseTurn = 'Player (X)'
            else:
                whoseTurn = 'Player 1 (X)'
        else:
            if  pvc == True:
                whoseTurn = 'Gracz (X)'
            else:
                whoseTurn = 'Gracz 1 (X)'
                                
    if language == 'ENG':
        if whoseWin is None:
            infotext = "Your turn: " + whoseTurn
        else:
            if whoseWin == 'x':
                if pvc == True:
                    infotext = "Player (X) win! Congratulations!"
                else:
                    infotext = "Player 1 (X) win! Congratulations!"
            else:
                if pvc == True:
                    infotext = "Computer (O) win!"
                else:
                    infotext = "Player 2 (O) win! Congratulations!"
        if draw:
            infotext = "Draw"
    else:
        if whoseWin is None:
            infotext = "Twoja tura: " + whoseTurn
        else:
            if whoseWin == 'x':
                if pvc == True:
                    infotext = "Wygrał: Gracz(X)! Gratulacje!"
                else:
                    infotext = "Wygrał: Gracz 1 (X)! Gratulacje!"
            else:
                if pvc == True:
                  infotext = "Wygrał: komputer (O)!"
                else:  
                    infotext = "Wygrał: Gracz 2 (O)! Gratulacje!"
        if draw:
            infotext = "Remis"

    font = pg.font.Font(dir + "/fonts/MuseoSlab.ttf", 30)
    message = font.render(infotext, True, colorWhite)
    if language == 'ENG':
        scoreInfo = "SCORE"
    else:
        scoreInfo = "PUNKTACJA"
    scoreInfoText = font.render(scoreInfo, True, colorBlack)
    if language == 'ENG':
        if pvc == True:
            score = "Player:   " + str(playerOneScore) + "     |     " + "Computer:   " + str(playerTwoScore)
        else:
            score = "Player 1:   " + str(playerOneScore) + "     |     " + "Player 2:   " + str(playerTwoScore)
    else:
        if pvc == True:
            score = "Gracz:   " + str(playerOneScore) + "     |     " + "Komputer:   " + str(playerTwoScore)
        else:
            score = "Gracz 1:   " + str(playerOneScore) + "     |     " + "Gracz 2:   " + str(playerTwoScore)
    scoretext = font.render(score, True, colorBlack)

    infoborders = message.get_rect(center=(gameWidth / 2, 630))
    scoreInfoBorders = scoreInfoText.get_rect(center=(gameWidth /2, 700))
    scoreborders = scoretext.get_rect(center=(gameWidth / 2, 750))

    gameScreen.fill((0, 0, 0), (0, 600, 600, 70))
    gameScreen.blit(message, infoborders)
    gameScreen.blit(scoreInfoText, scoreInfoBorders)
    gameScreen.blit(scoretext, scoreborders)
    
    pg.draw.rect(gameScreen,colorGrey,[0 , 800,600,100])
    if language == 'ENG':
        menuText = font.render('MAIN MENU', True, colorWhite)
        gameScreen.blit(menuText, (210 ,825))
    else:
        menuText = font.render('MENU GŁÓWNE', True, colorWhite)
        gameScreen.blit(menuText, (180 ,825))
    pg.display.update()
    gameReady = True


#Rysowanie symbolów na tablicy
def draw_symbol(line, column):
    global gameBoard, whatSign, whoseTurn, markSound, allColumns, allLines, useLines, useColumns, pvc
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
    useLines=line
    useColumns=column

    if whatSign == 'x':
        gameScreen.blit(xImage, (yposition, xposition))
        whatSign = 'o'
        if language == 'ENG':
            if pvc == True:
                whoseTurn = 'Computer (O)'
            else:
                whoseTurn = 'Player 2 (O)'
        else:
            if pvc == True:
                whoseTurn = 'Komputer (O)'
            else:
                whoseTurn = 'Gracz 2 (O)'
    elif whatSign == 'o':
        gameScreen.blit(oImage, (yposition, xposition))
        whatSign = 'x'
        if language == 'ENG':
            if pvc == True:
                whoseTurn = 'Player (X)'
            else:
                whoseTurn = 'Player 1 (O)'
        else:
            if pvc == True:
                whoseTurn = 'Gracz (X)'
            else:
                whoseTurn = 'Gracz 1 (X)'
    pg.display.update()


#Rysowanie informcji o autorach gry
def draw_authors():
    global credits
    gameScreen.fill(colorWhite)
    fontH = pg.font.Font(dir + '/fonts/MuseoSlab.ttf', 40)
    font = pg.font.Font(dir + '/fonts/MuseoSlab.ttf', 20)
    if language == 'ENG':
        authorsText = font.render('AUTHORS', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 100))
        gameScreen.blit(authorsText, authorsBorders)
    else:
        authorsText = font.render('AUTORZY', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 100))
        gameScreen.blit(authorsText, authorsBorders)
    if language == 'ENG':
        authorsText = fontH.render('Rafal Makowski', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 150))
        gameScreen.blit(authorsText, authorsBorders)
    else:
        authorsText = fontH.render('Rafal Makowski', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 150))
        gameScreen.blit(authorsText, authorsBorders)
    if language == 'ENG':
        authorsText = font.render('Music and sounds:', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 300))
        gameScreen.blit(authorsText, authorsBorders)
    else:
        authorsText = font.render('Muzyka i dźwięki:', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 300))
        gameScreen.blit(authorsText, authorsBorders)
    if language == 'ENG':
        authorsText = font.render('October Rose by StephieQueen (https://freesound.org)', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 350))
        gameScreen.blit(authorsText, authorsBorders)
    else:
        authorsText = font.render('"October Rose" - StephieQueen (https://freesound.org)', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 350))
        gameScreen.blit(authorsText, authorsBorders)
    if language == 'ENG':
        authorsText = font.render('and other sounds from https://freesound.org', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 400))
        gameScreen.blit(authorsText, authorsBorders)
    else:
        authorsText = font.render('i inne dźwięki dostępna na https://freesound.org', True, colorBlack)
        authorsBorders = authorsText.get_rect(center=(gameWidth / 2, 400))
        gameScreen.blit(authorsText, authorsBorders)
    pg.draw.rect(gameScreen,colorGrey,[0,700,600,200])
    fontButton = pg.font.Font(dir + '/fonts/MuseoSlab.ttf', 50)
    if language == 'ENG':
        menuText = fontButton.render('MAIN MENU', True, colorWhite)
        gameScreen.blit(menuText, (140 ,755))
    else:
        menuText = fontButton.render('MENU GŁÓWNE', True, colorWhite)
        gameScreen.blit(menuText, (100 ,755))
    pg.display.update()
    credits = True
    

#Sprawdzanie przycisku powrotu do menu z informacji o autrach
def check_authors():
    global menu, credits
    x, y = pg.mouse.get_pos()
    if (x > 0 and x < 600) and (y >700 and y <900):
        pg.draw.rect(gameScreen,colorBlack,[0,700, 600, 200])
        menu=True
        credits = False
    fontButton = pg.font.Font(dir + '/fonts/MuseoSlab.ttf', 50)
    if language == 'ENG':
        menuText = fontButton.render('MAIN MENU', True, colorWhite)
        gameScreen.blit(menuText, (140 ,755))
        pg.display.update()
        markSound.play()
        time.sleep(0.5)
    else:
        menuText = fontButton.render('MENU GŁÓWNE', True, colorWhite)
        gameScreen.blit(menuText, (100 ,755))
        pg.display.update()
        markSound.play()
        time.sleep(0.5)
        

# Sprawdzanie pozycji kursora względem tablicy
def check_board():
    global menu, buttonPressed, gameReady, deal, gameBoard, playerOneScore, playerTwoScore, motion, allColumns, allLines, useLines, useColumns, pvc
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
    
    motion += 1
    
    if line and column and gameBoard[line-1][column-1] is None:
        draw_symbol(line, column)
        check_win()


#Funkcja resetująca zmienne do ustawień początkowych po powrocie do menu z okna gry
def reset_variables():
    global menu, buttonPressed, gameReady, deal, gameBoard, playerOneScore, playerTwoScore, motion, allColumns, allLines, useLines, useColumns, pvc
    #Sprawdzanie czy został naciśnięty przycisk menu
    x, y = pg.mouse.get_pos()
    fontButtons = pg.font.Font(dir + '/fonts/MuseoSlab.ttf', 30)
    if (x > 0 and x < 600) and (y >800 and y <900):
        pg.draw.rect(gameScreen,colorBlack,[0,800, 600, 100])
        if language == 'ENG':
            menuText = fontButtons.render('MAIN MENU', True, colorWhite)
            gameScreen.blit(menuText, (210 ,825))
        else:
            menuText = fontButtons.render('MENU GŁÓWNE', True, colorWhite)
            gameScreen.blit(menuText, (180 ,825))
        #Restowanie ekranu i zmiennych
        pg.display.update()
        markSound.play()
        gameBoard = [[None]*3, [None]*3, [None]*3]
        deal = 1
        playerOneScore = 0
        playerTwoScore = 0
        motion = 0
        allLines = [1,2,3]
        allColumns = [1,2,3]
        useLines = 0
        useColumns = 0
        menu = True
        pvc = False
        gameReady = False
        buttonPressed = 0
        time.sleep(0.5)

#Sprawdzenie jaki przycisk menu został wciśnięty
def check_button():
    global buttonPressed, menu
    pg.display.update()
    # Zczytywanie pozycji kursora    
    x, y = pg.mouse.get_pos()
    fontButtons = pg.font.Font(dir + '/fonts/MuseoSlab.ttf', 20)
    if (x > gameWidth/3 and x < gameWidth/3+200) and (y > 200 and y < 300):
        buttonPressed = 1
        pg.draw.rect(gameScreen,colorBlack,[gameWidth/3,200,200,100])
        if language == 'ENG':
            pvpText = fontButtons.render('Player vs Player', True, colorWhite)
            gameScreen.blit(pvpText, (gameWidth/3+20,235))
            pg.display.update()
        else:
            pvpText = fontButtons.render('Gracz vs Gracz', True, colorWhite)
            gameScreen.blit(pvpText, (gameWidth/3+25,235))
            pg.display.update()
        markSound.play()
        time.sleep(0.5)
    elif (x > gameWidth/3 and x < gameWidth/3+200) and (y > 330 and y <430):
        buttonPressed = 2 
        pg.draw.rect(gameScreen,colorBlack,[gameWidth/3,330,200,100])
        if language == 'ENG':
            pvcText = fontButtons.render('Player vs CPU', True, colorWhite)
            gameScreen.blit(pvcText, (gameWidth/3+28,365))
            pg.display.update()
        else:
            pvcText = fontButtons.render('Gracz vs CPU', True, colorWhite)
            gameScreen.blit(pvcText, (gameWidth/3+28,365))
            pg.display.update()
        markSound.play()  
        time.sleep(0.5)
    elif (x > gameWidth/3 and x < gameWidth/3+200) and (y >460 and y <560):
        buttonPressed = 3 
        pg.draw.rect(gameScreen,colorBlack,[gameWidth/3,460,200,100])
        if language == 'ENG':
            authorsText = fontButtons.render('Authors', True, colorWhite)
            gameScreen.blit(authorsText, (gameWidth/3+58,495))
            pg.display.update()
        else:
            authorsText = fontButtons.render('Autorzy', True, colorWhite)
            gameScreen.blit(authorsText, (gameWidth/3+55,495))
            pg.display.update()  
        markSound.play()
        time.sleep(0.5)
    elif (x > gameWidth/3 and x < gameWidth/3+200) and (y >590 and y <690):
        buttonPressed = 4
        pg.draw.rect(gameScreen,colorBlack,[gameWidth/3,590,200,100])
        if language == 'ENG':
            languageText = fontButtons.render('Polish', True, colorWhite)
            gameScreen.blit(languageText, (gameWidth/3+65,625))
            pg.display.update()
        else:
            languageText = fontButtons.render('Angielski', True, colorWhite)
            gameScreen.blit(languageText, (gameWidth/3+50,625))
            pg.display.update()
        markSound.play()
        time.sleep(0.5)
    elif (x > gameWidth/3 and x < gameWidth/3+200) and (y >720 and y < 820):
        buttonPressed = 5
        pg.draw.rect(gameScreen,colorBlack,[gameWidth/3,720,200,100])
        if language == 'ENG':
            quitText = fontButtons.render('Quit', True, colorWhite)
            gameScreen.blit(quitText, (gameWidth/3+75,755))
            pg.display.update()
        else: 
            quitText = fontButtons.render('Wyjście', True, colorWhite)
            gameScreen.blit(quitText, (gameWidth/3+55,755))
            pg.display.update()
        markSound.play()
        time.sleep(0.5)  
    else:
        buttonPressed = 0         
        draw_menu()
        
           
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
   
   
#Funkcja programująca zachowanie ai w rozgrywce z komputerem 
def cpu_ai():
    global gameBoard, whoseWin, draw, winSound, whatSign, whoseTurn, markSound, useLines, useColumns, allLines, allColumns, gameReady
    #W pierwszym ruchu ai zajmuje losowo wybrane pole, poza tym wybranym przez gracza
    if whatSign == 'o' and motion == 1 and whoseWin == None:
        allLines.remove(useLines)
        allColumns.remove(useColumns)
    
        line = random.choice(allLines)
        column = random.choice(allColumns)
        
        time.sleep(0.5)
        draw_symbol(line, column)
    #Po pierwszym ruchu ai wykonuje szereg sprawdzeń pola i zależnie od sytuacji wykonuje swój ruch
    elif whatSign == 'o' and motion != 1 and whoseWin == None:
        #Resetowanie listy pól do natępnej rozgrywki
        allLines = [1,2,3]
        allColumns = [1,2,3]   
        #W pierwszej kolejności ai sprawdza czy ma dwa swoje znaki w jakiejś lini, jeśli tak, dokłada trzeci   
        for i in range (0, 3):
            if gameBoard[i].count('o') == 2 and gameBoard[i].count(None) == 1:
                if None in gameBoard[i]:
                    line = i+1
                    column = gameBoard[i].index(None)+1
                    time.sleep(0.5)
                    draw_symbol(line, column)
                    check_win()
                    return
        #W drugiej kolejności sprawdza czy ma dwa swoje symbole w którejś z kolumn
        for i in range (0, 3):
            if (gameBoard[0][i] == 'o') and (gameBoard[1][i] == 'o'):
                if gameBoard[2][i] is None:
                    line = 3
                    column = i+1
                    time.sleep(0.5)
                    draw_symbol(line, column)
                    check_win()
                    return
            if (gameBoard[1][i] == 'o') and (gameBoard[2][i] == 'o'):
                if gameBoard[0][i] is None:
                    line = 1
                    column = i+1
                    time.sleep(0.5)
                    draw_symbol(line, column)
                    check_win()
                    return
            if (gameBoard[0][i] == 'o') and (gameBoard[2][i] == 'o'):
                if gameBoard[1][i] is None:
                    line = 2
                    column = i+1
                    time.sleep(0.5)
                    draw_symbol(line, column)
                    check_win()
                    return
        #Następnie sprawdza przekątne pod kątem dwóch swoich symboli
        if (gameBoard[0][0] == 'o') and (gameBoard[1][1] == 'o'):
            if gameBoard[2][2] is None:
                line = 3
                column = 3
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[1][1] == 'o') and (gameBoard[2][2] == 'o'):
            if gameBoard[0][0] is None:
                line = 1
                column = 1
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[0][0] == 'o') and (gameBoard[2][2] == 'o'):
            if gameBoard[1][1] is None:
                line = 2
                column = 2
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[0][2] == 'o') and (gameBoard[1][1] == 'o'):
            if gameBoard[2][0] is None:
                line = 3
                column = 1
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[1][1] == 'o') and (gameBoard[2][0] == 'o'):
            if gameBoard[0][2] is None:
                line = 1
                column = 3
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[0][2] == 'o') and (gameBoard[2][0] == 'o'):
            if gameBoard[1][1] is None:
                line = 2
                column = 2
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        #Potem ai sprawsza czy gracz ma w jakiejś linie dwa swoje symbole, jeśli tak, kontruje trzecie pole w lini swoim 
        for i in range (0, 3):
            if gameBoard[i].count('x') == 2 and gameBoard[i].count(None) == 1:
                if None in gameBoard[i]:
                    line = i+1
                    column = gameBoard[i].index(None)+1
                    time.sleep(0.5)
                    draw_symbol(line, column)
                    check_win()
                    return
        #Po liniach sprawdza kolumny pod tym samym warunkiem
        for i in range (0, 3):
            if (gameBoard[0][i] == 'x') and (gameBoard[1][i] == 'x'):
                if gameBoard[2][i] is None:
                    line = 3
                    column = i+1
                    time.sleep(0.5)
                    draw_symbol(line, column)
                    check_win()
                    return
            if (gameBoard[1][i] == 'x') and (gameBoard[2][i] == 'x'):
                if gameBoard[0][i] is None:
                    line = 1
                    column = i+1
                    time.sleep(0.5)
                    draw_symbol(line, column)
                    check_win()
                    return
            if (gameBoard[0][i] == 'x') and (gameBoard[2][i] == 'x'):
                if gameBoard[1][i] is None:
                    line = 2
                    column = i+1
                    time.sleep(0.5)
                    draw_symbol(line, column)
                    check_win()
                    return
        #Po kolumnach sprawdza przekątne
        if (gameBoard[0][0] == 'x') and (gameBoard[1][1] == 'x'):
            if gameBoard[2][2] is None:
                line = 3
                column = 3
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[1][1] == 'x') and (gameBoard[2][2] == 'x'):
            if gameBoard[0][0] is None:
                line = 1
                column = 1
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[0][0] == 'x') and (gameBoard[2][2] == 'x'):
            if gameBoard[1][1] is None:
                line = 2
                column = 2
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[0][2] == 'x') and (gameBoard[1][1] == 'x'):
            if gameBoard[2][0] is None:
                line = 3
                column = 1
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[1][1] == 'x') and (gameBoard[2][0] == 'x'):
            if gameBoard[0][2] is None:
                line = 1
                column = 3
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        if (gameBoard[0][2] == 'x') and (gameBoard[2][0] == 'x'):
            if gameBoard[1][1] is None:
                line = 2
                column = 2
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
        #Na koniec, jeśli nie ma w żadej lini, kolumnie czy przekątnej dwóch takich samych symboli, losuje jedno z pozostałych wolnych pól 
        for i in range (0, 3):
            if gameBoard[i].count(None) >= 1:
                line = i+1
                column = gameBoard[i].index(None)+1
                time.sleep(0.5)
                draw_symbol(line, column)
                check_win()
                return
    gameReady = False
            

#Funkcja zmieniająca język gry         
def change_language():
    global language, menu, buttonPressed
    if language == 'PL':
        language = 'ENG'
    else:
        language = 'PL'
    if language == 'ENG':
        pg.display.set_caption("Tic Tac Toe Game")
    else:
        pg.display.set_caption("Gra Kółko i Krzyżyk")
    menu = False
    buttonPressed = 0
    pg.display.update()

    
# Funkcja restartująca rozdanie
def restart_game():
    global gameBoard, whoseWin, whatSign, draw, playerOneScore, playerTwoScore, whoseTurn, deal, gameReady, motion
    gameReady = False
    time.sleep(3)
    whatSign = 'x'
    if language == 'ENG':
        whoseTurn = 'Player 1 (X)'
    whoseTurn = 'Gracz 1 (X)'
    deal += 1
    draw = False
    motion = 0
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
    if menu == True:
        draw_menu()
    for incident in pg.event.get():
        if incident.type == QUIT:
            pg.quit()
            sys.exit()
        elif incident.type == MOUSEBUTTONDOWN and incident.button == 1:
            if menu == True:
                check_button()
            if buttonPressed == 1:
                menuSound.stop()
                menu = False   
                if gameReady == False:
                    draw_deal()
                    draw_lines()
                    draw_info()                    
                else:
                    check_board()
                    reset_variables()
                    if whoseWin or draw:
                        restart_game()
            if buttonPressed == 2:
                menuSound.stop() 
                menu = False  
                if gameReady == False:
                    pvc = True
                    draw_deal()
                    draw_lines()
                    draw_info()
                else:
                    check_board()
                    cpu_ai()
                    check_win()
                    reset_variables()
                    if whoseWin or draw:
                        restart_game()
            if buttonPressed == 3:
                menu = False
                if credits == False:
                    draw_authors() 
                else: 
                    check_authors()
            if buttonPressed == 4:
                menu=False
                change_language()
                menu=True
            if buttonPressed == 5:
                pg.quit()
                sys.exit()          
    pg.display.update()
    timer.tick(fps)
