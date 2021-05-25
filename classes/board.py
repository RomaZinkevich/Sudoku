import pygame
import numpy as np
import random
import sudoku_solver
import copy

BASE_FIELD = np.array(
    [[1, 2, 3, 4, 5, 6, 7, 8, 9],
     [4, 5, 6, 7, 8, 9, 1, 2, 3],
     [7, 8, 9, 1, 2, 3, 4, 5, 6],
     [2, 3, 4, 5, 6, 7, 8, 9, 1],
     [5, 6, 7, 8, 9, 1, 2, 3, 4],
     [8, 9, 1, 2, 3, 4, 5, 6, 7],
     [3, 4, 5, 6, 7, 8, 9, 1, 2],
     [6, 7, 8, 9, 1, 2, 3, 4, 5],
     [9, 1, 2, 3, 4, 5, 6, 7, 8]], dtype=np.uint8)


class Board:
    def __init__(self, width, height, screen, hearts):
        self.hearts = hearts
        self.screen = screen
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 90
        self.base_field = BASE_FIELD
        self.stop = False
        self.mix()
        self.field = copy.copy(self.base_field)
        self.chosen = []
        self.lifes = 3
        self.win = False
        self.quit = True

    def transpose(self):
        self.base_field = self.base_field.transpose()

    def swap_line_rows(self):
        area = random.randrange(0, 3)
        line1 = random.randrange(3 * area, 3 * area + 3)
        line2 = random.randrange(3 * area, 3 * area + 3)
        while line1 == line2:
            line2 = random.randrange(3 * area, 3 * area + 3)
        self.base_field[[line1, line2]] = self.base_field[[line2, line1]]

    def swap_line_colums(self):
        self.transpose()
        self.swap_line_rows()
        self.transpose()

    def swap_area_rows(self):
        area1 = random.randrange(0, 3)
        area2 = random.randrange(0, 3)
        while area1 == area2:
            area2 = random.randrange(0, 3)
        nums = []
        for i in range(area1 * 3, area1 * 3 + 3):
            nums.append(i)
        num1, num2, num3 = nums
        nums = []
        for i in range(area2 * 3, area2 * 3 + 3):
            nums.append(i)
        num4, num5, num6 = nums
        self.base_field[[num1, num2, num3, num4, num5, num6]
                        ] = self.base_field[[num4, num5, num6, num1, num2, num3]]

    def swap_area_colums(self):
        self.transpose()
        self.swap_area_rows()
        self.transpose()

    def mix(self):
        funcs = ['self.transpose()', 'self.swap_line_rows()', 'self.swap_area_rows()',
                 'self.swap_area_colums()', 'self.swap_line_colums()']
        for i in range(2000):
            func = random.randrange(0, 5)
            eval(funcs[func])

    def render(self, color):
        c = self.cell_size
        w = self.width
        h = self.height

        for i in range(w * h):
            y, x = divmod(i, w)
            x = x * c + self.left
            y = y * c + self.top
            pygame.draw.rect(
                self.screen, color, (x, y, c, c), 2)
        for i in range(3):
            for j in range(3):
                x = 270 * i + self.left
                y = 270 * j + self.top
                pygame.draw.rect(
                    self.screen, color, (x, y, 3 * c, 3 * c), 10)
        for i in range(self.lifes):
            self.screen.blit(self.hearts, (10 + i * 90, 820))
        if self.chosen != []:
            pygame.draw.rect(self.screen, 'blue', (int(
                self.chosen[0]), self.chosen[1], c, c), 15)
        f = pygame.font.Font(None, 100)
        while not self.stop:
            self.draw()
        if self.stop:
            for i in range(9):
                for j in range(9):
                    if self.base_field[i][j] == 10:
                        txt = ''
                    else:
                        txt = self.base_field[i][j]
                    num = f.render(str(txt), True, color)
                    self.screen.blit(num, (10 + 27 + 90 * j, 10 + 15 + 90 * i))

    def draw(self):
        row = random.randrange(0, 9)
        column = random.randrange(0, 9)
        sudoku = ''
        self.base_field[row][column] = 10
        for i in self.base_field:
            for j in i:
                sudoku += str(j)
        self.stop = sudoku_solver.solving(sudoku)

    def get_click(self, mouse_pos):
        if mouse_pos[1] < 820 and mouse_pos[0] > 15 and mouse_pos[0] < 815 and not self.win:
            cell = self.get_cell(mouse_pos)
            cell = self.on_click(cell)
            if cell == 10:
                self.chosen = [((mouse_pos[0] - 10) // 90 * 90) + 10,
                               ((mouse_pos[1] - 10) // 90 * 90) + 10]
            else:
                self.chosen = []
        if self.win:
            if int(mouse_pos[0]) >= 230 and int(mouse_pos[0]) <= 380 and int(mouse_pos[1]) >= 470 and int(mouse_pos[1]) <= 620:
                self.the_end()
            if int(mouse_pos[0]) >= 500 and int(mouse_pos[0]) <= 650 and int(mouse_pos[1]) >= 470 and int(mouse_pos[1]) <= 620:
                self.quit = False

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        w = (x - self.left) // self.cell_size
        h = (y - self.top) // self.cell_size
        if w in range(self.width) and h in range(self.height):
            return w, h

    def on_click(self, cell_coords):
        return self.base_field[cell_coords[1]][cell_coords[0]]

    def click(self, num):
        if self.chosen != [] and not self.win:
            field = self.get_cell(self.chosen)
            if int(num) == int(self.field[field[1]][field[0]]):
                self.base_field[field[1]][field[0]] = num
                self.chosen = []
            else:
                self.lifes -= 1
            if self.lifes == 0:
                self.the_end()
            if 10 not in self.base_field:
                self.won()

    def the_end(self):
        self.base_field = BASE_FIELD
        self.mix()
        self.field = copy.copy(self.base_field)
        self.stop = False
        self.chosen = []
        self.lifes = 3
        self.win = False

    def won(self):
        self.win = True
