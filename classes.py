from pygame import *
from funcs import resource_path


class Button():
    def __init__(self, text, image, x_rel, y_rel, width_rel, height_rel, font, color, dir):
        self.text = text
        self.font = font
        self.x_rel, self.y_rel = x_rel, y_rel
        self.color = color
        self.width_rel = width_rel  # Относительная ширина
        self.height_rel = height_rel  # Относительная высота
        self.image = image
        self.dir = dir
    def draw(self, screen, width, height, size):
        if self.image == None and size == None:
            # Вычисляем абсолютные координаты и размеры на основе текущего размера экрана
            x_abs = self.x_rel * width
            y_abs = self.y_rel * height
            width_abs = self.width_rel * width
            height_abs = self.height_rel * height

            rect = Rect(x_abs, y_abs, width_abs, height_abs)
            draw.rect(screen, (255,255,255), rect)
            if self.text != 'Random':
                text_surface = self.font.render(self.text, True, self.color)
                text_rect = text_surface.get_rect(center=rect.center)
            # Рисуем верхний бордюр
            draw.rect(screen, (0,0,0), (x_abs, y_abs, width_abs, 3))
            # Рисуем нижний бордюр
            draw.rect(screen, (0,0,0), (x_abs, y_abs + height_abs - 3, width_abs, 3))
            # Рисуем левый бордюр
            draw.rect(screen, (0,0,0), (x_abs, y_abs, 3, height_abs))
            # Рисуем правый бордюр
            draw.rect(screen, (0,0,0), (x_abs + width_abs - 3, y_abs, 3, height_abs))

            if self.text == 'Random':
                color_index = 0
                n = 0
                for char in self.text:
                    color_ = self.color[color_index % len(self.color)]
                    text_surface = self.font.render(char, True, color_)
                    text_rect = text_surface.get_rect(center=rect.center)
                    text_rect[0] -= 50
                    screen.blit(text_surface, (text_rect[0]+n, text_rect[1]))
                    n += 20
                    color_index += 1
            if self.text != 'Random':
                screen.blit(text_surface, text_rect)
        else:
            # Вычисляем абсолютные координаты и размеры на основе текущего размера экрана
            x_size, y_size = size
            x_abs = self.x_rel * width
            y_abs = self.y_rel * height
            width_abs = self.width_rel * width
            height_abs = self.height_rel * height
            self.image = resource_path(self.dir+r"\ "+self.image)
            self.image = self.image.replace(' ', '')
            image_ = transform.smoothscale(image.load(resource_path(self.image)), (x_size*height, y_size*height))
            rect = Rect(x_abs, y_abs, width_abs, height_abs)
            draw.rect(screen, (255,255,255), rect)
            
            text_surface = self.font.render(self.text, True, self.color)
            text_rect = text_surface.get_rect(midleft=rect.midleft)

            # Рисуем верхний бордюр
            draw.rect(screen, (0,0,0), (x_abs, y_abs, width_abs, 1))
            # Рисуем нижний бордюр
            draw.rect(screen, (0,0,0), (x_abs, y_abs + height_abs - 1, width_abs, 1))
            # Рисуем левый бордюр
            draw.rect(screen, (0,0,0), (x_abs, y_abs, 1, height_abs))
            # Рисуем правый бордюр
            draw.rect(screen, (0,0,0), (x_abs + width_abs - 1, y_abs, 1, height_abs))

            text_rect[0]+=5
            screen.blit(text_surface, text_rect)
            text_rect[0]+=170
            text_rect[1]+=12
            screen.blit(image_, text_rect)

class Coins():
    def __init__(self, text, text2, font_path, x_rel, y_rel, width_rel, height_rel):
        self.text = text
        self.text2 = text2
        self.font2 = font.Font(font_path, 25)
        self.font = font.Font(font_path, 30)
        self.x_rel, self.y_rel = x_rel, y_rel
        self.width_rel = width_rel  # Относительная ширина
        self.height_rel = height_rel  # Относительная высота

    def draw(self, screen, width, height):
        x_abs = self.x_rel * width
        y_abs = self.y_rel * height
        width_abs = self.width_rel * width
        height_abs = self.height_rel * height
            
        rect = Rect(x_abs, y_abs, width_abs, height_abs)
        draw.rect(screen, (255,255,255), rect)
        text_surface = self.font.render(self.text, True, (200,200,0))
        text_surface2 = self.font2.render(self.text2, True, (0,0,0))
        text_rect = text_surface2.get_rect(center=rect.center)

        # Рисуем верхний бордюр
        draw.rect(screen, (0,0,0), (x_abs, y_abs, width_abs, 1))
        # Рисуем нижний бордюр
        draw.rect(screen, (0,0,0), (x_abs, y_abs + height_abs - 1, width_abs, 1))
        # Рисуем левый бордюр
        draw.rect(screen, (0,0,0), (x_abs, y_abs, 1, height_abs))
        # Рисуем правый бордюр
        draw.rect(screen, (0,0,0), (x_abs + width_abs - 1, y_abs, 1, height_abs))
        text_rect[0]-=20
        text_rect[1]-=8
        screen.blit(text_surface, text_rect)
        text_rect[1]+=8
        text_rect[0]+=20
        screen.blit(text_surface2, text_rect)

class Text():
    def __init__(self, text, font_path, size_font, size_outline, x_rel, y_rel, width_rel, height_rel, color):
        self.text = text
        self.font = font.Font(font_path, size_font)
        self.size_outline = size_outline
        self.x_rel, self.y_rel = x_rel, y_rel
        self.width_rel = width_rel  # Относительная ширина
        self.height_rel = height_rel  # Относительная высота
        self.color = color

    def draw(self, screen, width, height):
        x_abs = self.x_rel * width
        y_abs = self.y_rel * height
        width_abs = self.width_rel * width
        height_abs = self.height_rel * height
            
        rect = Rect(x_abs, y_abs, width_abs, height_abs)
        draw.rect(screen, (255,255,255), rect)
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect(center=rect.center)

        # Создание поверхности для текста с обводкой
        text_surface2 = self.font.render(self.text, True, (0,0,0))
        outline_surface = Surface(text_surface.get_size(), SRCALPHA)

        # Рисуем обводку вокруг каждого символа
        outline_offset = self.size_outline  # Размер обводки (можно настроить по вашему усмотрению)
        for dx in range(-outline_offset, outline_offset + 1):
            for dy in range(-outline_offset, outline_offset + 1):
                if dx == 0 and dy == 0:
                    continue  # Пропускаем рисование исходного текста, чтобы не было дублирования
                outline_surface.blit(text_surface2, (dx, dy))

        screen.blit(outline_surface, text_rect)
        screen.blit(text_surface, text_rect)

class Image():
    def __init__(self, image, x_rel, y_rel, size, width_rel, height_rel,dir):
        self.image = image
        self.x_rel, self.y_rel = x_rel, y_rel
        self.width_rel, self.height_rel = width_rel, height_rel
        self.size = size
        self.dir = dir
    def draw(self, screen, width, height):
        x_abs = self.x_rel * width
        y_abs = self.y_rel * height
        width_abs = self.width_rel * width
        height_abs = self.height_rel * height
        x_size, y_size = self.size
        x_size *= width
        y_size *= width

        rect = Rect(x_abs, y_abs, width_abs, height_abs)
        draw.rect(screen, (255,255,255), rect)
        self.image = resource_path(self.dir+r"\ "+self.image)
        self.image = self.image.replace(' ', '')
        image_ = transform.smoothscale(image.load(self.image), (x_size,y_size))
        image_rect = image_.get_rect(center=rect.center)
        screen.blit(image_, image_rect)
        