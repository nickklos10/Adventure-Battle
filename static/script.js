document.getElementById('startGame').addEventListener('click', startGame);

async function startGame() {
    const response = await fetch('http://127.0.0.1:5000/start_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            width: 10,
            height: 10,
            num_players: 2
        })
    });
    const data = await response.json();
    console.log(data);
    getGameState();
}

async function getGameState() {
    const response = await fetch('http://127.0.0.1:5000/game_state');
    const data = await response.json();
    console.log(data);
    renderGameBoard(data);
}

function renderGameBoard(data) {
    const gameBoard = document.getElementById('gameBoard');
    gameBoard.innerHTML = '';
    const size = 10; // assuming 10x10 board size

    for (let y = 0; y < size; y++) {
        for (let x = 0; x < size; x++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.textContent = '.';
            gameBoard.appendChild(cell);
        }
    }

    data.players.forEach(player => {
        const index = player.position[1] * size + player.position[0];
        const cell = gameBoard.children[index];
        cell.textContent = player.id;
    });

    data.treasures.forEach(treasure => {
        const index = treasure.position[1] * size + treasure.position[0];
        const cell = gameBoard.children[index];
        cell.textContent = treasure.symbol;
    });

    data.weapons.forEach(weapon => {
        const index = weapon.position[1] * size + weapon.position[0];
        const cell = gameBoard.children[index];
        cell.textContent = weapon.symbol;
    });
}
