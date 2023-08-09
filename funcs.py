from random import shuffle, randint, choice
import os, sys
from pygame import *

#Функции
#поиск пустых ячеек
def empty(board):
    empty_cells = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    return empty_cells

#Проверка на совместимость
def check(field,chosen,row, col):
    for i in range(9):
        if field[row][i] == chosen or field[i][col] == chosen:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)         
    for i in range(3):
        for j in range(3):
            if field[start_row + i][start_col + j] == chosen:
                return False
    return True

def generate(minn, maxn):
    def generate_recursive(field, empty_cells):
        if not empty_cells:
            return True

        row, col = empty_cells[0]
        for num in nums:
            if check(field, num, row, col):
                field[row][col] = num
                if generate_recursive(field, empty_cells[1:]):
                    return True
                field[row][col] = 0

        return False
    
    field = [[0 for _ in range(9)] for _ in range(9)]
    nums = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    generate_recursive(field, empty(field))

    field2 = [row[:] for row in field]
    empty_cells = randint(minn, maxn)
    cells = [(i, j) for i in range(9) for j in range(9)]
    shuffle(cells)

    for i, j in cells[:empty_cells]:
        field2[i][j] = 0

    return (field, field2)

#Генерация поля
def playing_field(minn,maxn, gen, field2, field, path, path2):
    if gen == True:
        field, field2 = generate(minn,maxn)
        with open(path, 'w', encoding='utf-8') as f:
            for row in field:
                f.write(' '.join(str(num) for num in row))
                f.write('\n')

    with open(path2, 'w', encoding='utf-8') as f:
        for row in field2:
            f.write(' '.join(str(num) if num != 0 else '_' for num in row))
            f.write('\n')
    return field,field2


def net(field2, num_font, screen, width, new_width, height, new_height):
    sign = {'.': (255,0,0), '!': (0,0,255), '+':(0,145,0)}
    for i in range(9):
        for j in range(9):
            x = j * (55/width)*new_width
            y = i * (55/height)*new_height
            if str(field2[i][j]) != '0':
                if len(str(field2[i][j])) == 2:
                    for b in sign:
                        if field2[i][j][1] == b:
                            num = num_font.render(str(field2[i][j])[0], True, sign[b])
                else:
                    num = num_font.render(str(field2[i][j]), True, (0,0,0))
                screen.blit(num, (x+(145/width)*new_width, y+(70)/height*new_height))

def create_grid(new_width, new_height, width, height):
    coordinates = []
    for row in range(9):
        for col in range(9):
            coordinates.append((col*(55/width*new_width)+136/width*new_width, row*(55/height*new_height)+69/height*new_height))
    return coordinates

def line_coord(width, new_width, height, new_height):
    lines = []
    #Горизонтальные
    for row in range(9):
        if (row+1)%4 == 0:
            lines.append((9*(50/width*new_width)+(170/width*new_width), (row+1)*(41/height*new_height)+(65/height*new_height), 140/width*new_width, (row+1)*(41/height*new_height)+(65/height*new_height)))
    #Вертикальные
    for col in range(9):
        if (col+1)%4 == 0:
            lines.append(((col + 1)*(41/width*new_width)+(135/width*new_width), 9*(53/height*new_height)+(81/height*new_height), (col + 1) * (41/width*new_width)+(135/width*new_width), 62/height*new_height))
    return lines


# Функция для проверки клика на квадрате сетки
def check_click(x_, y_, coordinates, selected_square, width, new_width, height, new_height):
    for x, y in coordinates:
        if x <= x_ <= x + 44/width*new_width and y <= y_ <= y + 43/height*new_height:
            # Возвращаем координаты выделенного квадрата
            return x, y
        elif x_ >= 16/width*new_width and x_ <= 88/width*new_width and y_ >= 227/height*new_height and y_ <= 408/height*new_height:
            return selected_square
    return None

#Проверяем вставленные нами числа
def check_right(selected_square, field, field2, num, mistakes, width, height, new_width, new_height, path):
    x,y = selected_square
    # Считаем координаты этой цифры в field2
    x = round(x/(60/width*new_width))-2
    y = round(y/(57/height*new_height))-1
    numr = str(field[y][x])
    if field2[y][x] == 0 or len(str(field2[y][x])) == 2:
        if len(str(field2[y][x])) == 2:
            if str(field2[y][x])[1] == '!' or str(field2[y][x])[1] == '+':
                return mistakes
            else:
                if num == numr:
                    field2[y][x] = str(num) + '!'

                elif num != numr and num != 0:
                    field2[y][x] = str(num) + '.'
                    mistakes += 1

                elif num == 0:
                    field2[y][x] = num
        else:
            if num == numr:
                field2[y][x] = str(num) + '!'

            elif num != numr and num != 0:
                field2[y][x] = str(num) + '.'
                mistakes += 1
        with open(path, 'w', encoding='utf-8') as f:
                for row in field2:
                    f.write(' '.join(str(nums) for nums in row))
                    f.write('\n')
    return mistakes
#Проверка проигрыша или выигрыша
def win_lose(field,field2, mistakes):
    if mistakes >= 5:
        return 'YOU LOSE'
    #Считает все "за" и "против"
    yes = sum([1 for i in range(9) for j in range(9) if str(field2[i][j])[0] == str(field[i][j])])
    no = sum([1 for i in range(9) for j in range(9) if str(field2[i][j])[0] != str(field[i][j])])
    if no == 0 and yes == 81:
        no,yes = 0,0
        return 'YOU WIN'
    elif yes != 81 and no !=0:
        no,yes = 0,0
        return 'YOU LOSE'
    return None

