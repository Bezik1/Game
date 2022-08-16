class Food:
    def __init__(self, value: int) -> None:
        self.value = value
        
class Drink:
    def __init__(self, value: int) -> None:
        self.value = value

meat = Food(60)
fish = Food(40)
potatos = Food(60)
sweets = Food(30)

water = Drink(1)
beer = Drink(3)
juice = Drink(4)

food = {
    'Meat': meat,
    'Fish': fish,
    'Potatos': potatos,
    'Sweets': sweets,
}

drink = {
    'Water': water,
    'Beer': beer,
    'Juice':  juice,
}