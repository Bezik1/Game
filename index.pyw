from locale import currency
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QGridLayout, QMessageBox, QComboBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPalette, QPixmap, QImage, QBrush
import random

from players.characters import Character, Mage, Warrior, Shaman
from players.opponents import Dragon
import ctypes

class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.resize(1200, 800)
        self.clicked = 'name'
        self.current_floor = 0
        self.enemy = 0
        self.floors: dict[str, list[Mage | Warrior | Shaman]] = {}
        self.winner = None
        self.round = True
        self.opponent_round = True
        self.interface()
        self.show()
        
    
    def interface(self):
            
        self.layouts = QGridLayout()
        self.setLayout(self.layouts)
        
        self.write_name_label = QLabel('Podaj imię: ', self)
        name_label = QLabel('Twoje imię to: ', self)
        self.name = QLabel('', self)
        
        self.field = QLineEdit()
        
        self.name_button = QPushButton('Zapisz', self)
        self.name_button.setFixedWidth(200)
        
        self.character_label = QLabel('Twoja klasa to: ', self)
        self.character = QLabel('', self)
        
        oImage = QImage("assets/background.jpg")
        sImage = oImage.scaled(QSize(1200,800))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))                        
        self.setPalette(palette)
        
        self.character_label.hide()
                
        self.layouts.addWidget(name_label, 0, 0)
        self.layouts.addWidget(self.name, 0, 1)
        
        self.layouts.addWidget(self.character_label, 1, 0)
        self.layouts.addWidget(self.character, 1, 1)
        
        self.layouts.addWidget(self.write_name_label, 2, 0)
        self.layouts.addWidget(self.field, 2, 1)
        self.layouts.addWidget(self.name_button, 2, 2)
        
        self.name_button.clicked.connect(self.name_action)
    
    def is_effect(self, player):
        if player.effect:
            return player.effect.name + ' (pozostało ' + str(player.effect.time) + ' tur)'
        else:
            return 'Brak efektów'
    
    def update_players(self):
        self.player_name_label.setText(
            'Gracz: '+ self.player.name + '\n' + 
            'Mana: ' + str(self.player.mana) + '\n' +
            'Zdrowie' + str(self.player.health) + '\n' +
            'Efekty: ' +  self.is_effect(self.player))
        
        self.opponent_name_label.setText(
            'Gracz: '+ self.opponent.name + '\n' + 
            'Mana: ' + str(self.opponent.mana) + '\n' +
            'Zdrowie' + str(self.opponent.health) + '\n' +
            'Efekty: ' +  self.is_effect(self.opponent))
    
    def enemy_attack(self, opponent, mana_error_opponent):
        if self.opponent_round:
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
                                    opponent.fire_breath(self.player, mana_error_opponent)
                                case 1:
                                    opponent.sky_attack(self.player, mana_error_opponent)
                                case 2:
                                    opponent.lava_breath(self.player, mana_error_opponent)
                                case 3:
                                    opponent.mana_from_the_sky()
                case 'Mage':
                    match random_attack:
                        case 0:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Wand', 
                                'attack': 'fire ball (4)',
                                'enemy': self.player
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
                                'enemy': self.player
                            }
                            attack(attack_conf)
                        case 3:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Wand', 
                                'attack': 'fire ball (4)',
                                'enemy': self.player
                            }
                            attack(attack_conf)
                case 'Warrior':
                    match random_attack:
                        case 0:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Axe', 
                                'attack': 'straight attack (3)',
                                'enemy': self.player
                            }
                            attack(attack_conf)
                        case 1:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Axe', 
                                'attack': 'strong attack (6)',
                                'enemy': self.player
                            }
                            attack(attack_conf)
                        case 2:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Axe', 
                                'attack': 'charge attack (7)',
                                'enemy': self.player
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
                                'enemy': self.player
                            }
                            attack(attack_conf)
                        case 1:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Runic Book', 
                                'attack': 'write rune (5)',
                                'enemy': self.player
                            }
                            attack(attack_conf)
                        case 3:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Runic Book', 
                                'attack': 'summon thunder (10)',
                                'enemy': self.player
                            }
                            attack(attack_conf)
                        case 4:
                            attack_conf = {
                                'character': opponent, 
                                'weapon': 'Runic Book', 
                                'attack': 'write rune (5)',
                                'enemy': self.player
                            }
                            attack(attack_conf)
        else:
            mana_error_opponent.setText('Ogłuszenie')
            self.opponent_round = True
    
    def effect_action(self, player: Character, opponent: Character):
        if player.effect and player.effect.time > 0:
            player.effect.effect(opponent)
            player.effect.time -= 1
        elif player.effect and player.effect.time <= 0:
            player.effect = None
    
    def name_action(self):
        
        match self.clicked:
            case 'name':
                self.name.setText(self.field.text())
                self.write_name_label.setText('Wybierz klasę')
                self.character_label.show()
                #self.deleteItemsOfLayout(self.layouts)
                
                self.field.setParent(None)
                
                self.character_box = QComboBox(self)
                self.character_box.setGeometry(200, 150, 120, 30)
                character_list = ["mage", "warrior", "shaman"]
                
                self.character_box.addItems(character_list)
                self.layouts.addWidget(self.character_box, 2, 1)
                
                self.clicked = 'character'
            case 'character':
                self.character_box.hide()
                self.character.setText(self.character_box.currentText())
                
                match self.character_box.currentText():
                    case 'mage':
                        self.player = Mage(self.name.text())
                    case 'warrior':
                        self.player = Warrior(self.name.text())
                    case 'shaman':
                        self.player = Shaman(self.name.text())
                self.player.equipment()                  
                
                self.write_name_label.setText('Wybierz tryb')
                
                self.combo_box = QComboBox(self)
                self.combo_box.setGeometry(200, 150, 120, 30)
                mode_list = ["arena", "eq", "dungeon"]
                
                self.combo_box.addItems(mode_list)
                self.layouts.addWidget(self.combo_box, 2, 1)
                
                self.modes_button = QPushButton('Zapisz', self)
                self.name_button.setFixedWidth(200)
                
                self.layouts.addWidget(self.modes_button, 2, 2)
                
                self.clicked = 'mode'
                self.modes_button.clicked.connect(self.name_action)
            case 'mode':
                mode = self.combo_box.currentText()
                
                self.modes_button.hide()
                self.name_button.hide()
                self.name_button.hide()
                
                self.mode_button = QPushButton('Wejdź do ' + mode)
                self.mode_button.setFixedWidth(250)
                self.layouts.addWidget(self.mode_button, 2, 2)
                                
                self.clicked = mode
                self.mode_button.clicked.connect(self.name_action)
            case 'arena':
                self.delete_layout_items(self.layouts)
                
                def enemy_generator():
                    random_number = random.randint(0, 2)
                    
                    match random_number:
                        case 0:
                            self.opponent = Mage('Człowiek')
                        case 1:
                            self.opponent = Warrior('Ork')
                        case 2:
                            self.opponent = Shaman('Żywiołak')
                    self.opponent.equipment()
                enemy_generator()
                
                self.player_name_label = QLabel(
                    'Gracz: '+ self.name.text() + '\n' + 
                    'Mana: ' + str(self.player.mana) + '\n' +
                    'Zdrowie' + str(self.player.health) + '\n' +
                    'Efekty: ' +  self.is_effect(self.player)
                , self)
                
                self.opponent_name_label = QLabel(
                    'Gracz: '+ self.opponent.name + '\n' + 
                    'Mana: ' + str(self.opponent.mana) + '\n' +
                    'Zdrowie' + str(self.opponent.health) + '\n' +
                    'Efekty: ' +  self.is_effect(self.opponent)
                , self)
                                  
                mana_error_player = QLabel('', self)
                mana_error_opponent = QLabel('', self)      
                
                self.layouts.addWidget(self.player_name_label, 0, 0)
                self.layouts.addWidget(mana_error_player, 1, 0)
                
                self.layouts.addWidget(self.opponent_name_label, 0, 3)
                self.layouts.addWidget(mana_error_opponent, 1, 3)
                
                def choose_weapon():
                    if self.player.health <= 0 or self.opponent.health <= 0:
                        if self.player.health <= 0:
                            self.winner = self.opponent.name
                        elif self.opponent.health <= 0:
                            self.winner = self.player.name
                        self.game_over()
                    else:                  
                        def skipped():
                            self.round = False
                            choose_attack()
                        
                        self.weapon_box = QComboBox(self)
                        self.weapon_box.setGeometry(200, 150, 120, 30)
                        weapon_list = []
                        
                        for weapon in self.player.eq.keys():
                            weapon_list.append(weapon)
                        
                        self.weapon_box.addItems(weapon_list)
                        
                        self.weapon_label = QLabel('Wybierz broń: ', self)
                        weapon_button = QPushButton('Wybierz', self)
                        self.skip_button = QPushButton('Pomiń turę', self)
                        
                        self.layouts.addWidget(self.skip_button, 2, 2)
                        self.layouts.addWidget(weapon_button, 2, 3)
                        self.layouts.addWidget(self.weapon_box, 2, 1)
                        self.layouts.addWidget(self.weapon_label, 2, 0)
                        weapon_button.clicked.connect(choose_attack)
                        self.skip_button.clicked.connect(skipped)
                
                def choose_attack():
                    self.weapon_label.hide()
                    self.weapon_box.hide()
                    
                    if self.round:
                        weapon = self.weapon_box.currentText()
                        
                        self.attack_box = QComboBox(self)
                        self.attack_box.setGeometry(200, 150, 120, 30)
                        
                        attack_list = []
                        for attack in self.player.eq[weapon].attack_list.keys():
                            attack_list.append(attack)
                        
                        self.attack_label = QLabel('Wybierz atak: ', self)
                        self.attack_button = QPushButton('Wybierz', self)
                        
                        self.skip_button.hide()
                        self.layouts.addWidget(self.attack_button, 2, 3)
                        self.layouts.addWidget(self.attack_label, 2, 0)
                        
                        self.attack_box.addItems(attack_list) 
                        self.layouts.addWidget(self.attack_box, 2, 1)
                        
                        def attack_action():
                            attack = self.attack_box.currentText()
                            if attack == 'ice block (5)' or attack == 'block (3)' or attack == 'heavy block (8)':
                                self.player.eq[weapon].attack_list[attack](self.player, mana_error_player)
                            elif attack == 'stunning attack (7)':
                                self.player.eq[weapon].attack_list[attack](self.player, self.opponent, mana_error_player)
                                self.opponent_round = False
                            else:
                                self.player.eq[weapon].attack_list[attack](self.player, self.opponent, mana_error_player)
                            self.attack_box.hide()
                                
                            self.enemy_attack(self.opponent, mana_error_opponent)
                            self.effect_action(self.player, self.opponent)
                            self.effect_action(self.opponent, self.player)
                            self.update_players()
                            
                            self.attack_box.hide()
                            self.attack_label.hide()
                            
                            choose_weapon()
                        self.attack_button.clicked.connect(attack_action)
                    else:
                        self.round = True
                        self.player.round_skip()
                        self.enemy_attack(self.opponent, mana_error_opponent)
                        self.effect_action(self.player, self.opponent)
                        self.effect_action(self.opponent, self.player)
                        self.update_players()
                        choose_weapon()
                choose_weapon()
            case 'dungeon':
                def enemies_generators(enemies_number):
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

                
                def floors_generator(floors_number):
                    for floor_number in range(floors_number):
                        if floor_number == (floors_number -1):
                            self.floors['Floor: ' + str(floor_number)] = [Dragon('Fire Dragon', 'fire', 200)]
                        else:
                            self.floors['Floor: ' + str(floor_number)] = enemies_generators(floor_number)
                
                def write_dungeon():
                    florrs_labels = {}
                    
                    for floor in self.floors.keys():
                        text = ''
                        text += floor + ': '
                        for enemy in self.floors[floor]:
                            if enemy is self.floors[floor][-1]:
                                text += '\n' + enemy.name
                            else:
                                text += '\n' + enemy.name + ', '
                        florrs_labels[floor] = QLabel(text, self)
                        florrs_labels[floor].setAlignment(Qt.AlignCenter)
                        
                    counter = 0
                    for layout in florrs_labels.keys():
                        self.layouts.addWidget(florrs_labels[layout], 2, counter)
                        counter += 1                    
                 
                def dungeon_game():
                    self.delete_layout_items(self.layouts)
                    self.current_enemy = self.floors['Floor: ' + str(self.current_floor)][self.enemy]
                    
                    if self.player.health <= 0 or self.current_enemy.health <= 0:
                        if self.player.health <= 0:
                            self.winner = self.current_enemy.name
                            self.game_over()
                        elif self.current_floor == 2:
                            if self.current_enemy is self.floors['Floor: ' + str(self.current_floor)][-1]:
                                self.winner = self.current_enemy.name
                                self.game_over()
                        else:
                            if self.current_enemy is self.floors['Floor: ' + str(self.current_floor)][-1]:
                                if self.current_enemy.health <= 0:
                                    self.current_floor += 1
                                    self.enemy = 0
                                    dungeon_game()
                            else:
                                self.enemy += 1
                                dungeon_game()
                    
                    player_label = QLabel(
                        'Gracz: '+ self.player.name + '\n' + 
                        'Mana: ' + str(self.player.mana) + '\n' +
                        'Zdrowie' + str(self.player.health) + '\n' +
                        'Efekty: ' +  self.is_effect(self.player)
                    , self)

                    enemy_label = QLabel(
                        'Gracz: '+ self.current_enemy.name + '\n' +
                        'Mana: ' + str(self.current_enemy.mana) + '\n' +
                        'Zdrowie' + str(self.current_enemy.health) + '\n' +
                        'Efekty: ' +  self.is_effect(self.current_enemy)
                    , self)
                    
                    def update_players():
                        player_label.setText(
                            'Gracz: '+ self.player.name + '\n' + 
                            'Mana: ' + str(self.player.mana) + '\n' +
                            'Zdrowie' + str(self.player.health) + '\n' +
                            'Efekty: ' +  self.is_effect(self.player)
                        )

                        enemy_label.setText(
                            'Gracz: '+ self.current_enemy.name + '\n' +
                            'Mana: ' + str(self.current_enemy.mana) + '\n' +
                            'Zdrowie' + str(self.current_enemy.health) + '\n' +
                            'Efekty: ' +  self.is_effect(self.current_enemy)
                        )
                    
                    mana_player_label = QLabel('', self)
                    mana_enemy_label = QLabel('', self)
                    
                    current_floor_label = QLabel('Piętro: ' + str(self.current_floor), self)
                    
                    def update_floor():
                        current_floor_label.setText(
                            'Piętro: ' + str(self.current_floor) + '\n'
                            'Obecny przeciwnik: ' + self.current_enemy.name
                        )
                        
                    self.layouts.addWidget(current_floor_label, 0, 0)
                    self.layouts.addWidget(mana_player_label, 0, 0)
                    self.layouts.addWidget(mana_enemy_label, 0, 4)
                    self.layouts.addWidget(player_label, 1, 0)
                    self.layouts.addWidget(enemy_label, 1, 4)

                    update_players()
                    update_floor()
                    
                    def dungeon_choose_attack():
                        self.dungeon_weapon_label.hide()
                        self.skip_round_button.hide()
                        self.dungeon_weapon_button.hide()
                        self.dungeon_weapon_box.hide()
                        if self.round:                            
                            weapon = self.dungeon_weapon_box.currentText()
                            
                            self.dungeon_attack_label = QLabel('Wybierz atak', self)
                            self.dungeon_attack_button = QPushButton('Zapisz', self)
                            self.dungeon_attack_box = QComboBox(self)
                            
                            attack_list = []
                            for attack in self.player.eq[weapon].attack_list.keys():
                                attack_list.append(attack)
                            
                            self.dungeon_attack_box.addItems(attack_list)
                            
                            self.layouts.addWidget(self.dungeon_attack_label, 3, 0)
                            self.layouts.addWidget(self.dungeon_attack_box, 3, 2)
                            self.layouts.addWidget(self.dungeon_attack_button, 3, 4)
                            
                            self.dungeon_attack_button.clicked.connect(dungeon_player_attack)
                        else:
                            mana_player_label.setText('Pominięto rundę')
                            self.player.round_skip()
                            
                            dungeon_player_attack()
                    
                    def dungeon_player_attack():
                        
                        if self.round:
                            weapon = self.dungeon_weapon_box.currentText()
                            attack = self.dungeon_attack_box.currentText()
                            
                            if attack == 'ice block (5)' or attack == 'block (3)' or attack == 'heavy block (8)':
                                self.player.eq[weapon].attack_list[attack](self.player, mana_player_label)
                            elif attack == 'stunning attack (7)':
                                self.player.eq[weapon].attack_list[attack](self.player, self.current_enemy, mana_player_label)
                                self.opponent_round = False
                            else:
                                self.player.eq[weapon].attack_list[attack](self.player, self.current_enemy, mana_player_label)
                            self.dungeon_attack_label.hide()
                            self.dungeon_attack_button.hide()
                            self.dungeon_attack_box.hide()
                    
                        self.round = True
                        
                        current_floor_label.hide()
                        mana_player_label.hide()
                        mana_enemy_label.hide()
                        player_label.hide()
                        enemy_label.hide()
                        
                        self.enemy_attack(self.current_enemy, mana_enemy_label)
                        self.effect_action(self.player, self.current_enemy)
                        self.effect_action(self.current_enemy, self.player)
                        update_players()
                        
                        dungeon_game()
                    
                    def dungeon_choose_weapon():
                        def skipped():
                            self.round = False
                            dungeon_choose_attack()
                        
                        self.dungeon_weapon_label = QLabel('Wybierz broń', self)
                        self.skip_round_button = QPushButton('Pomiń turę', self)
                        self.dungeon_weapon_button = QPushButton('Zapisz', self)
                        self.dungeon_weapon_box = QComboBox(self)
                        
                        weapon_list = []
                        for weapon in self.player.eq.keys():
                            weapon_list.append(weapon)
                        
                        self.dungeon_weapon_box.addItems(weapon_list)
                        
                        self.layouts.addWidget(self.dungeon_weapon_label, 3, 0)
                        self.layouts.addWidget(self.dungeon_weapon_box, 3, 2)
                        self.layouts.addWidget(self.skip_round_button, 3, 3)
                        self.layouts.addWidget(self.dungeon_weapon_button, 3, 4)
                        
                        self.dungeon_weapon_button.clicked.connect(dungeon_choose_attack)
                        self.skip_round_button.clicked.connect(skipped)
                        
                    dungeon_choose_weapon()
                    
                def dungeon_generator(floors_number):
                    floors_generator(floors_number)
                    
                    enemies: list[Mage | Warrior | Shaman] = self.floors['Floor: ' + str(self.current_floor)]
                    
                    for enemy in enemies:
                        enemy.equipment()

                    self.delete_layout_items(self.layouts)
                    
                    start_label = QLabel('Witaj ' + self.player.name, self)
                    start_button = QPushButton('Wejdź do dungeon', self)
                    
                    start_label.setAlignment(Qt.AlignCenter)

                    write_dungeon()
                    
                    self.layouts.addWidget(start_button, 3, 1)
                    self.layouts.addWidget(start_label, 0, 1)
                    start_button.clicked.connect(dungeon_game)
                    
                dungeon_generator(3)
    
    def delete_layout_items(self, layout):
     if layout is not None:
         while layout.count():
             item = layout.takeAt(0)
             widget = item.widget()
             if widget is not None:
                 widget.setParent(None)
             else:
                 self.deleteItemsOfLayout(item.layout())

    def reset(self):
        self.player.health = 100
        self.player.mana = 10
        self.player.effect = None
        
    def game_over(self):
        self.reset()
        self.delete_layout_items(self.layouts)
        
        end_label = QLabel('Koniec gry, zwycięża ' + self.winner, self)
        lobby = QPushButton('Lobby', self)
        arena = QPushButton('Arena', self)
        
        self.layouts.addWidget(end_label, 0, 2)
        self.layouts.addWidget(lobby, 1, 1)
        self.layouts.addWidget(arena, 1, 3)
        
        def lobby_connect():
            self.reset()
            self.delete_layout_items(self.layouts)
            self.clicked = 'character'
            self.name_action()
            
        def arena_connect():
            self.clicked = 'arena'
            self.delete_layout_items(self.layouts)
            self.name_action()
        
        lobby.clicked.connect(lobby_connect)
        arena.clicked.connect(arena_connect)

app = QApplication([])
app.setApplicationName("Game")
app.setStyleSheet('''
    QWidget {
        font-size: 25px;
        font-weight: 550;
        color: #fff;
    }
    QComboBox {
        background: transparent;
    }
    QComboBox QAbstractItemView  {
        background-image: url("assets/background.jpg");
    }
    QPushButton { 
        background: transparent;
        border: 1px solid #fff;
    }
    QLineEdit {
        background: transparent;
        border: 1px solid #fff;
    }
    QLabel {
        width: auto;
        height: auto;
        text-align: center;
    }
''')

my_app_id = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

window = Window()
window.setWindowIcon(QIcon('assets/icon.ico'))

app_icon = QIcon()
app_icon.addFile('assets/icon.ico', QSize(64, 64))
app.setWindowIcon(app_icon)

try:
    app.exec_()
except SystemExit:
    print('Closing Window...')