from players.characters import Character

def effect_action(player: Character, opponent: Character):
    if player.effect and player.effect.time > 0:
        player.effect.effect(opponent)
        player.effect.time -= 1
    elif player.effect and player.effect.time <= 0:
        player.effect = None

def is_effect(player):
    if player.effect:
        return player.effect.name + ' (pozostało ' + str(player.effect.time) + ' tur)'
    else:
        return 'Brak efektów'