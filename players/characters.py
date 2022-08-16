from mechanics.foods import food, drink 
from mechanics.weapons import weapons_set

class Character:
    def __init__(self, name: str, health: int = 100, loot: dict = {}) -> None:
        self.name = name
        self.lvl = 0
        self.health = health
        self.dead = False
        self.mana = 10
        self.effect = None     
        self.eq = {}
        self.loot = loot
        self.my_round = 'my'
        self.money = 0

    def eat(self, food):
        self.health += food.value
    
    def drink(self, drink):
        self.effect.time -= drink.value
        
    def round_skip(self):
        if self.mana <= 10:
            self.mana += 10
        else:
            self.mana = 20
        
    def introduce_yourself(self):
        return 'Nazywam się ' + self.name

    def __mana_provider__(self, character, cost):
        if character.mana >= 0 and character.mana >= cost:
            character.mana -= cost
            return True
        else:
            character.round_skip()
            print('Pominięto turę')
            return False 
    
    def base_set(self):
        for i in food.keys():
            self.eq[i] = food[i]
            
        for i in drink.keys():
            self.eq[i] = drink[i]
        
    
class Mage(Character): 
        def equipment(self):
            self.role = 'Mage'
            self.eq = {
            'Wand': weapons_set['Wand'],
            }
            self.base_set()
            
class Warrior(Character):
        def equipment(self) -> None:
            self.role = 'Warrior'
            self.round = False
            self.eq = {
                'Shield': weapons_set['Shield'],
                'Axe': weapons_set['Axe'],
            }
            self.base_set()

class Shaman(Character):
    def equipment(self) -> None:
        self.role = 'Shaman'
        self.eq = {
            'Runic Book': weapons_set['Runic Book'],
        }
        self.base_set()