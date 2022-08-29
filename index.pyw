from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QLabel, QGridLayout, QComboBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPalette, QImage, QBrush
from modes.dungeon import Dungeon
from modes.arena import Arena

from game_mechanics.delete_layout_items import delete_layout_items
from game_mechanics.enemy_attack_system import enemy_attack
from game_mechanics.game_resets_functions import game_over
from players.characters import Character, Mage, Warrior, Shaman
import ctypes

class Game(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.resize(1200, 800)
        self.clicked = 'name'
        self.delete_layout_items = delete_layout_items
        self.enemy_attack = enemy_attack
        self.game_over = game_over
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
                arena = Arena(self)
                arena.game_start()
            case 'dungeon':
                dungeon = Dungeon(self, 3)
                dungeon.dungeon_generator()

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

window = Game()
window.setWindowIcon(QIcon('assets/icon.ico'))

app_icon = QIcon()
app_icon.addFile('assets/icon.ico', QSize(64, 64))
app.setWindowIcon(app_icon)

try:
    app.exec_()
except SystemExit:
    print('Closing Window...')