from locale import currency
from PyQt5.QtWidgets import QPushButton, QLabel, QComboBox
from PyQt5.QtCore import Qt
import random

from mechanics.enemy_attack_system import enemy_attack
from players.characters import Mage, Warrior, Shaman
from players.opponents import Dragon
import ctypes
from ast import ClassDef 

class Dungeon:
    def __init__(self, game: ClassDef, floors_number: int) -> None:
        self.game = game
        self.floors_number = floors_number
    
    def enemies_generators(self, enemies_number):
        players = []
        
        for enemy in range(enemies_number + 1):
            random_number = random.randint(0, 2)
            match random_number:
                case 0:
                    player = Mage('Człowiek')
                    player.equipment()
                case 1:
                    player = Warrior('Ork')
                    player.equipment()
                case 2:
                    player = Shaman('Żywiołak')
                    player.equipment()
            players.append(player)
        return players

    
    def floors_generator(self, floors_number):
        for floor_number in range(floors_number):
            if floor_number == (floors_number -1):
                self.game.floors['Floor: ' + str(floor_number)] = [Dragon('Fire Dragon', 'fire', 200)]
            else:
                self.game.floors['Floor: ' + str(floor_number)] = self.enemies_generators(floor_number)
    
    def write_dungeon(self):
        florrs_labels = {}
        
        for floor in self.game.floors.keys():
            text = ''
            text += floor + ': '
            for enemy in self.game.floors[floor]:
                if enemy is self.game.floors[floor][-1]:
                    text += '\n' + enemy.name
                else:
                    text += '\n' + enemy.name + ', '
            florrs_labels[floor] = QLabel(text, self.game)
            florrs_labels[floor].setAlignment(Qt.AlignCenter)
            
        counter = 0
        for layout in florrs_labels.keys():
            self.game.layouts.addWidget(florrs_labels[layout], 2, counter)
            counter += 1
                 
    def dungeon_game(self):
        self.game.delete_layout_items(self.game.layouts)
        self.game.current_enemy = self.game.floors['Floor: ' + str(self.game.current_floor)][self.game.enemy]
        
        if self.game.player.health <= 0 or self.game.current_enemy.health <= 0:
            if self.game.player.health <= 0:
                self.game.winner = self.game.current_enemy.name
                self.game.game_over()
            elif self.game.current_floor == 2:
                if self.game.current_enemy is self.game.floors['Floor: ' + str(self.game.current_floor)][-1]:
                    self.game.winner = self.game.current_enemy.name
                    self.game.game_over()
            else:
                if self.game.current_enemy is self.game.floors['Floor: ' + str(self.game.current_floor)][-1]:
                    if self.game.current_enemy.health <= 0:
                        self.game.current_floor += 1
                        self.game.enemy = 0
                        self.dungeon_game()
                else:
                    self.game.enemy += 1
                    self.dungeon_game()
        
        player_label = QLabel(
            'Gracz: '+ self.game.player.name + '\n' + 
            'Mana: ' + str(self.game.player.mana) + '\n' +
            'Zdrowie' + str(self.game.player.health) + '\n' +
            'Efekty: ' +  self.game.is_effect(self.game.player)
        , self.game)

        enemy_label = QLabel(
            'Gracz: '+ self.game.current_enemy.name + '\n' +
            'Mana: ' + str(self.game.current_enemy.mana) + '\n' +
            'Zdrowie' + str(self.game.current_enemy.health) + '\n' +
            'Efekty: ' +  self.game.is_effect(self.game.current_enemy)
        , self.game)
        
        def update_players():
            player_label.setText(
                'Gracz: '+ self.game.player.name + '\n' + 
                'Mana: ' + str(self.game.player.mana) + '\n' +
                'Zdrowie' + str(self.game.player.health) + '\n' +
                'Efekty: ' +  self.game.is_effect(self.game.player)
            )

            enemy_label.setText(
                'Gracz: '+ self.game.current_enemy.name + '\n' +
                'Mana: ' + str(self.game.current_enemy.mana) + '\n' +
                'Zdrowie' + str(self.game.current_enemy.health) + '\n' +
                'Efekty: ' +  self.game.is_effect(self.game.current_enemy)
            )
        
        mana_player_label = QLabel('', self.game)
        mana_enemy_label = QLabel('', self.game)
        
        current_floor_label = QLabel('Piętro: ' + str(self.game.current_floor), self.game)
        
        def update_floor():
            current_floor_label.setText(
                'Piętro: ' + str(self.game.current_floor) + '\n'
                'Obecny przeciwnik: ' + self.game.current_enemy.name
            )
            
        self.game.layouts.addWidget(current_floor_label, 0, 0)
        self.game.layouts.addWidget(mana_player_label, 0, 0)
        self.game.layouts.addWidget(mana_enemy_label, 0, 4)
        self.game.layouts.addWidget(player_label, 1, 0)
        self.game.layouts.addWidget(enemy_label, 1, 4)

        update_players()
        update_floor()
        
        def dungeon_choose_attack():
            self.game.dungeon_weapon_label.hide()
            self.game.skip_round_button.hide()
            self.game.dungeon_weapon_button.hide()
            self.game.dungeon_weapon_box.hide()
            if self.game.round:                            
                weapon = self.game.dungeon_weapon_box.currentText()
                
                self.game.dungeon_attack_label = QLabel('Wybierz atak', self.game)
                self.game.dungeon_attack_button = QPushButton('Zapisz', self.game)
                self.game.dungeon_attack_box = QComboBox(self.game)
                
                attack_list = []
                for attack in self.game.player.eq[weapon].attack_list.keys():
                    attack_list.append(attack)
                
                self.game.dungeon_attack_box.addItems(attack_list)
                
                self.game.layouts.addWidget(self.game.dungeon_attack_label, 3, 0)
                self.game.layouts.addWidget(self.game.dungeon_attack_box, 3, 2)
                self.game.layouts.addWidget(self.game.dungeon_attack_button, 3, 4)
                
                self.game.dungeon_attack_button.clicked.connect(dungeon_player_attack)
            else:
                mana_player_label.setText('Pominięto rundę')
                self.game.player.round_skip()
                
                dungeon_player_attack()
        
        def dungeon_player_attack():
            
            if self.game.round:
                weapon = self.game.dungeon_weapon_box.currentText()
                attack = self.game.dungeon_attack_box.currentText()
                
                if attack == 'ice block (5)' or attack == 'block (3)' or attack == 'heavy block (8)':
                    self.game.player.eq[weapon].attack_list[attack](self.game.player, mana_player_label)
                elif attack == 'stunning attack (7)':
                    self.game.player.eq[weapon].attack_list[attack](self.game.player, self.game.current_enemy, mana_player_label)
                    self.game.opponent_round = False
                else:
                    self.game.player.eq[weapon].attack_list[attack](self.game.player, self.game.current_enemy, mana_player_label)
                self.game.dungeon_attack_label.hide()
                self.game.dungeon_attack_button.hide()
                self.game.dungeon_attack_box.hide()
        
            self.game.round = True
            
            current_floor_label.hide()
            mana_player_label.hide()
            mana_enemy_label.hide()
            player_label.hide()
            enemy_label.hide()
            
            enemy_attack(self.game, self.game.current_enemy, mana_enemy_label)
            self.game.effect_action(self.game.player, self.game.current_enemy)
            self.game.effect_action(self.game.current_enemy, self.game.player)
            update_players()
            
            self.dungeon_game()
        
        def dungeon_choose_weapon():
            def skipped():
                self.game.round = False
                dungeon_choose_attack()
            
            self.game.dungeon_weapon_label = QLabel('Wybierz broń', self.game)
            self.game.skip_round_button = QPushButton('Pomiń turę', self.game)
            self.game.dungeon_weapon_button = QPushButton('Zapisz', self.game)
            self.game.dungeon_weapon_box = QComboBox(self.game)
            
            weapon_list = []
            for weapon in self.game.player.eq.keys():
                weapon_list.append(weapon)
            
            self.game.dungeon_weapon_box.addItems(weapon_list)
            
            self.game.layouts.addWidget(self.game.dungeon_weapon_label, 3, 0)
            self.game.layouts.addWidget(self.game.dungeon_weapon_box, 3, 2)
            self.game.layouts.addWidget(self.game.skip_round_button, 3, 3)
            self.game.layouts.addWidget(self.game.dungeon_weapon_button, 3, 4)
            
            self.game.dungeon_weapon_button.clicked.connect(dungeon_choose_attack)
            self.game.skip_round_button.clicked.connect(skipped)
            
        dungeon_choose_weapon()
        
    def dungeon_generator(self):
        self.floors_generator(self.floors_number)
        
        enemies: list[Mage | Warrior | Shaman] = self.game.floors['Floor: ' + str(self.game.current_floor)]
        
        for enemy in enemies:
            enemy.equipment()

        self.game.delete_layout_items(self.game.layouts)
        
        start_label = QLabel('Witaj ' + self.game.player.name, self.game)
        start_button = QPushButton('Wejdź do dungeon', self.game)
        
        start_label.setAlignment(Qt.AlignCenter)

        self.write_dungeon()
        
        self.game.layouts.addWidget(start_button, 3, 1)
        self.game.layouts.addWidget(start_label, 0, 1)
        start_button.clicked.connect(self.dungeon_game)
        
        self.dungeon_game()