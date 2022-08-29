from ast import ClassDef
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox
import random

from players.characters import Mage, Warrior, Shaman

class Arena:
    def __init__(self, game: ClassDef) -> None:
        self.game = game
    
    def enemy_generator(self):
        random_number = random.randint(0, 2)
        
        match random_number:
            case 0:
                self.game.opponent = Mage('Człowiek')
            case 1:
                self.game.opponent = Warrior('Ork')
            case 2:
                self.game.opponent = Shaman('Żywiołak')
        self.game.opponent.equipment()
    
    def game_start(self):
        self.game.delete_layout_items(self.game, self.game.layouts)
        self.enemy_generator()

        self.game.player_name_label = QLabel(
        'Gracz: '+ self.game.name.text() + '\n' + 
        'Mana: ' + str(self.game.player.mana) + '\n' +
        'Zdrowie' + str(self.game.player.health) + '\n' +
        'Efekty: ' +  self.game.is_effect(self.game.player)
        , self.game)
        
        self.game.opponent_name_label = QLabel(
            'Gracz: '+ self.game.opponent.name + '\n' + 
            'Mana: ' + str(self.game.opponent.mana) + '\n' +
            'Zdrowie' + str(self.game.opponent.health) + '\n' +
            'Efekty: ' +  self.game.is_effect(self.game.opponent)
        , self.game)
                            
        self.mana_error_player = QLabel('', self.game)
        self.mana_error_opponent = QLabel('', self.game)      
        
        self.game.layouts.addWidget(self.game.player_name_label, 0, 0)
        self.game.layouts.addWidget(self.mana_error_player, 1, 0)
        
        self.game.layouts.addWidget(self.game.opponent_name_label, 0, 3)
        self.game.layouts.addWidget(self.mana_error_opponent, 1, 3)
        
        self.choose_weapon()
    
    def choose_weapon(self):
        if self.game.player.health <= 0 or self.game.opponent.health <= 0:
            if self.game.player.health <= 0:
                self.game.winner = self.game.opponent.name
            elif self.game.opponent.health <= 0:
                self.game.winner = self.game.player.name
            self.game.game_over(self.game)
        else:                  
            def skipped():
                self.game.round = False
                self.choose_attack()
            
            self.game.weapon_box = QComboBox(self.game)
            self.game.weapon_box.setGeometry(200, 150, 120, 30)
            weapon_list = []
            
            for weapon in self.game.player.eq.keys():
                weapon_list.append(weapon)
            
            self.game.weapon_box.addItems(weapon_list)
            
            self.game.weapon_label = QLabel('Wybierz broń: ', self.game)
            weapon_button = QPushButton('Wybierz', self.game)
            self.game.skip_button = QPushButton('Pomiń turę', self.game)
            
            self.game.layouts.addWidget(self.game.skip_button, 2, 2)
            self.game.layouts.addWidget(weapon_button, 2, 3)
            self.game.layouts.addWidget(self.game.weapon_box, 2, 1)
            self.game.layouts.addWidget(self.game.weapon_label, 2, 0)
            weapon_button.clicked.connect(self.choose_attack)
            self.game.skip_button.clicked.connect(skipped)
    
    def choose_attack(self):
        self.game.weapon_label.hide()
        self.game.weapon_box.hide()
        
        if self.game.round:
            weapon = self.game.weapon_box.currentText()
            
            self.game.attack_box = QComboBox(self.game)
            self.game.attack_box.setGeometry(200, 150, 120, 30)
            
            attack_list = []
            for attack in self.game.player.eq[weapon].attack_list.keys():
                attack_list.append(attack)
            
            self.game.attack_label = QLabel('Wybierz atak: ', self.game)
            self.game.attack_button = QPushButton('Wybierz', self.game)
            
            self.game.skip_button.hide()
            self.game.layouts.addWidget(self.game.attack_button, 2, 3)
            self.game.layouts.addWidget(self.game.attack_label, 2, 0)
            
            self.game.attack_box.addItems(attack_list) 
            self.game.layouts.addWidget(self.game.attack_box, 2, 1)
            
            def attack_action():
                attack = self.game.attack_box.currentText()
                if attack == 'ice block (5)' or attack == 'block (3)' or attack == 'heavy block (8)':
                    self.game.player.eq[weapon].attack_list[attack](self.game.player, self.mana_error_player)
                elif attack == 'stunning attack (7)':
                    self.game.player.eq[weapon].attack_list[attack](self.game.player, self.game.opponent, self.mana_error_player)
                    self.game.opponent_round = False
                else:
                    self.game.player.eq[weapon].attack_list[attack](self.game.player, self.game.opponent, self.mana_error_player)
                self.game.attack_box.hide()
                    
                self.game.enemy_attack(self.game, self.game.opponent, self.mana_error_opponent)
                self.game.effect_action(self.game.player, self.game.opponent)
                self.game.effect_action(self.game.opponent, self.game.player)
                self.game.update_players(self.game)
                
                self.game.attack_box.hide()
                self.game.attack_label.hide()
                
                self.choose_weapon()
            self.game.attack_button.clicked.connect(attack_action)
        else:
            self.game.round = True
            self.game.player.round_skip()
            self.game.enemy_attack(self.game, self.game.opponent, self.mana_error_opponent)
            self.game.effect_action(self.game.player, self.game.opponent)
            self.game.effect_action(self.game.opponent, self.game.player)
            self.game.update_players(self.game)
            self.choose_weapon()