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
        self.is_enemy = False

    def __str__(self):
        return f"{self.symbol} HP:{self.hp}/{self.max_hp} ATK:{self.attack_damage}"

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        return self.name == other.name and self.x == other.x and self.y == other.y
    
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
            return True  # персонаж умер

        return False  # персонаж выжил
    
    #атака и врага, и персонажа
    def attack(self, target):
        if self == target:
            return False, "Нельзя атаковать себя!"

        damage = self.attack_damage #сила атаки
        target_died = target.take_damage(damage)

        message = f"{self.symbol} атакует {target.symbol} и наносит {damage} урона!"

        if target_died:
            message += f" {target.symbol} убит!"

        return target_died, message
    
    #проверка на то, жив ли 
    def is_alive(self):
        return self.alive
    
    #текущая позиция
    def get_position(self):
        return (self.x, self.y)
    
    #Расстояние до другого персонажа
    def distance_to(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class Person(Entity):
    def __init__(self, x = 1, y = 1):
        # Игрок: символ '@', 100 HP, 5 урона
        super().__init__('@', max_hp = 100, attack_damage = 5, x=x, y=y)
        self.is_enemy = True

    def __str__(self):
        return f"Player {self.symbol} HP:{self.hp}/{self.max_hp} ATK:{self.attack_damage}"
    
    #лечение
    def heal(self, amount = 20):
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
        super().__init__('Z', max_hp = 50, attack_damage = 3, x=x, y=y)

    #Движение в сторону игрока
    def move_towards_player(self, player_x, player_y, MAP):

        # Сначала пытаемся двигаться по горизонтали
        if self.x < player_x:
            # Игрок справа - двигаемся вправо
            new_x = self.x + 1
            new_y = self.y
        elif self.x > player_x:
            # Игрок слева - двигаемся влево
            new_x = self.x - 1
            new_y = self.y
        else:
            # По горизонтали уже на одной линии
            new_x = self.x
            new_y = self.y

            # Пытаемся двигаться по вертикали
            if self.y < player_y:
                new_y = self.y + 1
            elif self.y > player_y:
                new_y = self.y - 1

        # Проверяем, можно ли пройти в выбранную клетку
        if 0 <= new_x < MAP.width and 0 <= new_y < MAP.height:
            if MAP.dungeon[new_y][new_x] = '.':
                self.move(new_x, new_y)
                return True

        # Если не получилось, пробуем другое направление
        # Пробуем вертикальное движение
        if self.y < player_y:
            new_x = self.x
            new_y = self.y + 1
        elif self.y > player_y:
            new_x = self.x
            new_y = self.y - 1
        else:
            # Пробуем горизонтальное движение (если вертикаль не подошла)
            if self.x < player_x:
                new_x = self.x + 1
                new_y = self.y
            elif self.x > player_x:
                new_x = self.x - 1
                new_y = self.y
            else:
                return False  # Не можем двигаться

        # Проверяем второе направление
        if 0 <= new_x < MAP.width and 0 <= new_y < MAP.height:
            if MAP.tiles[new_y][new_x].walkable:
                self.move(new_x, new_y)
                return True

        return False  # Никуда не можем двинуться

    def __str__(self):
        return f"Enemy {self.symbol} HP:{self.hp}/{self.max_hp} ATK:{self.attack_damage}"

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
