import numpy as np
import copy


def solve(sudoku):
    NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    sudoku_np = np.array([sudoku])
    for u in range(9):
        cube = [sudoku[0 + 3 * (u // 3)][(u % 3) * 3:(u % 3) * 3 + 3], sudoku[1 + 3 * (u // 3)]
                [(u % 3) * 3:(u % 3) * 3 + 3], sudoku[2 + 3 * (u // 3)][(u % 3) * 3:(u % 3) * 3 + 3]]

        cube_in_lines = sudoku[0 + 3 * (u // 3)][(u % 3) * 3:(u % 3) * 3 + 3] + sudoku[1 +
                                                                                       3 * (u // 3)][(u % 3) * 3:(u % 3) * 3 + 3] + sudoku[2 + 3 * (u // 3)][(u % 3) * 3:(u % 3) * 3 + 3]
        all_nums = []
        needed_nums = copy.copy(NUMS)
        for i in cube_in_lines:
            if i != " " and i != "":
                all_nums.append(int(i))
                needed_nums.remove(int(i))
        for j, i in enumerate(cube_in_lines):
            if i == " " or i == "":
                y = j % 3
                x = j // 3
                x, y = x + (u // 3) * 3, y + (u % 3) * 3
                row = sudoku[x]
                sudoku_np = sudoku_np.transpose()
                column = sudoku_np[y]
                sudoku_np = sudoku_np.transpose()
                lil_needed_nums = copy.copy(NUMS)
                for ululu, k in enumerate([row, column, cube_in_lines]):
                    for q in k:
                        if q != "" and q != " " and int(q) in lil_needed_nums:
                            lil_needed_nums.remove(int(q))
                if len(lil_needed_nums) == 1:
                    sudoku[x][y] = lil_needed_nums[0]
                    return sudoku


def solving(sudoku):
    sudoku = sudoku.replace('10', ' ')
    sudoku1 = []
    for i in range(9):
        row = []
        for j in range(9):
            a = sudoku[j + i * 9]
            row.append(a)
        sudoku1.append(row)
        row = []
    for i in range(50):
        if ' ' in sudoku:
            sudoku1 = solve(sudoku1)
            sudoku = ''
            try:
                for i in sudoku1:
                    for j in i:
                        sudoku += str(j)
            except:
                return True
        elif ' ' not in sudoku:
            return False
        else:
            return True
