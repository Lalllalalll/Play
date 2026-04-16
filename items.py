class HealthIt:
    def __init__(self, x, y, heal_amount=20):
        self.x = x
        self.y = y
        self.symbol = '&'
        self.heal_amount = heal_amount
        self.is_it = True
        self.is_enemy = False