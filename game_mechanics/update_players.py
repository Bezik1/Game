def update_players(game):
    game.player_name_label.setText(
        'Gracz: '+ game.player.name + '\n' + 
        'Mana: ' + str(game.player.mana) + '\n' +
        'Zdrowie' + str(game.player.health) + '\n' +
        'Efekty: ' +  game.is_effect(game.player))
    
    game.opponent_name_label.setText(
        'Gracz: '+ game.opponent.name + '\n' + 
        'Mana: ' + str(game.opponent.mana) + '\n' +
        'Zdrowie' + str(game.opponent.health) + '\n' +
        'Efekty: ' +  game.is_effect(game.opponent))