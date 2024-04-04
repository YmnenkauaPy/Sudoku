from pygame import *
from funcs import resource_path, draw_border, get_sizes

#Шаблон Фабрика
class ManagerButton():
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

    def manage(self, status, button, size):
        if status == 'button':
            button = Button(button)
            button.draw(self.screen, self.width, self.height)

        if status == 'random':
            button = RandomButton(button)
            button.draw(self.screen, self.width, self.height)
        
        if status == 'image':
            image = button[0]
            button.remove(button[0])
            dir = button[0]
            button.remove(button[0])
            button = ImageButton(image, dir, button)
            button.draw(self.screen, self.width, self.height, size)

class Button():
    def __init__(self, args):
        self._text, self.x_rel, self.y_rel, self.width_rel, self.height_rel, self.font, self.color = args

    def draw(self, screen, width, height):
        # Вычисляем абсолютные координаты и размеры на основе текущего размера экрана
        x_abs, y_abs, width_abs, height_abs = get_sizes(self.x_rel, self.y_rel, self.width_rel, self.height_rel, width, height)
        rect = Rect(x_abs, y_abs, width_abs, height_abs)
        draw.rect(screen, (255,255,255), rect)

        text_surface = self.font.render(self._text, True, self.color)
        text_rect = text_surface.get_rect(center = rect.center)

        draw_border(screen, x_abs, y_abs, width_abs, height_abs)

        screen.blit(text_surface, text_rect)


class RandomButton(Button):
    def draw(self, screen, width, height):
        x_abs, y_abs, width_abs, height_abs = get_sizes(self.x_rel, self.y_rel, self.width_rel, self.height_rel, width, height)
        
        rect = Rect(x_abs, y_abs, width_abs, height_abs)
        draw.rect(screen, (255,255,255), rect)
        
        draw_border(screen, x_abs, y_abs, width_abs, height_abs)
        
        color_index = 0
        n = 0
        for char in self._text:
            color_ = self.color[color_index % len(self.color)]
            text_surface = self.font.render(char, True, color_)
            text_rect = text_surface.get_rect(center = rect.center)
            text_rect[0] -= 50
            screen.blit(text_surface, (text_rect[0]+n, text_rect[1]))
            n += 20
            color_index += 1


class ImageButton(Button):
    def __init__(self, image, dir, *args):
        super().__init__(*args)
        self.image = image
        self.dir = dir

    def draw(self, screen, width, height, size):
        # Вычисляем абсолютные координаты и размеры на основе текущего размера экрана
        x_size, y_size = size
        x_abs, y_abs, width_abs, height_abs = get_sizes(self.x_rel, self.y_rel, self.width_rel, self.height_rel, width, height)
        self.image = resource_path(self.dir+r"\ "+self.image)
        self.image = self.image.replace(' ', '')
        image_ = transform.smoothscale(image.load(resource_path(self.image)), (x_size*height, y_size*height))
        rect = Rect(x_abs, y_abs, width_abs, height_abs)
        draw.rect(screen, (255,255,255), rect)
        
        text_surface = self.font.render(self._text, True, self.color)
        text_rect = text_surface.get_rect(midleft=rect.midleft)

        draw_border(screen, x_abs, y_abs, width_abs, height_abs)

        text_rect[0] += 5
        screen.blit(text_surface, text_rect)
        text_rect[0] += 170
        text_rect[1] += 12
        screen.blit(image_, text_rect)

########################################################
#Шаблон Фабрика
class ManagerClasses():
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
    
    def manage(self, status, text):
        if status == 'coins':
            text = Coins(text)
            text.draw(self.screen, self.width, self.height)
        
        if status == 'text':
            text = Text(text)
            text.draw(self.screen, self.width, self.height)
        
        if status == 'image':
            text = Image(text)
            text.draw(self.screen, self.width, self.height)

class Coins():
    def __init__(self, args):
        self.text, self.text2, self.font_path, self.x_rel, self.y_rel, self.width_rel, self.height_rel = args
        self.font2 = font.Font(self.font_path, 25)
        self.font = font.Font(self.font_path, 30)
        
    def draw(self, screen, width, height):
        x_abs, y_abs, width_abs, height_abs = get_sizes(self.x_rel, self.y_rel, self.width_rel, self.height_rel, width, height)
            
        rect = Rect(x_abs, y_abs, width_abs, height_abs)
        draw.rect(screen, (255,255,255), rect)
        text_surface = self.font.render(self.text, True, (200,200,0))
        text_surface2 = self.font2.render(self.text2, True, (0,0,0))
        text_rect = text_surface2.get_rect(center=rect.center)

        draw_border(screen, x_abs, y_abs, width_abs, height_abs)

        text_rect[0]-=20
        text_rect[1]-=8
        screen.blit(text_surface, text_rect)
        text_rect[1]+=8
        text_rect[0]+=20
        screen.blit(text_surface2, text_rect)

class Text():
    def __init__(self, args):
        self.text, self.font_path, self.size_font, self.size_outline, self.x_rel, self.y_rel, self.width_rel, self.height_rel, self.color = args
        self.font = font.Font(self.font_path, self.size_font)

    def draw(self, screen, width, height):
        x_abs, y_abs, width_abs, height_abs = get_sizes(self.x_rel, self.y_rel, self.width_rel, self.height_rel, width, height)
            
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
    def __init__(self, args):
        self.image, self.x_rel, self.y_rel, self.size, self.width_rel, self.height_rel, self.dir = args
        
    def draw(self, screen, width, height):
        x_abs, y_abs, width_abs, height_abs = get_sizes(self.x_rel, self.y_rel, self.width_rel, self.height_rel, width, height)

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
