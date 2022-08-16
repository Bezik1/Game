class Money:
    def __init__(self, value: int) -> None:
        self.value = value
        
class Crystal:
    def __init__(self, name: str, size: str) -> None:
        self.name = name
        self.size = size

class ManaCrystal(Crystal):
    def __init__(self, name: str, size: str) -> None:
        super().__init__(name, size)
    
    def useCrystal(self, character):
        character.mana = 20
        
class FireCrystal(Crystal):
    def __init__(self, name: str, size: str) -> None:
        super().__init__(name, size)
        
    def useCrystal(self, weapon):
        weapon.effect = 'fire'