class Effect:
    def __init__(self, name: str) -> None:
        self.name = name

class Poison(Effect):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.time = 1
        
    def effect(self, opponent):
        opponent.health -= 30
        
class Bleeding(Effect):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.time = 5
    
    def effect(self, opponent):
        opponent.health -= 10

class Burning(Effect):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.time = 1
    
    def effect(self, opponent):
        opponent.health -= 40

class DragonBurning(Effect):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.time = 3
    
    def effect(self, opponent):
        opponent.health -= 40
        
class DragonToxin(Effect):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.time = 1
        
    def effect(self, opponent):
        opponent.health -= 50

class Nurrish(Effect):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.time = 3
        
    def effect(self, character):
        character.mana += 3

poison = Poison('poison')
bleeding = Bleeding('bleeding')
burning = Burning('burning')
nurrish = Nurrish('nurrish')
dragon_burning = DragonBurning('dragon burning')
dragon_toxin = DragonToxin('dragon_toxin')

effects_set = {
        'Poison': poison,
        'Bleeding': bleeding, 
        'Burning': burning,
        'Nurrish': nurrish,
        'Dragon Burning': dragon_burning,
        'Dragon Toxin': dragon_toxin,
}