#Модули
from pygame import *
import funcs
import os
import classes
import time as tm
import locale

#Pygame
init()

play = True
width, height = (800, 600)
new_width, new_height = (800, 600)
screen = display.set_mode((width,height), RESIZABLE)
display.set_caption('SUDOKU')

clock = time.Clock()
FPS = 60

#Текст
dir = os.path.join(os.path.dirname(__file__))
font_path = os.path.join(dir, 'HachiMaruPop-Regular.ttf')
font_path2 = os.path.join(dir, 'Symbola.ttf')
diff_font = font.Font(font_path, 30)
num_font = font.Font(font_path, 25)
win_font = font.Font(font_path, 40)
set_font = font.Font(font_path, 24)

#Монеты
with open(funcs.resource_path(dir + r'\coins.txt'), 'r', encoding='utf-8') as f:
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

clock_font = font.Font(font_path2, 60)
clock_txt = clock_font.render('⌚', True, (0,0,0))

#Сложности, нужные переменные 
difs = {'easy':[20,30], 'medium':[30,35], 'hard':[35,45], 'difficult':[45,55]} #+ random
dif = '' #сложность
field = '' #правильное поле
field2 = '' #поле с пустыми ячейками
numeric = '' #число, которое мы хотим поставить
n_ = 1 #Чтобы начислять монетки только 1 раз
bool = None #надпись результата
keyboard = True #Режимы игры
mouse_ = False 
selected_square = None
key_ = None #для версии с мышкой

