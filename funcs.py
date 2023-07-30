from random import choice, shuffle, randint
from pygame import *

#Функции
#поиск пустых ячеек
def empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i,j
    return False

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

#Генерация поля
def generate(minn,maxn):
    field = [[0 for i in range(9)] for i in range(9)]
    cell = True
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(9):
        cell = empty(field)
        row, col = cell
        shuffle(nums)
        chosen = nums.pop()
        field[row][col] = chosen
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    n = 0
    while cell is not None:
        cell = empty(field)
        if field[row].count(0) == 0:
            nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        row, col = cell
        while cell and field[row].count(0) != 0:
            if not cell:
                break
            row, col = cell
            shuffle(nums)
            chosen = choice(nums)
            if check(field, chosen, row, col) == False and n == 5:
                n = 0
                field[row] = [0] * 9 
                nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                break 
            if check(field, chosen, row, col) == False:
                n += 1
                break
            field[row][col] = chosen
            nums.remove(chosen)
            cell = empty(field)
        if not cell:
            break
    field2 = [row[:] for row in field]
    empty_cells = randint(minn,maxn+1) 
    cells = [(i, j) for i in range(9) for j in range(9)]
    shuffle(cells)

    for i, j in cells[:empty_cells]:
        field2[i][j] = 0
    return (field, field2)

def net(field2, num_font, screen):
    sign = {'.': (255,0,0), '!': (0,0,255), '+':(0,145,0)}
    for i in range(9):
        for j in range(9):
            x = j * 70
            y = i * 75
            if str(field2[i][j]) != '0':
                if len(str(field2[i][j])) == 2:
                    for b in sign:
                        if field2[i][j][1] == b:
                            num = num_font.render(str(field2[i][j])[0], True, sign[b])
                else:
                    num = num_font.render(str(field2[i][j]), True, (0,0,0))
                screen.blit(num, (x+175, y+90))

def create_grid():
    coordinates = []
    cycle = [[coordinates.append((col*70+170, row*75+90)) for col in range(9)]for row in range(9)]
    return coordinates

def line_coord():
    lines = []
    #Горизонтальные
    cycle = [lines.append((9*70+170, (row+1)*53+98, 150, (row+1)*53+98)) for row in range(9) if (row+1) % 4 == 0]
    #Вертикальные
    cycle = [lines.append(((col + 1) * 52+161, 9 * 70+105, (col + 1) * 52+161, 70)) for col in range(9) if (col+1) % 4 == 0]
    return lines

# Функция для проверки клика на квадрате сетки
def check_click(x_, y_, coordinates):
    for x, y in coordinates:
        if x <= x_ <= x + 55 and y <= y_ <= y + 56:
            # Возвращаем координаты выделенного квадрата
            return x, y
    return None
#Проверяем вставленные нами числа
def check_right(selected_square, field, field2, num, mistakes):
    x,y = selected_square
    # Считаем координаты этой цифры в field2
    x = round(x/75)-2
    y = int(y/76.6)-1
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

        with open('field.txt', 'w', encoding='utf-8') as f:
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
    dict = {}
    for i in field2:
        for j in i:
            if j != 0:
                if len(str(j)) == 2:
                    if str(j)[1] == '!' or str(j)[1] == '+':
                        dict.get(int(str(j)[0]), 0) +1
                else:
                    dict.get(j, 0)+1

    return dict

#Ищем все квадраты с одинаковыми цифрами
def square(selected_square, coordinates, field2):
    x,y = selected_square
    coor = []
    number = field2[int(y/76.6)-1][round(x/75)-2]
    for x,y in coordinates:
        if len(str(number)) == 2:
            number = int(number[0])
        if len(str(field2[int(y/76.6)-1][round(x/75)-2])) == 2:
            if int(field2[int(y/76.6)-1][round(x/75)-2][0]) == number:
                xy = x,y
                if field2[int(y/76.6)-1][round(x/75)-2] != 0:
                    coor.append(xy)
        else:
            if field2[int(y/76.6)-1][round(x/75)-2] == number:
                xy = x,y
                if field2[int(y/76.6)-1][round(x/75)-2] != 0:
                    coor.append(xy)
    return coor

#Подсказки
def use_hint(field2, field):
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
    with open('coins.txt', 'r', encoding='utf-8') as f:
        money = int(f.readlines()[0]) - 100
    with open('coins.txt', 'w', encoding = 'utf-8') as f:
        f.write(str(money))
    return money

#Функция для радужной кнопки
def draw_text(text, x, y, rainbow_colors, diff_font, screen):
    color_index = 0

    for char in text:
        color = rainbow_colors[color_index % len(rainbow_colors)]
        rendered_char = diff_font.render(char, True, color)
        screen.blit(rendered_char, (x, y))
        x += rendered_char.get_width()
        color_index += 1

#Генерация поля
def playing_field(minn,maxn, gen, field2, field):
    if gen == True:
        field, field2 = generate(minn,maxn)
        with open('field_right.txt', 'w', encoding='utf-8') as f:
            for row in field:
                f.write(' '.join(str(num) for num in row))
                f.write('\n')

    with open('field.txt', 'w', encoding='utf-8') as f:
        for row in field2:
            f.write(' '.join(str(num) if num != 0 else '_' for num in row))
            f.write('\n')
    return field,field2