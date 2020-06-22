import pygame
import random

pygame.init()
winHeight = 700
winWidth = 900
win = pygame.display.set_mode((winWidth,winHeight))

BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREY = (209,209,209)
BLUE = (0,0,255)

pygame.display.set_caption('Hangman Game')
icon = pygame.image.load('assets/logo.png')
pygame.display.set_icon(icon)
btn_font = pygame.font.SysFont("consolas", 18)
guess_font = pygame.font.SysFont("monospace", 24)
maintitle_font = pygame.font.SysFont('yanmartext', 75)
title_font = pygame.font.SysFont('consolas', 20)
replaytitle_font = pygame.font.SysFont('consolas', 15)
background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (900, 750))
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('assets/hangman0.png'), pygame.image.load('assets/hangman1.png'), pygame.image.load('assets/hangman2.png'), pygame.image.load('assets/hangman3.png'), pygame.image.load('assets/hangman4.png'), pygame.image.load('assets/hangman5.png'), pygame.image.load('assets/hangman6.png')]

limbs = 0


def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(BLACK)
    win.blit(background, (0,0))
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (int(buttons[i][1]), int(buttons[i][2])), int(buttons[i][3]))
            pygame.draw.circle(win, buttons[i][0], (int(buttons[i][1]), int(buttons[i][2])), int(buttons[i][3]) - 2)
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, WHITE)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1,(winWidth/2 - length/2, 650))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()


def randomWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]


def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False


def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if x == 0:
            spacedWord += word[x].upper() + ' '
        elif x == len(word) - 1:
            spacedWord += word[x].upper() + ' '
        else:
            if word[x] != ' ':
                spacedWord += '_ '
                for i in range(len(guessedLetters)):
                    if word[x].upper() == guessedLetters[i]:
                        spacedWord = spacedWord[:-2]
                        spacedWord += word[x].upper() + ' '
            elif word[x] == ' ':
                spacedWord += ' '
    return spacedWord
            

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None


def end(winner=False):
    global limbs
    lostTxt = 'YOU LOST'
    winTxt = 'YOU WON'
    redraw_game_window()
    pygame.time.delay(1000)
    win.fill(BLACK)

    if winner == True:
        label = maintitle_font.render(winTxt, 1, WHITE)
    else:
        label = maintitle_font.render(lostTxt, 1, WHITE)

    wordTxt = title_font.render(word.upper(), 1, WHITE)
    wordWas = title_font.render('The phrase was: ', 1, WHITE)
    goNext = replaytitle_font.render('Press any button to play again', 1, WHITE)
    dontgoNext = replaytitle_font.render('Press Esc to quit', 1, WHITE)
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    win.blit(wordWas, (winWidth / 2 - wordWas.get_width() / 2, 245))
    win.blit(wordTxt, (winWidth / 2 - wordTxt.get_width() / 2, 295))
    win.blit(goNext, (winWidth / 2 - goNext.get_width() / 2, 625))
    win.blit(dontgoNext, (winWidth / 2 - dontgoNext.get_width() / 2, 650))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                again = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                again = False
    reset()


def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()

# Setup buttons
increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([RED, x, y, 20, True, 65 + i])

word = randomWord()
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        limbs += 1
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()