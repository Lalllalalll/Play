import numpy as np
import random
from entity import Person, Enemy

class Map:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.dungeon = np.full((self.height, self.width), '■') #строка - y, столбец - x
        self.dungeon[1:self.height-1, 1:self.width-1] = '.'
        self.player = None
        self.enemies = []
        self.item = []

    def __str__(self): 
        #должен вернуть СТРОКУ
        rroww = []
        for row in self.dungeon:
            rroww.append(''.join(row))
        return '\n'.join(rroww)

    #функция, которая добавляет персонажа в рандомную позицию
    def add_player(self, object):
        #ДОРАБОТАТь, что, если свободного пространства НЕТ
        self.player = object
        count = 0
        plased = False
        for i in range(100): #100 попыток на создание
            x = random.randint(1, self.width-2) #массивы с 0
            y = random.randint(1, self.height-2)
            if self.dungeon[y, x] == '.':
                self.dungeon[y, x] = object.symbol
                object.x = x
                object.y = y
                plased = True
                break

    #функция, которая добавляет список мобов/предметов в рандомную позицию
    def add_something(self, objects_list):
        #ДОРАБОТАТь, что, если свободного пространства НЕТ
        plased = False
        for object in objects_list[:]: #чтобы можно было убирать элементы, перебираем копию списка, но удаляем из самого списка
            for i in range(100): #100 попыток на создание
                x = random.randint(1, self.width-2) #массивы с 0
                y = random.randint(1, self.height-2)
                if self.dungeon[y, x] == '.':
                    self.dungeon[y, x] = object.symbol
                    object.x = x
                    object.y = y
                    if object.is_enemy:
                        self.enemies.append(object)
                    elif object.is_it:
                        self.item.append(object)
                    else:
                        self.item.append(object)
                    plased = True
                    break

    def add_block(self):
        block = '█'
        self.dungeon[:, 0] = block    # левый край
        self.dungeon[:, -1] = block   # правый край
        self.dungeon[0, :] = '■'    # верхний край
        self.dungeon[-1, :] = '■'   # нижний край


    #функция, которая ставит рандомно блоки в заданном диапозоне
    def random_wall(self):
        for i in range(random.randint(15, 39)):
            wall = '■'
            plased = False
            for i in range(100): #100 попыток на создание
                x = random.randint(1, self.width-2) #массивы с 0
                y = random.randint(1, self.height-2)
                if self.dungeon[y, x] == '.':
                    self.dungeon[y, x] = wall
                    plased = True
                    break

    #функция, которая проверяет границы
    @staticmethod
    def is_valid_move(x, y, MAP):
        if not (0 <= x < MAP.width and 0 <= y < MAP.height):
            return False
        return True

    #удаление координат
    def delection_player(self, obj):
        if obj.is_alive() == False:
            self.dungeon[obj.y, obj.x] = '.'

    #нажимаем на w, a, d, s - движение вверх, вправо, влево, вниз
    def movement_player(self, object, MAP):
        self.player = object
        alw = True
        while alw == True:
            c = input() #w, a, d, s
            object.get_position()
            match c: #object.x, object.y
                case 'w':
                    new_y = self.player.y - 1
                    new_x = self.player.x
                    if self.is_valid_move(new_x, new_y, MAP):
                        if self.dungeon[self.player.y-1, self.player.x] == '.':
                            self.dungeon[self.player.y, self.player.x] = '.'
                            self.player.move(new_x, new_y) #обновляем координаты у игрока
                            self.dungeon[new_y, new_x] = self.player.symbol
                            alw = False

                case 'a':
                    new_y = self.player.y
                    new_x = self.player.x + 1
                    if self.is_valid_move(new_x, new_y):
                        if self.dungeon[self.player.y, self.player.x + 1] == '.':
                            self.dungeon[self.player.y, self.player.x] = '.'
                            self.player.move(new_x, new_y)
                            self.dungeon[new_y, new_x] = self.player.symbol
                            alw = False

                case 'd':
                    new_y = self.player.y
                    new_x = self.player.x - 1
                    if self.is_valid_move(new_x, new_y):
                        if self.dungeon[self.player.y, self.player.x - 1] == '.':
                            self.dungeon[self.player.y, self.player.x] = '.'
                            self.player.move(new_x, new_y)
                            self.dungeon[new_y, new_x] = self.player.symbol
                            alw = False

                case 's':
                    new_y = self.player.y + 1
                    new_x = self.player.x
                    if self.is_valid_move(new_x, new_y):
                        if self.dungeon[self.player.y + 1, self.player.x] == '.':
                            self.dungeon[self.player.y, self.player.x] = '.'
                            self.player.move(new_x, new_y)
                            self.dungeon[new_y, new_x] = self.player.symbol
                            alw = False
                case '':
                    alw = False


    #функция, которая генерирует карту с рандомными width и height
    @classmethod
    def create_map(cls):
        height = random.randint(10, 30)
        width = random.randint(45, 60)
        return cls(height, width)
    

# Логика:
#1)2 уровень. Использование файлов для настроек игры 
#2)условие проигрыша
#3)2 уровень. Поле зрения у врагов
#4)класс ИГРЫ: Пошаговый режим, с возможностью на каждом шаге игроком совершить действие,
#5)функция, которая сравнивает координаты врага и игрока, игрока и зельки. \
#6)Бой в самой карте или как отдельная функция в самой игре? 



