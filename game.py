from map import Map
from items import HealthIt
from entity import Person, Enemy
from intercface import GameInterface
import random
class Game:

    def __init__(self):
        self.level = 1
        self.running = True

    #создание списка мобов
    @staticmethod
    def generation_obj(obj, count, MAP):
        lst_obj = []
        for i in range(count):
            x = random.randint(1, MAP.width - 2)
            y = random.randint(1, MAP.height - 2)
            lst_obj.append(obj(x, y))
        return lst_obj

    #бой персонажа и зомби
    def battle_p_e(self, player, enemy_l, map, interface):
        for enem in enemy_l[:]:
            if enem.x == player.x and enem.y == player.y:
                enem.attack(player)
                player.attack(enem)
                if enem.is_alive() == False:
                    map.delection_player(enem)
                    enemy_l.remove(enem)
                    interface.add_log("Зомби погиб!")
                    player.upgrade_stats(10, 5) #улучшаем характеристики
                if player.is_alive() == False:
                    map.delection_player(player)
                    interface.add_log("СТОП ИГРА. Вы погибли!")
                    

    #движение списка мобов
    def movement_mob(self, enemy_l, player, map):
        if player == None:
            return
        for enemy in enemy_l:
            old_x = enemy.x
            old_y = enemy.y
            moved = enemy.move_towards_player(player, map) #вернёт True или False
            if not moved:
                for _ in range(10): #10 попыток
                    new_x = random.randint(enemy.x-1, enemy.x+1)
                    new_y = random.randint(enemy.y-1, enemy.y+1)
                    if map.dungeon[new_y, new_x] != '■' and map.dungeon[new_y, new_x] != '█':
                        map.dungeon[old_y, old_x] = '.'
                        enemy.move(new_x, new_y)
                        map.dungeon[new_y, new_x] = enemy.symbol
                        break

            
    #функция поглощения зелья
    def eat_z(self, item_l, player, map):
        for it in item_l[:]: 
            if it.x == player.x and it.y == player.y:
                player.heal(amount = 10)
                # map.dungeon[it.y, it.x] = '.'
                item_l.remove(it)

    #игра
    def run(self):

        while self.level <= 5 and self.running: #если True

            #создаём карту
            MAP = Map.create_map()
            MAP.add_block()
            MAP.random_wall()

            #создаём персонажа
            p = Person(14, 5)
            MAP.add_player(p)

            #создаём мобов
            mobs = Game.generation_obj(Enemy, 5, MAP)
            MAP.add_something(mobs)

            #создаём зелья
            items = Game.generation_obj(HealthIt, 2, MAP)
            MAP.add_something(items)

            #создаём интерфейс
            ui = GameInterface(MAP, p, mobs, items)
            ui.add_log(f'НАЧАЛСЯ УРОВЕНЬ {self.level}')

            #сама игра
            while p.is_alive():
                ui.draw()

                MAP.movement_player(p, MAP) #движение игрока, потом мобов
                self.movement_mob(mobs, p, MAP)

                self.battle_p_e(p, mobs, MAP, ui) #бой

                self.eat_z(items, p, MAP) #собираем зелья

                #проверка победы на уровень
                if len(mobs) <= 0:
                    ui.add_log(f'Вы прошли 1 уровень.')
                    self.level += 1
                    break

                # Проверка ПОБЕДЫ вообще
                if not p.is_alive():
                    ui.add_log("ВЫ ПОГИБЛИ")
                    choice = input("Начать уровень заново? (y/n): ")
                    if choice.lower() == 'y':
                        self.level = 1
                        continue  # ← перезапускаем уровень
                    else:
                        break  # выходим из игры

        if self.level >= 5:
           print('ВЫ ВЫИГРАЛИ! КРУТЫЕ!')
try:
    game = Game()
    game.run()
except Exception as e: #работает с любыми ошибками
    print(f'Произошла ошибка: {e}')

# Ошибки:
# 1)Персонаж и зомби сливаются в одно
# 2)Подредактировать цикл, чтобы хп и навыки оставались одними и теми же

# Карта:
# 1)#функция, которая добавляет персонажа в рандомную позицию
#     def add_player(self, object):
# 2)#функция, которая добавляет список мобов/предметов в рандомную позицию
#     def add_something(self, objects_list):
# 3)#функция, которая проверяет границы
#     @classmethod
#     def is_valid_move(cls, x, y):
# 4)#удаление координат
#     def delection_player(self, obj):
# 5)#нажимаем на w, a, d, s - движение вверх, вправо, влево, вниз
#     def movement_player(self, object):
# 6)#функция, которая генерирует карту с рандомными width и height
#     @classmethod
#     def create_map(cls):
    
# Общая:
# 1)#передам новые координаты
#     def move(self, new_x, new_y)
# 2)#получение урона
#     def take_damage(self, damage):
# 3)#атака
#     def attack(self, target):
# 4)#проверка на то, жив ли 
#     def is_alive(self):

# Персонаж:
# 1)#Улучшение характеристик 
#     def upgrade_stats(self, hp_increase=0, damage_increase=0):

# Зомби:
# 1)#Движение в сторону игрока
#     def move_towards_player(self, person, MAP):

# Интерфейс:
# 1)#добавление сообщений на экран
#     def add_log(self, message):
# 2)def clear_screen(self):
# 3)#функция отрисовки карты
#     def draw_map(self):
# 4)#полный интерфейс
# def draw(self):

            



# Логика:
# 1)Экран замирает после или перед каждого хода игрока
# 2)Ловить ошибки, чтобы игра не останавливалась
# 3)Добавление карты, персонажей и зелей, ПОТОМ интерфейс. Враги двигаются только тогда, когда двигается сам персонаж
# # !4)Реализовать бой между игроком и персонажем 
# 2)Условие проигрыша и победы в игре
# 3)Ход самой игры