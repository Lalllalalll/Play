import random

class Entity:
    def __init__(self, symbol, max_hp, attack_damage, x=1, y=1):
        self.symbol = symbol  # символ для отображения
        self.max_hp = max_hp  # максимальное HP
        self.hp = max_hp  # текущее HP (начинаем с максимума)
        self.attack_damage = attack_damage  # сила атаки
        self.x = x  # позиция по X
        self.y = y  # позиция по Y
        self.alive = True  # жив ли персонаж
        self.is_enemy = False #проверка на зомби

    def __str__(self):
        return f"{self.symbol} HP:{self.hp}/{self.max_hp} ATK:{self.attack_damage}"

    def __eq__(self, other):
        if not isinstance(other, type(self)): #сравниваем КЛАССЫ
            return False
        return self.symbol == other.symbol and self.x == other.x and self.y == other.y
    
    #передам новые координаты
    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    #получение урона
    def take_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    #атака
    def attack(self, target):
        if self == target:
            return False  #Нельзя атаковать себя!"

        damage = self.attack_damage #сила атаки
        target.take_damage(damage)

    #проверка на то, жив ли 
    def is_alive(self):
        return self.alive
    
    #Расстояние до другого персонажа
    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    #текущая позиция
    def get_position(self):
        return (self.x, self.y)


class Person(Entity):
    def __init__(self, x = 1, y = 1):
        # Игрок: символ '@', 100 HP, 5 урона
        super().__init__('@', max_hp = 60, attack_damage = 5, x=x, y=y)
        self.is_enemy = False
    
    #лечение
    def heal(self, amount = 10):
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    #Улучшение характеристик 
    def upgrade_stats(self, hp_increase=0, damage_increase=0):
        if hp_increase > 0: 
            self.max_hp += hp_increase
            self.hp += hp_increase  # также восстанавливаем здоровье

        if damage_increase > 0:
            self.attack_damage += damage_increase
    


class Enemy(Entity):
    def __init__(self, x=1, y=1):
        # Враг: символ 'Z', 50 HP, 3 урона
        health = random.randint(20, 40)
        super().__init__('Z', health, attack_damage = 5, x=x, y=y)
        self.is_enemy = True

    #Движение в сторону игрока
    def move_towards_player(self, person, MAP):
        if self.distance_to(person) <= 2:
            return False
        
        if self.distance_to(person) > 5:
            return False
        
        # Сначала пытаемся двигаться по горизонтали
        if self.x < person.x:
            # Игрок справа - двигаемся вправо
            new_x = self.x + 1
            new_y = self.y
        elif self.x > person.x:
            # Игрок слева - двигаемся влево
            new_x = self.x - 1
            new_y = self.y
        else:
            # По горизонтали уже на одной линии
            new_x = self.x
            new_y = self.y

            # Пытаемся двигаться по вертикали
            if self.y < person.y:
                new_y = self.y + 1
            elif self.y > person.y:
                new_y = self.y - 1

        # Проверяем, можно ли пройти в выбранную клетку
        if 0 <= new_x < MAP.width and 0 <= new_y < MAP.height:
            if MAP.dungeon[new_y, new_x] != '█' and \
                MAP.dungeon[new_y, new_x] != '■':
                MAP.dungeon[self.y, self.x] = '.'
                self.move(new_x, new_y)
                MAP.dungeon[ new_y, new_x] = self.symbol
                return True

        # Если не получилось, пробуем другое направление
        # Пробуем вертикальное движение
        if self.y < person.y:
            new_x = self.x
            new_y = self.y + 1
        elif self.y > person.y:
            new_x = self.x
            new_y = self.y - 1
        else:
            # Пробуем горизонтальное движение (если вертикаль не подошла)
            if self.x < person.x:
                new_x = self.x + 1
                new_y = self.y
            elif self.x > person.x:
                new_x = self.x - 1
                new_y = self.y
            else:
                return False  # Не можем двигаться

        #Проверяем второе направление
        if 0 <= new_x < MAP.width and 0 <= new_y < MAP.height:
            if MAP.dungeon[new_y, new_x] != '█' and \
                MAP.dungeon[new_y, new_x] != '■':
                MAP.dungeon[self.y, self.x] = '.'
                self.move(new_x, new_y)
                MAP.dungeon[ new_y, new_x] = self.symbol
                return True
