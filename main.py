import pygame
from classes import board as brd
import sudoku_solver
import sys

NUM_NUMS = {1073741913: 1,
            1073741905: 2,
            1073741915: 3,
            1073741904: 4,
            1073741917: 5,
            1073741903: 6,
            1073741919: 7,
            1073741906: 8,
            1073741921: 9}

pygame.font.init()
screen = pygame.display.set_mode((830, 930))
pygame.display.set_caption("Судоку")
clock = pygame.time.Clock()

hearts = pygame.image.load('images/heart.png')
cross = pygame.image.load('images/cross.png')
retry = pygame.image.load('images/retry.png')
top = pygame.image.load('images/top.png')
hearts = pygame.transform.scale(hearts, (90, 90))
cross = pygame.transform.scale(cross, (150, 150))
retry = pygame.transform.scale(retry, (150, 150))
top = pygame.transform.scale(top, (100, 100))


color = 'black'


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 265 and event.pos[0] <= 565:
                    if event.pos[1] >= 250 and event.pos[1] <= 350:  # easy
                        board = brd.Board(9, 9, screen, hearts, 30, "EASY")
                        game(board)
                    elif event.pos[1] >= 550 and event.pos[1] <= 650:  # hard
                        board = brd.Board(9, 9, screen, hearts, 40, "HARD")
                        game(board)
                if event.pos[0] >= 215 and event.pos[0] <= 615 and event.pos[1] >= 400 and event.pos[1] <= 500:  # medium
                    board = brd.Board(9, 9, screen, hearts, 35, "MEDIUM")
                    game(board)
                if event.pos[0] >= 350 and event.pos[0] <= 480 and event.pos[1] >= 715 and event.pos[1] <= 845:
                    print("top")
        clock.tick(100)
        screen.fill('white')
        f = pygame.font.Font(None, 180)
        f2 = pygame.font.Font(None, 130)
        txt = f.render("SUDOKU", True, 'black')
        easy = f2.render("EASY", True, 'black')
        medium = f2.render("MEDIUM", True, 'black')
        hard = f2.render("HARD", True, 'black')
        screen.blit(txt, (150, 50))
        for i in range(2):
            pygame.draw.rect(screen, 'black', (265, 250 + i * 300, 300, 100),
                             8, border_radius=30)
        pygame.draw.rect(screen, 'black', (215, 400, 400, 100),
                         8, border_radius=30)
        pygame.draw.rect(screen, 'black', (350, 715, 130, 130),
                         8, border_radius=30)
        screen.blit(easy, (290, 260))
        screen.blit(medium, (235, 410))
        screen.blit(hard, (285, 560))
        screen.blit(top, (365, 730))
        pygame.display.flip()


def game(board):
    global color
    running = True
    while running and board.quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key >= 49 and event.key <= 57:
                    board.click(event.unicode)
                elif event.key in NUM_NUMS:
                    board.click(NUM_NUMS[event.key])
        screen.fill((255, 255, 255))
        board.render(color)
        if board.win:
            f = pygame.font.Font(None, 200)
            txt = f.render("YOU WIN!", True, 'black')
            screen.blit(txt, (100, 350))
            screen.blit(cross, (500, 470))
            screen.blit(retry, (230, 470))
            color = (100, 100, 100)
        else:
            color = 'black'
        clock.tick(100)
        pygame.display.flip()


start_screen()
