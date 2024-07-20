from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from game import Game
from randomNum import Random
import sys

app = Flask(__name__)
CORS(app)

# Initialize the random generator
rand = Random()
if len(sys.argv) > 1:
    rand.setSeed(int(sys.argv[1]))
game = None

@app.route('/')
def serve_game():
    return render_template('game.html')

@app.route('/instructions')
def serve_instructions():
    return render_template('instructions.html')
@app.route('/form')
def serve_form():
    return render_template('form.html')

@app.route('/game_board')
def serve_game_board():
    return render_template('game_board.html')

@app.route('/winner')
def winner_page():
    return render_template('winner.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    data = request.get_json()
    width = data['width']
    height = data['height']
    num_players = data['num_players']
    print("Received width:", width, "height:", height, "num_players:", num_players)
    game = Game(width, height, num_players, rand)
    print("Game started with width: {}, height: {}, players: {}".format(width, height, num_players))

    game.drawUpdatedGameBoard()

    # Debugging information
    for player in game.listOfPlayers:
        print(f"Player {player.gameBoardSymbol} at ({player.x}, {player.y})")
    for treasure in game.listOfTreasures:
        print(f"Treasure {treasure.gameBoardSymbol} at ({treasure.x}, {treasure.y})")
    for weapon in game.listOfWeapons:
        print(f"Weapon {weapon.gameBoardSymbol} at ({weapon.x}, {weapon.y})")
    return jsonify({"message": "Game started", "width": width, "height": height, "num_players": num_players})

@app.route('/move', methods=['POST'])
def move():
    global game
    data = request.get_json()
    player_id = data['player_id']
    direction = data['direction']
    distance = data['distance']

    
    # Debugging information
    print(f"Move request received for player ID: {player_id}")
    print(f"Current list of players: {[player.gameBoardSymbol for player in game.listOfPlayers]}")
    
    # Find the player by gameBoardSymbol
    player = game.listOfPlayers[game.currentPlayerNum]
    
    if not player:
        return jsonify({"error": "Player not found"}), 400

    player.move(direction, distance)

    players_removed = []
    for other_player in list(game.listOfPlayers):  # Use list to avoid modification issues during iteration
        if player != other_player and player.x == other_player.x and player.y == other_player.y:
            game.listOfPlayers.remove(other_player)
            players_removed.append(other_player.gameBoardSymbol)
            print(f"You eliminated player {other_player.gameBoardSymbol} from the game!")
    
    # Check for treasure collection after moving
    for treasure in list(game.listOfTreasures):  # Use list to avoid modification issues during iteration
        if player.x == treasure.x and player.y == treasure.y:
            player.collectTreasure(treasure)
            game.listOfTreasures.remove(treasure)  # Remove the treasure from the game
            print(f"Treasure {treasure.name} collected by Player {player_id}")
    
    # Check for weapon collection after moving
    for weapon in list(game.listOfWeapons):  # Using list to avoid modification issues during iteration
        if player.x == weapon.x and player.y == weapon.y:
            player.collectWeapon(weapon)
            game.listOfWeapons.remove(weapon)  # Remove the weapon from the game
            print(f"Weapon {weapon.name} collected by Player {player_id}")
    
    # Check if all treasures are collected or only one player left
    if len(game.listOfTreasures) == 0 or len(game.listOfPlayers) == 1:
        winner = game.end_game()
        return jsonify({"message": "Game Over", "winner": winner.gameBoardSymbol, "game_over": True})


    # Update the current player index
    game.currentPlayerNum = (game.currentPlayerNum + 1) % len(game.listOfPlayers)
    
    # Debugging information
    current_player_id = game.listOfPlayers[game.currentPlayerNum].gameBoardSymbol
    print("Current Player ID after move:", current_player_id)  # Debugging statement
    
    return jsonify({"message": "Player moved", "player_id": player_id, "new_position": (player.x, player.y),"players_removed": players_removed, "current_player_id": current_player_id})

@app.route('/rest', methods=['POST'])
def rest():
    global game
    data = request.get_json()
    player_id = data['player_id']
    player = game.listOfPlayers[game.currentPlayerNum]
    player.energy += 2.0
    
    # Check if there are still other players left
    if len(game.listOfPlayers) > 1:
        game.currentPlayerNum = (game.currentPlayerNum + 1) % len(game.listOfPlayers)
        current_player_id = game.listOfPlayers[game.currentPlayerNum].gameBoardSymbol
    
    return jsonify({"message": "Player rested", "player_id": player_id, "new_energy": player.energy, "current_player_id": current_player_id})


@app.route('/attack', methods=['POST'])
def attack():
    print("Attack started")
    global game
    if not game:
        return jsonify({"error": "Game not started"}), 400

    data = request.get_json()
    player_id = data['player_id']
    # Convert player_id to integer if it's passed as a string
    player_id = int(player_id) if isinstance(player_id, str) else player_id
    # Ensure player_id is valid
    if player_id < 1 or player_id > len(game.listOfPlayers):
        return jsonify({"error": "Invalid player ID"}), 400

    player = game.listOfPlayers[game.currentPlayerNum]

    # Check if the player has any weapons
    if not player.collectedWeapons:
        # Update current player before returning the response
        game.currentPlayerNum = (game.currentPlayerNum + 1) % len(game.listOfPlayers)
        current_player_id = game.listOfPlayers[game.currentPlayerNum].gameBoardSymbol
        return jsonify({"message": "No weapons to attack", "current_player_id": current_player_id}), 400

    # Determine the weapon with the greatest strike distance
    weapon = player.collectedWeapons[0]
    highest_strike_weapon = max(player.collectedWeapons, key=lambda weapon: weapon.strikedistance)

    # Check if any players are in range and remove them
    players_removed = []
    for other_player in game.listOfPlayers[:]:
        if player != other_player:
            distance = ((player.x - other_player.x) ** 2 + (player.y - other_player.y) ** 2) ** 0.5
            if distance < highest_strike_weapon.strikedistance:
                game.listOfPlayers.remove(other_player)
                players_removed.append(other_player.gameBoardSymbol)
                print(f"You eliminated player {other_player.gameBoardSymbol} from the game!")
                player.collectedWeapons.remove(weapon)

    # Update current player after attack
    game.currentPlayerNum = (game.currentPlayerNum + 1) % len(game.listOfPlayers)
    current_player_id = game.listOfPlayers[game.currentPlayerNum].gameBoardSymbol
    print("Current Player ID after attack:", current_player_id)  # Debugging statement

    # Check if only one player is left
    if len(game.listOfPlayers) == 1:
        winner = game.listOfPlayers[0]
        return jsonify({
            "message": "Attack executed",
            "players_removed": players_removed,
            "game_over": True,
            "winner": winner.gameBoardSymbol,
            "current_player_id": current_player_id
        })

    return jsonify({
        "message": "Attack executed",
        "players_removed": players_removed,
        "current_player_id": current_player_id
    })

@app.route('/game_state', methods=['GET'])
def game_state():
    global game
    if not game:
        return jsonify({"error": "Game not started"}), 400

    player_data = [{
        "id": player.gameBoardSymbol,  # Use gameBoardSymbol as a unique identifier
        "x": player.x,
        "y": player.y,
        "points": player.getPoints(),  # Using the getPoints method to include points
        "energy": player.energy,
        "collectedTreasures": [{"name": treasure.name, "symbol": treasure.gameBoardSymbol} for treasure in player.collectedTreasures],
        "collectedWeapons": [{"name": weapon.name, "symbol": weapon.gameBoardSymbol} for weapon in player.collectedWeapons]
    } for player in game.listOfPlayers]

    treasures_data = [{
        "name": treasure.name,
        "symbol": treasure.gameBoardSymbol,  # Corrected attribute name
        "points": treasure.pointValue,
        "position": (treasure.x, treasure.y)
    } for treasure in game.listOfTreasures]

    weapons_data = [{
        "name": weapon.name,
        "symbol": weapon.gameBoardSymbol,  # Ensure correct attribute name is used if necessary
        "strike_distance": weapon.strikedistance,  # Correct attribute name if typo
        "position": (weapon.x, weapon.y)
    } for weapon in game.listOfWeapons]

    current_player_id = game.listOfPlayers[game.currentPlayerNum].gameBoardSymbol if game.listOfPlayers else None
    print("Current Player ID:", current_player_id)  # Debugging statement

    return jsonify({
        "width": game.gameBoardWidth,
        "height": game.gameBoardHeight,
        "players": player_data,
        "treasures": treasures_data,
        "weapons": weapons_data,
        "current_player_id": current_player_id
    })

if __name__ == '__main__':
    if len(sys.argv) > 1:
        rand.setSeed(int(sys.argv[1]))
    app.run(debug=True, port=5001)






