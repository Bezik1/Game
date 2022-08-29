from players.characters import Character
import random

def enemy_attack(game, opponent, mana_error_opponent):
        if game.opponent_round:
            opponent.equipment()
            mana_error_opponent.setText('')
            random_attack = random.randint(0, 3)
            
            
            def attack(attack_conf: dict[str, Character | str]):
                if attack_conf['enemy'] == None:
                    attack_conf['character'].eq[attack_conf['weapon']].attack_list[
                        attack_conf['attack']](attack_conf['character'], mana_error_opponent)
                else:
                    attack_conf['character'].eq[attack_conf['weapon']].attack_list[
                        attack_conf['attack']](attack_conf['character'], attack_conf['enemy'], mana_error_opponent)
                    
            match opponent.role:
                case 'Dragon':
                    match opponent.type:
                        case 'fire':
                            match random_attack:
                                case 0:
                                    opponent.fire_breath(game.player, mana_error_opponent)
                                case 1:
                                    opponent.sky_attack(game.player, mana_error_opponent)
                                case 2:
                                    opponent.lava_breath(game.player, mana_error_opponent)
                                case 3:
                                    opponent.mana_from_the_sky()
                case 'Mage':
                    match random_attack:
                        case 0:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Wand', 
                                'attack': 'fire ball (4)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
                        case 1:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Wand', 
                                'attack': 'ice block (5)',
                                'enemy': None
                            }
                            attack(attack_conf)
                        case 2:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Wand', 
                                'attack': 'thunder storm (2)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
                        case 3:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Wand', 
                                'attack': 'fire ball (4)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
                case 'Warrior':
                    match random_attack:
                        case 0:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Axe', 
                                'attack': 'straight attack (3)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
                        case 1:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Axe', 
                                'attack': 'strong attack (6)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
                        case 2:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Axe', 
                                'attack': 'charge attack (7)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
                        case 3:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Shield', 
                                'attack': 'block (3)',
                                'enemy': None
                            }
                            attack(attack_conf)
                case 'Shaman':
                    match random_attack:
                        case 0:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Runic Book', 
                                'attack': 'summon totem (3)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
                        case 1:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Runic Book', 
                                'attack': 'write rune (5)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
                        case 3:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Runic Book', 
                                'attack': 'summon thunder (10)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
                        case 4:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Runic Book', 
                                'attack': 'write rune (5)',
                                'enemy': game.player
                            }
                            attack(attack_conf)
        else:
            mana_error_opponent.setText('Ogłuszenie')
            game.opponent_round = True