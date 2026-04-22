import numpy as np
import random
from entity import Person, Enemy
import msvcrt

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
        self.player = object
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
        for object in objects_list:
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
                    plased = True
                    break

    def add_block(self):
        block = '█'
        self.dungeon[0, 0] = block    # левый край
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

    #возращает нажатую клавишу или ничего БЕЗ enter
    @staticmethod
    def get_key():
        if msvcrt.kbhit(): #True, если клавиша нажата
            key = msvcrt.getch().decode('utf-8') #getch() возвращает байты символа, превращаем их в строку
            #utf-8 - таблица, содержащяя все символы и их байты
            return key
        return None

    #нажимаем на w, a, d, s - движение вверх, вправо, влево, вниз
    def movement_player(self, object, MAP):
        self.player = object
        alw = True
        while alw == True:
            if not self.player.is_alive():
                return
            
            c = self.get_key() #w, a, d, s

            if c == None:
                continue

            old_y = self.player.y
            old_x = self.player.x


            match c: #object.x, object.y
                case 'w':
                    new_y = self.player.y - 1
                    new_x = self.player.x

                case 'a':
                    new_x = self.player.x - 1
                    new_y = self.player.y

                case 'd':
                    new_x = self.player.x + 1
                    new_y = self.player.y

                case 's':
                    new_y = self.player.y + 1
                    new_x = self.player.x

                case '':
                    alw = False
                
            if self.is_valid_move(new_x, new_y, MAP):
                if self.dungeon[new_y, new_x] != '█' and self.dungeon[new_y, new_x] != '■':
                    if self.dungeon[new_y, new_x] != 'Z':
                        self.dungeon[old_y, old_x] = '.'
                        self.player.move(new_x, new_y) #обновляем координаты у игрока
                        self.dungeon[new_y, new_x] = self.player.symbol
                        alw = False
                    else:
                        self.dungeon[old_y, old_x] = '.'
                        self.player.move(new_x, new_y) #обновляем координаты у игрока
                        self.dungeon[new_y, new_x] = '┼'
                        alw = False

    #функция, которая генерирует карту с рандомными width и height
    @classmethod
    def create_map(cls):
        height = random.randint(15, 25)
        width = random.randint(30, 40)
        return cls(height, width)
    

# Логика:
#1)2 уровень. Использование файлов для настроек игры 
#2)условие проигрыша
#3)2 уровень. Поле зрения у врагов
#4)класс ИГРЫ: Пошаговый режим, с возможностью на каждом шаге игроком совершить действие,
#5)функция, которая сравнивает координаты врага и игрока, игрока и зельки. \
#6)Бой в самой карте или как отдельная функция в самой игре? 



