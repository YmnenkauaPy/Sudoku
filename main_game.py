#Модули
from pygame import *
from random import choice, shuffle, randint
from funcs import *
import os
import time as tm
import locale

#Pygame
init()

play = True
width, height = (1000, 800)
screen = display.set_mode((width,height))
display.set_caption('СУДОКУ')
clock = time.Clock()
FPS = 60
background_image = image.load('Sudoku_menu.png')
board = transform.smoothscale(image.load('board.png'), (width, height))
background_image = transform.smoothscale(background_image, (width, height))
hint = transform.smoothscale(image.load('hint.png'), (100, 110))
cross = transform.smoothscale(image.load('cross.png'), (70, 70))
no = transform.smoothscale(image.load('no.png'), (50, 50))
yes = transform.smoothscale(image.load('yes.png'), (50, 50))

#Текст
font_dir = os.path.join(os.path.dirname(__file__))
font_path = os.path.join(font_dir, 'HachiMaruPop-Regular.ttf')
diff_font = font.Font(font_path, 41, bold=True)
num_font = font.Font(font_path, 35, bold=True)
win_font = font.Font(font_path, 50, bold=True)
set_font = font.Font(font_path, 30, bold=True)
size_c= 41 #размер надписи монеток

#Монеты
with open('coins.txt', 'r', encoding='utf-8') as f:
    money = f.readlines()[0]

mistakes = 0

rainbow_colors = [
    (255, 0, 0),     # Красный
    (255, 165, 0),   # Оранжевый
    (255, 255, 0),   # Желтый
    (0, 255, 0),     # Зеленый
    (0, 0, 255),     # Голубой
    (75, 0, 130),    # Синий
    (160, 50, 255)   # Фиолетовый
]

easy = diff_font.render('Easy', True, rainbow_colors[4])
medium = diff_font.render('Medium', True, rainbow_colors[1])
hard = diff_font.render('Hard', True, rainbow_colors[0])
difficult = diff_font.render('Difficult', True, (150,0,0))
coin = diff_font.render(money, True, (0,0,0))
timee = diff_font.render('0', True, (0,0,0))
keyboardtxt = set_font.render('keyboard', True, (0,0,0))
mousetxt = set_font.render('mouse', True, (0,0,0))

#Сложности, нужные переменные 
difs = {'easy':[20,30], 'medium':[30,35], 'hard':[35,45], 'difficult':[45,55]} #+random
dif = '' #сложность
field = '' #правильное поле
field2 = '' #поле с пустыми ячейками
numeric = '' #число, которое мы хотим поставить
n_ = 1 #Чтобы начислять монетки только 1 раз
bool = None #надпись результата
x_b, y_b = 390, 650 #x, y для кнопок сложности
keyboard = True #Режимы игры
mouse_ = False 
selected_square = None
key_ = None #для версии с мышкой

#Создаем поле
coordinates = create_grid() 
line_coordinates = line_coord()

selected_squares = set()
key_messages = {
    K_1: "1",
    K_2: "2",
    K_3: "3",
    K_4: "4",
    K_5: "5",
    K_6: "6",
    K_7: "7",
    K_8: "8",
    K_9: "9",
}

