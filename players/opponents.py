from players.characters import Character
from mechanics.effects import effects_set

class Dragon(Character):
    def __init__(self, name: str, health: int = 100, loot: dict = ...) -> None:
        super().__init__(name, health, loot)
        
    def __mana_dragon_provider__(self, character, comunicat, cost):
        if character.mana >= 0 and character.mana >= cost:
            character.mana -= cost
            comunicat.setText('')
            return True
        else:
            character.round_skip()
            comunicat.setText('Masz za mało many')
            return False
    
    def __init__(self, name: str, type: str, health: int = 100, loot: dict = {}) -> None:
        super().__init__(name, health, loot)
        self.type = type
        
    def equipment(self):
        self.role = 'Dragon'
        self.base_set()
    
    def fire_breath(self, opponent: Character, comunicat):
        if self.__mana_dragon_provider__(self, comunicat, 5) == True:
            opponent.health -= 50
            opponent.effect = effects_set['Dragon Burning']
        else:
            print('Masz za mało many')
    
    def sky_attack(self, opponent: Character, comunicat):
        if self.__mana_dragon_provider__(self, comunicat, 2) == True:
            opponent.health -= 20
            self.mana += 2
        else:
            print('Masz za mało many')
            
    def mana_from_the_sky(self):
        self.mana += 12
            
    def lava_breath(self, opponent: Character, comunicat):
        if self.__mana_dragon_provider__(self, comunicat, 10) == True:
            opponent.health -= 100
            
            if self.mana > 10:
                self.mana -= 4
            else:
                self.mana = 0
        else:
            print('Masz za mało many') 
            
    def toxic_breath(self, opponent: Character):
        if self.__mana_dragon_provider__(self, 4) == True:
            opponent.health -= 60
            opponent.effect = effects_set['Poison']
        else:
            print('Masz za mało many')
            
    def toxic_shock(self, opponent: Character):
        if self.__mana_dragon_provider__(self, 2) == True:
            opponent.effect = effects_set['Dragon Toxin']
        else:
            print('Masz za mało many')
            
    def toxic_wave(self, opponent: Character):
        if self.__mana_dragon_provider__(self, 8):
            opponent.health -= 80
        else:
            print('Masz za mało many')
    
    def voice_of_swamp(self):
        if self.__mana_dragon_provider__(self, 4):
            self.health += 60
            
    def swamp_monster(self, opponent: Character):
        if self.__mana_dragon_provider__(self, 8):
            opponent.health -= 80
            opponent.effect = effects_set['Poison']
            
    def swamp_breath(self, opponent: Character):
        if self.__mana_dragon_provider__(self, 4):
            opponent.health -= 40
            self.health += 40