#Создаем поле
coordinates = funcs.create_grid(new_width, new_height, width, height) 

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

        elif e.type == VIDEORESIZE:
            new_width, new_height = e.w, e.h
            if new_width < 550 or new_height < 425:
                new_width = max(new_width, 550)
                new_height = max(new_height, 425)
                display.set_mode((new_width, new_height), RESIZABLE)
                selected_square = None
            else:
                display.set_mode((new_width, new_height), RESIZABLE)
                selected_square = None

        elif e.type == MOUSEBUTTONDOWN:
            x_pos, y_pos = mouse.get_pos()
            selected_square = funcs.check_click(x_pos, y_pos, coordinates, selected_square, width, new_width, height, new_height)
            if selected_square:
                # Добавляем или удаляем квадрат из множества выделенных квадратов
                if selected_square in selected_squares:
                    selected_squares.remove(selected_square)
                else:
                    selected_squares.add(selected_square)

            mode = 'menu'

            if not dif:
                mode = 'menu'
                actions = funcs.actions_coor_menu(width, height, new_width, new_height, difs)

            if dif and mouse_:
                mode = 'game_mouse'
                actions = funcs.actions_coor_mouse(width, height, new_width, new_height)

            if dif and keyboard:
                mode = 'game_keys'
                actions = funcs.actions_coor_game(width, height, new_width, new_height)

            clicked_button = funcs.clicker(x_pos, y_pos, actions)
            
            #if actions were in menu's version
            if clicked_button and mode == 'menu':
                if clicked_button in ['easy', 'medium', 'hard', 'difficult'] and not dif:
                    dif = clicked_button
                    field, field2 = funcs.playing_field(difs[dif][0], difs[dif][1], True, field2, field, funcs.resource_path(dir + r'\field_right.txt'), funcs.resource_path(dir + r'\field.txt'))
                    start_time = tm.time()

                if (clicked_button == 'key' or clicked_button == 'mouse') and not dif:
                    if not keyboard:
                        keyboard = True
                        mouse_ = False
                    else:
                        keyboard = False
                        mouse_ = True  

                if clicked_button == 'help' and not dif:
                    file_path = funcs.os.path.join(dir, funcs.resource_path(dir + r'\Help.docx'))
                    if os.path.exists(file_path):
                        # Открытие файла
                        os.startfile(file_path)

            #if actions were in mouse's version
            if clicked_button and mode == 'game_mouse':
                if clicked_button == 'hint' and dif and bool == None and not int(money) < 100:
                    money = funcs.use_hint(field2,field, funcs.resource_path(dir + r'\coins.txt'))
                    field, field2 = funcs.playing_field(difs[dif][0], difs[dif][1], False, field2, field, funcs.resource_path(dir + r'\field_right.txt'), funcs.resource_path(dir + r'\field.txt'))
                
                if clicked_button == 'cross' and dif and bool != None:
                    bool = 'end'

                if clicked_button in ['1', '2', '3', '4', '5', '6', '7', '8', '9'] and dif and bool == None and selected_square:
                    numeric = clicked_button
                    
                if clicked_button == 'del' and dif and bool == None and selected_square:
                    numeric = 0

                if clicked_button == 'menu' and dif:
                    dif = ''
                    bool = None
                    mistakes = 0
                    n_ = 1

            #if actions were in keyboard's version
            if clicked_button and mode == 'game_keys':
                if clicked_button == 'hint' and dif and bool == None and not int(money) < 100:
                    money = funcs.use_hint(field2,field, funcs.resource_path(dir + r'\coins.txt'))
                    field, field2 = funcs.playing_field(difs[dif][0], difs[dif][1], False, field2, field, funcs.resource_path(dir + r'\field_right.txt'), funcs.resource_path(dir + r'\field.txt'))
                
                if clicked_button == 'cross' and dif and bool != None:
                    bool = 'end'
                
                if clicked_button == 'menu' and dif:
                    dif = ''
                    bool = None
                    mistakes = 0
                    n_ = 1
        
        elif e.type == KEYDOWN and not mouse_:
            if e.key in key_messages and selected_square and not mistakes >= 5:
                numeric = key_messages[e.key]

            if e.key == K_BACKSPACE and bool != 'end':
                numeric = 0
                field, field2 = funcs.playing_field(difs[dif][0], difs[dif][1], False, field2, field, funcs.resource_path(dir + r'\field_right.txt'), funcs.resource_path(dir + r'\field.txt'))
    
    #Игровое поле
    if dif:
        #Текст, переменные
        managercl = classes.ManagerClasses(screen, new_width, new_height)

        line_coordinates = funcs.line_coord(width, new_width, height, new_height)
        win_font = font.Font(font_path, int(40/width*new_width))
        cross = transform.smoothscale(image.load(funcs.resource_path(dir + r'\cross.png')), (56/width*new_width, 91/height*new_height))

        coor = []   
        n = 0
        #screen.blit
        screen.fill((255,255,255))
        managercl.manage('text', ['Mistakes: ' + str(mistakes) +'/5', font_path, int(25/width*new_width), 0, 264/width, 5/height, 300/width, 60/height, (0,0,0)])
        managercl.manage('text', ['Difficulty: ' + dif, font_path, int(25/width*new_width), 0, 15/width, 560/height, 340/width, 35/height, (0,0,0)])
        
        managercl.manage('text', ['$100', font_path, int(28/width*new_width), 0, 40/width, 180/height, 55/width, 28/height, (0,0,0)])
        managercl.manage('image', ['hint.png', 27/width, 79/height, (75/width,80/width), 85/width, 90/height, dir])
        managercl.manage('image', ['menu.png', 665/width, 10/height, (100/width,70/height), 100/width, 75/height, dir])

        num_font = font.Font(font_path, int(25/width*new_width))

        #циклы for, функции
        coordinates = funcs.create_grid(new_width, new_height, width, height)
        funcs.net(field2, num_font, screen, width, new_width, height, new_height)
        dict = funcs.nums(field2)

        if mouse_:
            for i in funcs.nums_mouse(width, height, new_width, new_height):
                number = num_font.render(str(i), True, (90, 145, 150))
                screen.blit(number, funcs.nums_mouse(width, height, new_width, new_height)[i])
        
        #Отрисовка сколько осталось циферок
        for i in dict:
            num = num_font.render(str(i) + ': ' + str(dict[i]), True, (0,0,0))
            screen.blit(num, (656/width*new_width, (80/height*new_height)+i*(36/height*new_height)))

        for x, y in coordinates:
            if selected_square != None:
                coor= funcs.square(selected_square, coordinates, field2, new_width, new_height, width, height)
            # Определяем цвет для квадратов
            if (x, y) == selected_square:
                color = (255,0,0)
                draw.rect(screen, (170,0,170), (x, y, 52/width*new_width, 52/height*new_height), 5)
                for i in coor:
                    x1,y1 = i
                    if (x1,y1) != (x,y):
                        draw.rect(screen, color, (x1,y1, 52/width*new_width, 52/height*new_height), 5)
            else:
                color = (0, 0, 0)
                draw.rect(screen, color, (x, y, 52/width*new_width, 52/height*new_height), 1)  # Рисуем квадраты

        # Отрисовываем линии
        for line in line_coordinates:
            draw.line(screen, (0, 0, 0), line[:2], line[2:], int(3/width*new_width))  # Рисуем линии
            
        #Проверяем закончена ли игра
        for i in range(9):
            for j in range(9):
                if len(str(field2[i][j])) == 2 and field2[i][j][1] == '.':
                    n += 1
                if field2[i][j] == 0:
                    n += 1
        if (n == 0 or mistakes >= 5) and bool != 'end':    
            bool = funcs.win_lose(field, field2, mistakes)

        #Концовка
        if bool and bool != 'end':
            draw.rect(screen, (255, 255, 255), (180/width*new_width, 115/height*new_height, int(400/width*new_width), int(330/height*new_height)))  # Рисуем квадрат
            end = win_font.render(bool, True, (0,0,0))
            if bool == 'YOU WIN' and n_ == 0:
                n_+=1
                with open(funcs.resource_path(dir + r'\coins.txt'), 'r', encoding = 'utf-8') as f:
                    money = int(f.readline())+(100-6*mistakes)
                with open(funcs.resource_path(dir + r'\coins.txt'), 'w', encoding = 'utf-8') as f:
                    f.write(str(money))
                    f.close()
            screen.blit(end, (240/width*new_width, 230/height*new_height))
            screen.blit(cross, (532/width*new_width, 115/height*new_height))

        if not bool:
            end_time = tm.time()

        #Проверка чисел
        if numeric != '':
            x,y = selected_square
            # Считаем координаты этой цифры в field2
            x = round(x/(60/width*new_width))-2
            y = round(y/(57/height*new_height))-1
            mistakes = funcs.check_right(x, y, field, field2, numeric, mistakes, funcs.resource_path(dir + r'\field.txt'))
            field, field2 = funcs.playing_field(difs[dif][0], difs[dif][1], False, field2, field, funcs.resource_path(dir + r'\field_right.txt'), funcs.resource_path(dir + r'\field.txt'))
            numeric = ''

        #время
        clock_font = font.Font(font_path2, int(50/width*new_width))
        clock_txt = clock_font.render('⌚', True, (0,0,0))
        screen.blit(clock_txt, (37/width*new_width, 8/height*new_height))
        managercl.manage('text', [(f"{tm.strftime('%H:%M:%S', tm.gmtime(end_time-start_time))}"),font_path, int(30/width*new_width), 0, 120/width, 6/height, 100/width, 50/height, (0,0,0)])
        
        if (end_time-start_time) > 604798 and bool != 'end':
            bool = funcs.win_lose(field, field2, mistakes)
    
    #Меню
    if not dif:      
        screen.fill((255,255,255))  
            
        #Текст
        managercl = classes.ManagerClasses(screen, new_width, new_height)

        managercl.manage('text', ['SUDOKU', font_path, 75, 2, 220/width, 145/height, 370/width, 75/height, (0, 185, 255)])
        managercl.manage('text', ['By Ymnenkaua', font_path, 20, 2, 30/width, 570/height, 200/width, 20/height, ((185, 135, 255))])

        #Кнопки
        managerbut = classes.ManagerButton(screen, new_width, new_height)

        managerbut.manage('button', ['Easy', 200/width, 293/height,384/width,55/height, diff_font, rainbow_colors[4]], None)
        managerbut.manage('button', ['Medium', 200/width, 345/height,384/width,55/height, diff_font, rainbow_colors[1]], None)
        managerbut.manage('button', ['Hard', 200/width, 397/height,384/width,55/height, diff_font, rainbow_colors[0]], None)
        managerbut.manage('button', ['Difficult', 200/width, 450/height,384/width,55/height, diff_font, (150, 0,0)], None)
        managerbut.manage('random', ['Random', 200/width, 500/height, 384/width, 55/height, diff_font, rainbow_colors], None)
        managerbut.manage('button', ['HELP', 560/width, 65/height, 220/width, 50/height, diff_font, (55, 140, 255)], None)

        if not mouse_:
            managerbut.manage('image', ['yes.png', dir, 'keyboard', 16/width, 15/height, 300/width, 50/height, diff_font, (0,0,0)], (30/height, 30/height))
            managerbut.manage('image', ['no.png', dir, 'mouse', 16/width, 60/height, 300/width, 50/height, diff_font, (0,0,0)], (30/height, 30/height))

        elif not keyboard:
            managerbut.manage('image', ['yes.png', dir, 'mouse', 16/width, 60/height, 300/width, 50/height, diff_font, (0,0,0)], (30/height, 30/height))
            managerbut.manage('image', ['no.png', dir, 'keyboard', 16/width, 15/height, 300/width, 50/height, diff_font, (0,0,0)], (30/height, 30/height))

        # Форматируем число с разделителем запятой
        locale.setlocale(locale.LC_ALL, '')
        formatted_number = locale.format_string("%d", int(money), grouping=True)
        managercl.manage('coins', ['$ ', str(formatted_number), font_path, 524/width, 0/height, 270/width, 50/height])

    display.update()