#Основая часть
while play:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            play = False

        elif e.type == MOUSEBUTTONDOWN:
            x_pos, y_pos = mouse.get_pos()
            #print(x_pos, y_pos)
            selected_square = check_click(x_pos, y_pos, coordinates, selected_square)
            if selected_square:
                # Добавляем или удаляем квадрат из множества выделенных квадратов
                if selected_square in selected_squares:
                    selected_squares.remove(selected_square)
                else:
                    selected_squares.add(selected_square)
            actions = {
                'easy':[250, 730, 390, 445],
                '':[835, 985, 0, 105],
                'medium':[250, 730, 460, 525],
                'hard':[250, 730, 530, 595],
                'difficult':[250, 730, 600, 660],
                choice(list(difs.keys())):[250, 730, 665, 730],
                'hint':[30, 140, 100, 265],
                'cross': [665, 725, 150, 215],
                'key' : [200, 245, 25, 60],
                'mouse' : [200, 245, 75, 115],
                '1' : [20, 50, 300, 330],
                '2' : [70, 115, 300, 335],
                '3' : [20, 60, 350, 380],
                '4' : [70, 110, 350, 390],
                '5' : [20, 60, 400, 435],
                '6' : [65, 110, 395, 435],
                '7' : [30, 60, 450, 485],
                '8' : [70, 110, 450, 485],
                '9' : [20, 65, 500, 535],
                'del' : [70, 105, 500, 530]
            }                 
            for i in actions:
                if x_pos >= actions[i][0] and x_pos <= actions[i][1] and y_pos >= actions[i][2] and y_pos <= actions[i][3]:
                    if i in ['easy', 'medium', 'hard', 'difficult'] and not dif:
                        dif = i
                        field, field2=playing_field(difs[dif][0], difs[dif][1], True, field2, field)
                        start_time = tm.time()
                    elif i == '' and dif:
                        dif = ''
                        bool = None
                        mistakes = 0
                    elif i == 'hint' and dif and bool == None and not int(money) < 100:
                        money = use_hint(field2,field)
                        field, field2=playing_field(difs[dif][0], difs[dif][1], False, field2, field)
                    elif i == 'cross' and dif and bool != None:
                        bool = 'End'
                    elif i == 'key' and not dif:
                        if not keyboard:
                            keyboard = True
                            mouse_ = False
                        else:
                            keyboard = False
                            mouse_ = True
                    elif i == 'mouse' and not dif:
                        if not mouse_:
                            keyboard = False
                            mouse_ = True
                        else:
                            keyboard = True
                            mouse_ = False     
                    elif i in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and dif and bool == None and selected_square:
                        numeric = i
                    elif i == 'del' and dif and bool == None and selected_square:
                        numeric = 0

        elif e.type == KEYDOWN and not mouse_:
            if e.key in key_messages and selected_square and not mistakes >= 5:
                numeric = key_messages[e.key]

            if e.key == K_BACKSPACE:
                numeric = 0
                check_right(selected_square, field, field2, numeric, mistakes)
                field, field2=playing_field(difs[dif][0], difs[dif][1], False, field2, field)

    if dif:
        #Текст, переменные
        mist = diff_font.render('Mistakes: ' + str(mistakes) +'/5', True, (0,0,0))
        diff = diff_font.render('Difficulty: ' + dif, True, (0,0,0))
        price = num_font.render('100', True, (0,0,0))

        coor = []
        n = 0
        #screen.blit
        screen.blit(board,(0,0))
        screen.blit(mist, (330, 7))
        screen.blit(diff, (30, 735))
        screen.blit(timee,(90,8))
        screen.blit(hint, (30,110))
        screen.blit(price, (45,220))

        #циклы for, функции
        coordinates = create_grid()
        net(field2, num_font, screen)
        dict = nums(field2)

        if mouse_:
            for i in nums_mouse():
                number = num_font.render(str(i), True, (90, 145, 150))
                screen.blit(number, nums_mouse()[i])

        for i in dict:
            num = num_font.render(str(i) + ': ' + str(dict[i]), True, (0,0,0))
            screen.blit(num, (820, 150+i*55))
        for x, y in coordinates:
            if selected_square != None:
                coor= square(selected_square, coordinates, field2)
            # Определяем цвет для квадратов
            if (x, y) == selected_square:
                color = (255,0,0)
                draw.rect(screen, (170,0,170), (x, y, 52, 52), 5)
                for i in coor:
                    x1,y1 = i
                    if (x1,y1) != (x,y):
                        draw.rect(screen, color, (x1,y1, 52, 52), 5)
            else:
                color = (0, 0, 0)
                draw.rect(screen, color, (x, y, 52, 52), 1)  # Рисуем квадраты

        # Отрисовываем линии
        for line in line_coordinates:
            draw.line(screen, (0, 0, 0), line[:2], line[2:], 7)  # Рисуем линии
        
        #Проверяем закончена ли игра
        for i in range(9):
            for j in range(9):
                if len(str(field2[i][j])) == 2:
                    if field2[i][j][1] == '.':
                        n += 1
                if field2[i][j] == 0:
                    n += 1
        if n == 0 and bool != 'End' or mistakes >= 5 and bool != 'End':    
            bool = win_lose(field,field2,mistakes)

        #Концовка
        if bool != None and bool != 'End':
            draw.rect(screen, (255, 255, 255), (225, 150, 510, 430))  # Рисуем квадрат
            end = win_font.render(bool, True, (0,0,0))
            if bool == 'YOU WIN' and not n_ > 1:
                n_+=1
                with open('coins.txt', 'r', encoding = 'utf-8') as f:
                    money = int(f.readline())+(100-6*mistakes)
                with open('coins.txt', 'w', encoding = 'utf-8') as f:
                    f.write(str(money))
            screen.blit(end, (300, 300))
            screen.blit(cross, (665, 150))

        if bool == None and bool != 'End':
            end_time = tm.time()
        #Проверка чисел
        if numeric != '':
            mistakes = check_right(selected_square, field, field2, numeric, mistakes)
            field, field2=playing_field(difs[dif][0], difs[dif][1], False, field2, field)
            numeric = ''
        #время
        minute,sec = int((end_time-start_time)//60), int((end_time-start_time)%60)
        timee = diff_font.render((f"{minute}:{sec:02}"), True, (0,0,0))
    
    #Меню
    if not dif:
        screen.blit(background_image, (0, 0))

        #Кнопки
        easy = diff_font.render('Easy', True, rainbow_colors[4])
        screen.blit(easy, (x_b, y_b//1.7))
        medium = diff_font.render('Medium', True, rainbow_colors[1])
        screen.blit(medium, (x_b, y_b//1.4))
        hard = diff_font.render('Hard', True, rainbow_colors[0])
        screen.blit(hard, (x_b, y_b-120))
        difficult = diff_font.render('Difficult', True, (150,0,0))
        screen.blit(difficult, (x_b, y_b-50))
        draw_text('Random', x_b+5, y_b+17, rainbow_colors, diff_font, screen)
        screen.blit(keyboardtxt, (20, 20))
        screen.blit(mousetxt, (20, 70))
        if not mouse_:
            screen.blit(yes, (200, 20))
            screen.blit(no, (200, 70))
        elif not keyboard:
            screen.blit(no, (200, 20))
            screen.blit(yes, (200, 70))
        # Форматируем число с разделителем запятой
        locale.setlocale(locale.LC_ALL, '')
        formatted_number = locale.format_string("%d", int(money), grouping=True)
        coin_font = font.Font(font_path, size_c, bold=True)
        coin = coin_font.render(str(formatted_number), True, (0,0,0))
        if len(str(money)) >= 7:
            size_c = 30
        else:
            size_c = 41

        if size_c == 41:
            screen.blit(coin, (730, 0))
        else:
            screen.blit(coin, (735, 10))

    display.update()
