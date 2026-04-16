import os
from map import Map
from entity import Person, Enemy
class GameInterface:
    def __init__(self, game_map, player, enemies, items):
        self.map = game_map
        self.player = player
        self.enemy = enemies
        self.items = items
        self.log = [] #журнал событий

        self.height = game_map.height
        self.width = game_map.width

    #добавление сообщений на экран
    def add_log(self, message):
        self.log.append(message)
        if len(self.log)>7:
            self.log.pop(0) #удаляем самое старое

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear') #Windows или Mac/Linux


    #функция отрисовки карты
    def draw_map(self):
        map_lines = []
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                row += self.map.dungeon[y][x] #символ из матрицы берём
            map_lines.append(row)
        return map_lines
    
    #события и статус
    def get_right_lines(self):
        lines = []
        lines.append('== СОБЫТИЯ ==')
        for cvc in self.log[-5:]: #на экран выводим только 5 последних 
            if len(cvc) > 25:
                cvc = cvc[:25] + '...'
            lines.append(cvc)

        lines.append('')
        lines.append('== ХАРАКТЕРИСТИКИ ==')
        lines.append(f'hp: {self.player.hp}/{self.player.max_hp}')

        enemy_life = []
        for e in self.enemy:
            if e.hp > 0:
                enemy_life.append(e)
        lines.append(f'врагов: {len(enemy_life)}')

        for i, e in enumerate(enemy_life):
            lines.append(f'враг{i + 1}, hp: {e.hp}')

        lines.append(f'зелий: {len(self.items)}')
        return lines

    def draw(self):
        self.clear_screen()
        map_lines = self.draw_map()
        left_lines = [
            '=== УПРАВЛЕНИЕ ===',
            'w/a/s/d - движение',
            '---- ПРАВИЛА ----',
            '1. убей всех зомби',
            '2. возьми зелье(8)',
            'для лечения',
            '3. с врагом на клетке -',
            'бой',
            '4. пройди 5 уровней,',
            'чтобы победить!',
        ]

        right_lines = self.get_right_lines()

        max_h = max(len(map_lines), len(left_lines), len(right_lines)) #максимальная высота среди колонок

        #делаем одинаковую пустоту
        while len(map_lines)<max_h:
            map_lines.append('')
        while len(left_lines)<max_h:
            left_lines.append('')
        while len(right_lines)<max_h:
            right_lines.append('')

        #делаем рамку
        col_width = 25 
        print('┌' + '─' * (col_width * 3 + 2) + '┐')


        for w in range(0, max_h):
            left = left_lines[w]
            center = map_lines[w]
            right = right_lines[w]
            print(f'|{left:<{col_width}}|{center:<{col_width}}|{right:<{col_width}}|')

        print('└' + '─' * (col_width * 3 + 2) + '┘')


