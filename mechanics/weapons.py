import random
from mechanics.effects import effects_set
        
class Weapon:
    def __init__(self) -> None:
        self.effect = None
    
    def __mana_provider__(self, character, comunicat, cost):
        if character.mana >= 0 and character.mana >= cost:
            character.mana -= cost
            comunicat.setText('')
            return True
        else:
            character.round_skip()
            comunicat.setText('Masz za mało many')
            return False        

class Wand(Weapon):
        def __init__(self) -> None:
            self.attack_list = {
                'fire ball (4)': self.fire_ball, 
                'ice block (5)': self.ice_block,
                'thunder storm (2)': self.thunder_storm
                }      
        def fire_ball(self, character, opponent, comunicat):
            if self.__mana_provider__(character, comunicat, 4) == True:
                opponent.health -= 40
            else:
                return False 
        
        def ice_block(self, character, comunicat):
            if self.__mana_provider__(character, comunicat, 5) == True:
                character.health += 80
            else:
                return False  
                
        def thunder_storm(self, character, opponent, comunicat):
            if self.__mana_provider__(character, comunicat, 2) == True:
                opponent.health -= 20
                opponent.effect = effects_set['Burning']
                return opponent.effect
            else:
                return False

class Axe(Weapon):
    def __init__(self) -> None:
        super().__init__()
        self.attack_list = {
            'straight attack (3)': self.straight_attack, 
            'strong attack (6)': self.strong_attack,
            'charge attack (7)': self.charge_attack
            }

    def straight_attack(self, character, opponent, comunicat):
        if self.__mana_provider__(character, comunicat, 3) == True:
            opponent.health -= 30
            if self.effect != None:
                match self.effect:
                    case 'fire':
                        opponent.effect = effects_set['Burning']
        else:
            return False
        
    def strong_attack(self, character, opponent, comunicat):
        if self.__mana_provider__(character, comunicat, 6) == True:
            opponent.health -= 50
            opponent.effect = effects_set['Bleeding']

        else:
            return False
        
    def charge_attack(self, character, opponent, comunicat):
        if self.__mana_provider__(character, comunicat, 7) == True:
            if character.round == False:
                character.round_skip()
                character.round = True
            else:
                if self.effect != None:
                    match self.effect:
                        case 'fire':
                            opponent.effect = effects_set['Burning']
                opponent.health -= 99
                character.round = False
        else:
            return False
        
class Shield(Weapon):
    def __init__(self) -> None:
        self.attack_list = {
            'block (3)': self.block, 
            'heavy block (8)': self.heavy_block, 
            'stunning attack (7)': self.stunning_attack
            }
        
    def block(self, character, comunicat):
        if self.__mana_provider__(character, comunicat, 3) == True:
            character.health += 40
        else:
            return False
        
    def heavy_block(self, character, comunicat):
        if self.__mana_provider__(character, comunicat, 8) == True:
            character.health += 100
        else:
            return False
        
    def stunning_attack(self, character, opponent, comunicat):
        if self.__mana_provider__(character, comunicat, 7) == True:
            opponent.health -= 30
        else:
            return False

class RunicBook(Weapon):
    def __init__(self) -> None:
        self.attack_list = {
            'summon totem (3)': self.summon_totem,
            'write rune (5)': self.write_rune,
            'summon thunder (10)': self.summon_thunder,
        }
        
    def summon_totem(self, character, opponent, comunicat):
        if self.__mana_provider__(character, comunicat, 3) == True:
            random_number = random.randint(0, 4)
            
            match random_number:
                case 0:
                    character.health += 20
                case 1:
                    opponent.health -= 20
                case 2:
                    character.mana += 3
                case 3:
                    character.food += 20
                    character.water += 20
                case 4:
                    character.health -= 10
                    opponent.health -= 10
        else:
            return False
                
    def write_rune(self, character, opponent, comunicat):
        if self.__mana_provider__(character, comunicat, 5) == True:
            random_number = random.randint(0, 2)
            
            match random_number:
                case 0:
                    opponent.effect = effects_set['Poison']
                case 1:
                    character.effect = effects_set['Nurrish']
                case 2:
                    character.effect = effects_set['Burning']
                    opponent.effect = effects_set['Burning']
        else:
            return False
            
    def summon_thunder(self, character, opponent, comunicat):
        if self.__mana_provider__(character, comunicat, 10) == True:
            random_number = random.randint(0, 80) + 20
            
            opponent.health -= random_number

wand = Wand()
axe = Axe()
shield = Shield()
runic_book = RunicBook()

weapons_set = {
    'Wand': wand, 
    'Axe': axe,
    'Shield': shield,
    'Runic Book': runic_book,
}
