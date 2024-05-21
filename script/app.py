from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from game import Game
from randomNum import Random
import sys

app = Flask(__name__)
CORS(app)

# Initialize rand and game variables
rand = Random()
game = None

if len(sys.argv) > 1:
    rand.setSeed(int(sys.argv[1]))

@app.route('/')
def serve_game():
    return send_from_directory('static', 'game.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global game
    data = request.get_json()
    width = data['width']
    height = data['height']
    num_players = data['num_players']
    game = Game(width, height, num_players, rand)
    return jsonify({"message": "Game started", "width": width, "height": height, "num_players": num_players})

@app.route('/move', methods=['POST'])
def move():
    global game
    data = request.get_json()
    player_id = data['player_id']
    direction = data['direction']
    distance = data['distance']
    player = game.listOfPlayers[player_id - 1]
    player.move(direction, distance)
    return jsonify({"message": "Player moved", "player_id": player_id, "new_position": (player.x, player.y)})

@app.route('/rest', methods=['POST'])
def rest():
    global game
    data = request.get_json()
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

if __name__ == '__main__':
    app.run(debug=True)

