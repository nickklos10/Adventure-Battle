from flask import Flask, request, jsonify, send_from_directory
import os
from game import Game
from treasure import Treasure
from player import Player
from randomNum import Random

app = Flask(__name__)
rand = Random()
game = None

@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    data = request.json
    width = data['width']
    height = data['height']
    num_players = data['num_players']
    game = Game(width, height, num_players)
    return jsonify({"message": "Game started"}), 200

@app.route('/move', methods=['POST'])
def move():
    global game
    data = request.json
    player_id = data['player_id']
    direction = data['direction']
    distance = data['distance']
    player = game.listOfPlayers[player_id - 1]
    player.move(direction, distance)
    return jsonify({"message": "Player moved", "player_id": player_id, "new_position": (player.x, player.y)})

@app.route('/rest', methods=['POST'])
def rest():
    global game
    data = request.json
    player_id = data['player_id']
    player = game.listOfPlayers[player_id - 1]
    player.energy += 4.0
    return jsonify({"message": "Player rested", "player_id": player_id, "new_energy": player.energy})

@app.route('/game_state', methods=['GET'])
def game_state():
    global game
    players = [{"id": p.gameBoardSymbol, "points": p.getPoints(), "energy": p.energy, "position": (p.x, p.y)} for p in game.listOfPlayers]
    treasures = [{"name": t.name, "symbol": t.gameBoardSymbol, "points": t.pointValue, "position": (t.x, t.y)} for t in game.listOfTreasures]
    weapons = [{"name": w.name, "symbol": w.gameBoardSymbol, "strike_distance": w.strikedistance, "position": (w.x, w.y)} for w in game.listOfWeapons]
    return jsonify({"players": players, "treasures": treasures, "weapons": weapons})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test endpoint working"}), 200

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)



