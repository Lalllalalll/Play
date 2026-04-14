import numpy as np
import random
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
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
                self.dungeon[y, x] = object.char
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
                    self.dungeon[y, x] = object.char
                    object.x = x
                    object.y = y
                    self.enemies.append(object)
                    plased = True
                    break

    def add_block(self):
        block = '█'
        self.dungeon[:, 0:1] = block
        self.dungeon[:, self.width-1:self.width] = block
        self.dungeon[0, self.width-1:self.width] = '■'
        self.dungeon[0, 0] = '■'
        self.dungeon[self.height-1:self.height, 0] = '■'
        self.dungeon[self.height-1:self.height, self.width-1:self.width] = '■'


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
    def is_valid_move(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return True
    
    #движение списка мобов
    #удаление мёртвых игроков
    #загрузить на гитхаб
    #2 уровень. Использование файлов для настроек игры 
    #условие проигрыша
    #2 уровень. Поле зрения у врагов
    #класс ИГРЫ: Пошаговый режим, с возможностью на каждом шаге игроком совершить действие,
    #воплотить саму игру или класс игры???
    #функция, которая сравнивает координаты врага и игрока, игрока и зельки. \
    # зелька убирается, мобы стираются с карты. Бой в самой карте или как отдельная функция в самой игре? (Алина - игра)

    #нажимаем на w, a, d, s - движение вверх, вправо, влево, вниз
    def movement_player(self, object):
        self.player = object
        alw = True
        while alw == True:
            c = input() #w, a, d, s
            object.get_position()
            match c: #object.x, object.y
                case 'w':
                    new_y = self.player.y - 1
                    new_x = self.player.x
                    if self.is_valid_move(new_x, new_y):
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
    def create_map(self):
        width = random.randint(10, 30)
        height = random.randint(45, 60)
        return Map(height, width)


class Entity:
    def __init__(self, name, char, health, y, x):
        self.name = name
        self.char = char
        self.health = health
        self.y = y
        self.x = x

    def __str__(self):
        return self.char
    

class Person(Entity):
    def __init__(self, y, x):
        super().__init__('Игрок', '@', 100, y, x)

class Mob(Entity):
    def __init__(self, y, x, health = 50):
        super().__init__('Зомби', 'Z', health, y, x)

    #функция, которая создаёт монстров в фиксированном значении
    @classmethod
    def generation_mobs(cls, count, MAP):
        lst_mob = []
        for i in range(count):
            cls.health = random.randint(10, 50)
            x = random.randint(1, MAP.width - 2)
            y = random.randint(1, MAP.height - 2)
            lst_mob.append(cls(cls.health, y, x))
        return lst_mob

# class Player:
#     def __init__(self, symbol, max_hp, attack_damage, x=1, y=1):
#         """Конструктор персонажа
#         Args:
#             symbol: символ отображения ('@', 'G', 'O' и т.д.)
#             max_hp: максимальное здоровье
#             attack_damage: сила атаки
#             x: координата X на карте
#             y: координата Y на карте"""
#         self.symbol = symbol  # символ для отображения
#         self.max_hp = max_hp  # максимальное HP
#         self.hp = max_hp  # текущее HP (начинаем с максимума)
#         self.attack_damage = attack_damage  # сила атаки
#         self.x = x  # позиция по X
#         self.y = y  # позиция по Y
#         self.alive = True  # жив ли персонаж

#     def __str__(self):
#         """Строковое представление для вывода"""
#         return f"{self.symbol} HP:{self.hp}/{self.max_hp} ATK:{self.attack_damage}"

#     def __repr__(self):
#         """Короткое представление для отладки"""
#         return self.symbol

#     def move(self, new_x, new_y):
#         """Перемещение персонажа на новые координаты
#         Args:
#             new_x: новая координата X
#             new_y: новая координата Y"""
#         self.x = new_x
#         self.y = new_y

#     def take_damage(self, damage):
#         """Получение урона
#         Args:
#             damage: количество урона
#         Returns:
#             bool: True если персонаж умер, False если выжил"""
#         self.hp -= damage

#         if self.hp <= 0:
#             self.hp = 0
#             self.alive = False
#             return True  # персонаж умер

#         return False  # персонаж выжил

#     def attack(self, target):
#         """Функция и врага, и персонажа
#         Args:
#             target: цель атаки (другой объект Person)
#         Returns:
#             tuple: (target_died, message)
#             target_died: bool - умерла ли цель
#             message: str - описание атаки"""
#         # Нельзя атаковать себя
#         if self == target:
#             return False, "Нельзя атаковать себя!"

#         # Наносим урон цели
#         damage = self.attack_damage #сила атаки
#         target_died = target.take_damage(damage)

#         # Формируем сообщение
#         message = f"{self.symbol} атакует {target.symbol} и наносит {damage} урона!"

#         if target_died:
#             message += f" {target.symbol} убит!"

#         return target_died, message

#     def heal(self, amount):
#         """Лечение персонажа
#         Args:
#             amount: количество здоровья для восстановления
#         Returns:
#             int: сколько здоровья реально восстановлено"""
#         old_hp = self.hp
#         self.hp = min(self.max_hp, self.hp + amount)
#         return self.hp - old_hp

#     def upgrade_stats(self, hp_increase=0, damage_increase=0):
#         """Улучшение характеристик (после убийства врага)
#         Args:
#             hp_increase: увеличение максимального здоровья
#             damage_increase: увеличение силы атаки"""
#         if hp_increase > 0: 
#             self.max_hp += hp_increase
#             self.hp += hp_increase  # также восстанавливаем здоровье

#         if damage_increase > 0:
#             self.attack_damage += damage_increase

#     def is_alive(self):
#         """Проверка, жив ли персонаж"""
#         return self.alive

#     def get_position(self):
#         """Получить текущую позицию"""
#         return (self.x, self.y)

#     def distance_to(self, other):
#         """Расстояние до другого персонажа (Манхэттенское)"""
#         return abs(self.x - other.x) + abs(self.y - other.y)


# class Person(Player):
#     """Класс игрока (без системы опыта)"""
#     def __init__(self, x = 1, y = 1):
#         # Игрок: символ '@', 100 HP, 5 урона
#         super().__init__('@', max_hp = 100, attack_damage = 5, x=x, y=y)

#     def __str__(self):
#         """Отображение игрока"""
#         return f"Player {self.symbol} HP:{self.hp}/{self.max_hp} ATK:{self.attack_damage}"


# class Enemy(Player):
#     """Класс врага"""
#     def __init__(self, x=1, y=1):
#         # Враг: символ 'Z', 50 HP, 3 урона
#         super().__init__('Z', max_hp = 50, attack_damage = 3, x=x, y=y)

#     def move_towards_player(self, player_x, player_y, MAP):
#         """Движение в сторону игрока
#         Args:
#             player_x: X координата игрока
#             player_y: Y координата игрока
#             MAP: объект карты для проверки проходимости
#         Returns:
#             bool: удалось ли сдвинуться"""

#         # Сначала пытаемся двигаться по горизонтали
#         if self.x < player_x:
#             # Игрок справа - двигаемся вправо
#             new_x = self.x + 1
#             new_y = self.y
#         elif self.x > player_x:
#             # Игрок слева - двигаемся влево
#             new_x = self.x - 1
#             new_y = self.y
#         else:
#             # По горизонтали уже на одной линии
#             new_x = self.x
#             new_y = self.y

#             # Пытаемся двигаться по вертикали
#             if self.y < player_y:
#                 new_y = self.y + 1
#             elif self.y > player_y:
#                 new_y = self.y - 1

#         # Проверяем, можно ли пройти в выбранную клетку
#         if 0 <= new_x < MAP.width and 0 <= new_y < MAP.height:
#             if MAP.tiles[new_y][new_x].walkable:
#                 self.move(new_x, new_y)
#                 return True

#         # Если не получилось, пробуем другое направление
#         # Пробуем вертикальное движение
#         if self.y < player_y:
#             new_x = self.x
#             new_y = self.y + 1
#         elif self.y > player_y:
#             new_x = self.x
#             new_y = self.y - 1
#         else:
#             # Пробуем горизонтальное движение (если вертикаль не подошла)
#             if self.x < player_x:
#                 new_x = self.x + 1
#                 new_y = self.y
#             elif self.x > player_x:
#                 new_x = self.x - 1
#                 new_y = self.y
#             else:
#                 return False  # Не можем двигаться

#         # Проверяем второе направление
#         if 0 <= new_x < MAP.width and 0 <= new_y < MAP.height:
#             if MAP.tiles[new_y][new_x].walkable:
#                 self.move(new_x, new_y)
#                 return True

#         return False  # Никуда не можем двинуться

#     def __str__(self):
#         """Отображение врага"""
#         return f"Enemy {self.symbol} HP:{self.hp}/{self.max_hp} ATK:{self.attack_damage}"

    #функция, которая создаёт монстров в фиксированном значении
    @classmethod
    def generation_mobs(cls, count, MAP):
        lst_mob = []
        for i in range(count):
            cls.health = random.randint(10, 50)
            x = random.randint(1, MAP.width - 2)
            y = random.randint(1, MAP.height - 2)
            lst_mob.append(cls(cls.health, y, x))
        return lst_mob

# нужно 5 мобов
p = Person(14, 15)
m = Map(45, 11)
mobs = Mob.generation_mobs(15, m)
m.add_player(p) 
m.add_something(mobs) 
m.add_block()
m.random_wall()
print(m)  
#Функция самой игры:
# вызать карту, отобразить всё на карте, передвижение игрока, убийство зомби, как убили - появляется дверь и игрок проходит в другую комнату(что со старой?)