#Сколько осталось чисел каждого вида
def nums(field2):
    dict = {1: 9, 2:9, 3:9, 4:9, 5:9, 6:9, 7:9, 8:9, 9:9}
    for i in field2:
        for j in i:
            if j != 0:
                if len(str(j)) == 2:
                    if j[1] == '.':
                        continue
                dict[int(str(j)[0])]=dict[int(str(j)[0])]-1

    return dict

#Ищем все квадраты с одинаковыми цифрами
def square(selected_square, coordinates, field2, width, height, new_width, new_height):
    x,y = selected_square
    coor = []
    number = field2[round((y/57)/height*new_height)-1][round((x/60)/width*new_width)-2]
    for x,y in coordinates:
        if len(str(number)) == 2:
            number = int(number[0])
        if len(str(field2[round((y/57)/height*new_height)-1][round((x/60)/width*new_width)-2])) == 2:
            if int(field2[round((y/57)/height*new_height)-1][round((x/60)/width*new_width)-2][0]) == number:
                xy = x,y
                if field2[round((y/57)/height*new_height)-1][round((x/60)/width*new_width)-2] != 0:
                    coor.append(xy)
        else:
            if field2[round((y/57)/height*new_height)-1][round((x/60)/width*new_width)-2] == number:
                xy = x,y
                if field2[round((y/57)/height*new_height)-1][round((x/60)/width*new_width)-2] != 0:
                    coor.append(xy)
    return coor

#Подсказки
def use_hint(field2, field, path):
    n = sum(1 for i in range(9) for j in range(9) if field2[i][j] == 0)
    rand = randint(1, n)
    b=0
    for i in range(9):
        for j in range(9):
            if field2[i][j] == 0:
                b +=1
                if b == rand:
                    field2[i][j] = field[i][j]
                    field2[i][j] = str(field2[i][j]) + '+'
                    with open('field.txt', 'w', encoding='utf-8') as f:
                        for row in field2:
                            f.write(' '.join(str(nums) for nums in row))
                            f.write('\n')
    with open(path, 'r', encoding='utf-8') as f:
        money = int(f.readline()) - 100
    with open(path, 'w', encoding = 'utf-8') as f:
        f.write(str(money))
    return money        

def nums_mouse(width, height, new_width, new_height):
    nums = {}
    x, y = -16/width*new_width, 185/height*new_height
    for i in range(1,10):
        if i%2 != 0:
            nums[i] = [x+40/width*new_width,y+38/height*new_height]
            x,y = x+40/width*new_width,y+38/height*new_height
        else:
            nums[i] = [x+40/width*new_width,y]
            x -=40/width*new_width
    nums['x'] = [x+40/width*new_width,y]
    return nums

#Проверяет какая кнопка (квадрат) был(а) нажат(а)
def clicker(width, height, new_width, new_height, x_pos, y_pos, difs):
    actions = {
        'easy': [200/width*new_width, 584/width*new_width, 300/height*new_height, 342/height*new_height],
        'menu': [668/width*new_width, 788/width*new_width, 0/height*new_height, 81/height*new_height],
        'medium': [200/width*new_width, 584/width*new_width, 354/height*new_height, 404/height*new_height],
        'hard': [200/width*new_width, 584/width*new_width, 408/height*new_height, 458/height*new_height],
        'difficult': [200/width*new_width, 584/width*new_width, 462/height*new_height, 508/height*new_height],
        choice(list(difs.keys())): [200/width*new_width, 584/width*new_width, 512/height*new_height, 562/height*new_height],
        'hint': [30/width*new_width, 100/width*new_width, 80/height*new_height, 155/height*new_height],
        'cross': [524/width*new_width, 575/width*new_width, 120/height*new_height, 195/height*new_height],
        'key': [20/width*new_width, 300/width*new_width, 20/height*new_height, 60/height*new_height],
        'mouse': [20/width*new_width, 300/width*new_width, 60/height*new_height, 115/height*new_height],
        '1': [20/width*new_width, 40/width*new_width, 228/height*new_height, 250/height*new_height],
        '2': [55/width*new_width, 85/width*new_width, 229/height*new_height, 252/height*new_height],
        '3': [20/width*new_width, 46/width*new_width, 267/height*new_height, 292/height*new_height],
        '4': [56/width*new_width, 89/width*new_width, 264/height*new_height, 292/height*new_height],
        '5': [20/width*new_width, 46/width*new_width, 305/height*new_height, 329/height*new_height],
        '6': [58/width*new_width, 86/width*new_width, 304/height*new_height, 329/height*new_height],
        '7': [20/width*new_width, 48/width*new_width, 343/height*new_height, 367/height*new_height],
        '8': [59/width*new_width, 86/width*new_width, 339/height*new_height, 372/height*new_height],
        '9': [18/width*new_width, 46/width*new_width, 379/height*new_height, 403/height*new_height],
        'del': [58/width*new_width, 84/width*new_width, 379/height*new_height, 403/height*new_height],
        'help': [555/width*new_width, 775/width*new_width, 70/height*new_height, 100/height*new_height]
    }
    for i in actions:
        if x_pos > actions[i][0] and x_pos < actions[i][1] and y_pos > actions[i][2] and y_pos < actions[i][3]:
            return i
    return None

#files
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
