import pygame
import random
# initialize 
pygame.init()

# colors
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#fonts
btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('arial', 45)


# create the screen
winHeight = 480
winWidth = 700
win_size = (winWidth,winHeight)
win = pygame.display.set_mode(win_size)
pygame.display.set_caption("Hangman")
running = True
clock = pygame.time.Clock()
# we have 26 buttons for 26 chars
word = ''
buttons = [] 
guessed = []
hangmanPics = [pygame.image.load('/Users/zhangyuchen/Documents/code/pygame/wordguess/hangman0.png'), pygame.image.load('/Users/zhangyuchen/Documents/code/pygame/wordguess/hangman1.png'), pygame.image.load('/Users/zhangyuchen/Documents/code/pygame/wordguess/hangman2.png'), pygame.image.load('/Users/zhangyuchen/Documents/code/pygame/wordguess/hangman3.png'), pygame.image.load('/Users/zhangyuchen/Documents/code/pygame/wordguess/hangman4.png'), pygame.image.load('/Users/zhangyuchen/Documents/code/pygame/wordguess/hangman5.png'), pygame.image.load('/Users/zhangyuchen/Documents/code/pygame/wordguess/hangman6.png')]

limbs = 0
# setup buttons
space = win_size[0] // 13
for i in range(1,27):
    if i < 14:
        x = 25 + space * (i - 1)
        y = 40
    else:
        x = 25 + space * (i - 14)
        y = 90
    buttons += [[WHITE, x, y, 20, True, 65 + i - 1]]

# functions
def draw_game():
    global guessed
    global hangmanPics
    global limbs
    # print(buttons)
    win.fill(GREEN)
    for idx, btn in enumerate(buttons):
        if btn[4]:
            pygame.draw.circle(win, BLACK,(btn[1],btn[2]),btn[3])
            pygame.draw.circle(win, btn[0],(btn[1],btn[2]),btn[3] - 2)
            label = btn_font.render(chr(btn[5]),1,BLACK)
            pos = [btn[1]-(label.get_width())/2,btn[2]-(label.get_height())/2]
            win.blit(label, pos)
    
    spaced = spaces(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1,(winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()
    # clock.tick(10)

def select_word():
    file = open('/Users/zhangyuchen/Documents/code/pygame/wordguess/words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]

def guess_and_hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False

def spaces(word, guess=[]):
    spaced_word = ""
    guessed_letter = guess
    for x in range(len(word)):
        if word[x] != ' ':
            spaced_word += '_ '
            for i in range(len(guessed_letter)):
                if word[x].upper() == guessed_letter[i]:
                    spaced_word = spaced_word[:-2]
                    spaced_word += word[x].upper() + " "
        elif word[x] == ' ':
            spaced_word += ' '
    return spaced_word


def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None
    

def end(winner=False):
    global limbs
    lostTxt = 'You Lost! press any key to play again...'
    winTxt = 'You Win! press any key to play again...'
    draw_game()
    pygame.time.delay(1000)
    win.fill(GREEN)

    if winner == True:
        label = lost_font.render(winTxt, 1, BLACK)
    else:
        label = lost_font.render(lostTxt, 1, BLACK)

    wordTxt = lost_font.render(word.upper(), 1, BLACK)
    wordWas = lost_font.render('The phrase was: ', 1, BLACK)

    win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, 295))
    win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
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
    word = select_word()

word = select_word()
# starts 
while running:
    
    draw_game()
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                # print(chr(letter),len(buttons),len(buttons[0]))
                buttons[letter - 65][4] = False
                if guess_and_hang(chr(letter)):
                    if limbs < 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spaces(word, guessed))
                    if spaces(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()