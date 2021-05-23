import pygame
from classes import board as brd
import sudoku_solver

pygame.font.init()
screen = pygame.display.set_mode((830, 930))
pygame.display.set_caption("Судоку")

hearts = pygame.image.load('images/heart.png')
cross = pygame.image.load('images/cross.png')
retry = pygame.image.load('images/retry.png')
hearts = pygame.transform.scale(hearts, (90, 90))
cross = pygame.transform.scale(cross, (150, 150))
retry = pygame.transform.scale(retry, (150, 150))

board = brd.Board(9, 9, screen, hearts)
color = 'black'
running = True
while running and board.quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key >= 49 and event.key <= 57:
                board.click(event.unicode)
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

    pygame.display.flip()
