from PyQt5.QtWidgets import QPushButton, QLabel

def reset(game):
    game.player.health = 100
    game.player.mana = 10
    game.player.effect = None
        
def game_over(game):
    reset(game)
    game.delete_layout_items(game, game.layouts)

    end_label = QLabel('Koniec gry, zwycięża ' + game.winner, game)
    lobby = QPushButton('Lobby', game)
    arena = QPushButton('Arena', game)

    game.layouts.addWidget(end_label, 0, 2)
    game.layouts.addWidget(lobby, 1, 1)
    game.layouts.addWidget(arena, 1, 3)

    def lobby_connect():
        reset(game)
        game.delete_layout_items(game, game.layouts)
        game.clicked = 'character'
        game.name_action()
        
    def arena_connect():
        game.clicked = 'arena'
        game.delete_layout_items(game, game.layouts)
        game.name_action()

    lobby.clicked.connect(lobby_connect)
    arena.clicked.connect(arena_connect)