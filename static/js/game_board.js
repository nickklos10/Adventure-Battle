console.log("JS received");
let currentPlayer = 1;
let totalPlayers = 0;

const icons = {
  players: {
    P1: "static/images/form/icons_board/1.png", // Example path for player 1 icon
    P2: "static/images/form/icons_board/2.png", // Example path for player 2 icon
    P3: "static/images/form/icons_board/3.png", // Example path for player 3 icon
    P4: "static/images/form/icons_board/4.png", // Example path for player 4 icon
  },
  treasures: {
    G: "static/images/form/icons_board/gold.png",
    S: "static/images/form/icons_board/silver.png",
    P: "static/images/form/icons_board/platinum.png",
    D: "static/images/form/icons_board/diamond.png",
    E: "static/images/form/icons_board/emerald.png",
  },
  weapons: {
    "/": "static/images/form/icons_board/gun.png",
    o: "static/images/form/icons_board/grenade.png",
  },
};

async function getGameState() {
  const response = await fetch("/game_state");
  const data = await response.json();
  console.log("Received data:", data);
  console.log("Player's time:", data.current_player_id);
  if (data.error) {
    alert(data.error);
    return;
  }

  if (data.game_over) {
    console.log(
      `Game Over! Redirecting to winner page with winner ${data.winner}`
    );
    window.location.href = `/winner?winner=${data.winner}`;
    return;
  }

  renderGameBoard(data);

  if (data.players_removed) {
    data.players_removed.forEach((removedPlayerId) => {
      triggerFloatingEffect(removedPlayerId);
    });
  }

  if (totalPlayers === 0) {
    totalPlayers = data.players.length;
  }

  updatePlayerInfo(data.players);
  highlightCurrentPlayer(data.current_player_id, data.players);
  askPlayerAction(data.current_player_id);
}

function renderGameBoard(data) {
  console.log(`Rendering...`);
  const gameBoard = document.getElementById("gameBoard");
  gameBoard.innerHTML = "";
  const width = data.width;
  const height = data.height;

  gameBoard.style.gridTemplateColumns = `repeat(${width}, 30px)`;
  gameBoard.style.gridTemplateRows = `repeat(${height}, 30px)`;

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const cell = document.createElement("div");
      cell.classList.add("cell");
      gameBoard.appendChild(cell);
    }
  }

  appendElementsToGrid(data.players, gameBoard, "players", width, height);
  appendElementsToGrid(data.treasures, gameBoard, "treasures", width, height);
  appendElementsToGrid(data.weapons, gameBoard, "weapons", width, height);
}

function appendElementsToGrid(elements, gameBoard, type, width, height) {
  console.log(`Appending ${elements.length} elements of type ${type}`);
  elements.forEach((element) => {
    let x, y;

    if (type === "players") {
      x = element.x;
      y = element.y;
    } else if (type === "treasures" || type === "weapons") {
      if (!element.position || element.position.length < 2) {
        console.error(`Invalid or missing position data for ${type}:`, element);
        return;
      }
      x = element.position[0];
      y = element.position[1];
    }

    console.log("Width and Height:", width, height);
    console.log("X and Y coordinates for " + type + ":", x, y);

    if (
      typeof x !== "number" ||
      typeof y !== "number" ||
      x < 0 ||
      y < 0 ||
      x >= width ||
      y >= height
    ) {
      console.error(
        `Invalid or missing position data for ${type}: x=${x}, y=${y}`,
        element
      );
      return;
    }

    const index = y * width + x;
    if (index >= gameBoard.children.length || index < 0) {
      console.error(
        `Index out of range: ${index} for ${type} at position x: ${x}, y: ${y}`
      );
      return;
    }

    const cell = gameBoard.children[index];
    if (!cell) {
      console.error(`No cell found at index ${index} for ${type}`);
      return;
    }

    const img = document.createElement("img");
    img.src =
      type === "players" && icons[type]
        ? icons[type]["P" + element.id]
        : icons[type][element.symbol];
    img.alt = `${type} icon`;
    cell.appendChild(img);

    if (type === "players") {
      const balloon = document.createElement("div");
      balloon.className = "balloon-popup";
      balloon.innerHTML = `
        <p>Points: ${element.points}</p>
        <p>Energy: ${element.energy}</p>
        <div class="icons">
          ${element.collectedTreasures
            .map(
              (t) => `<img src="${icons.treasures[t.symbol]}" alt="Treasure">`
            )
            .join("")}
          ${element.collectedWeapons
            .map((w) => `<img src="${icons.weapons[w.symbol]}" alt="Weapon">`)
            .join("")}
        </div>
      `;
      cell.appendChild(balloon);
      console.log(`Added balloon for player ${element.id} at cell ${index}`);
    }

    if (type === "players") {
      cell.setAttribute("data-player-id", element.id);
      cell.setAttribute("data-x", x);
      cell.setAttribute("data-y", y);
      console.log(
        `Set data-player-id=${element.id} for cell at index ${index}`
      );
      if (element.id === currentPlayer) {
        cell.classList.add("glowing-cell");
      }
    }
  });
}

function updatePlayerInfo(players) {
  players.forEach((player, index) => {
    const playerId = index + 1; // Assuming player IDs are sequential starting at 1
    let pointsElement = document.getElementById(`player${playerId}Points`);
    let energyElement = document.getElementById(`player${playerId}Energy`);
    if (pointsElement && energyElement) {
      pointsElement.textContent = player.points;
      energyElement.textContent = player.energy;
    } else {
      console.log(`Elements for player ${playerId} not found.`);
    }

    const popup = document.getElementById(`player${playerId}Info`);
    if (popup) {
      popup.innerHTML = `
        <div class="player-info">
          <p>Points: ${player.points}</p>
          <p>Energy: ${player.energy}</p>
          <div class="collected-items">${collectedItems}</div>
        </div>
      `;
    } else {
      console.log(`Popup for player ${playerId} not found.`);
    }
  });
}

function askPlayerAction(playerId) {
  const actionContainer = document.getElementById("Actions");
  actionContainer.innerHTML = `
  <div class="container">
  <a
    href="#"
    class="button start-button"
    id="moveButton"
    onclick="chooseAction(${playerId}, 'move')"
  >
    <div class="button__content">
      <span class="button__text">Move</span>

      <div class="button__reflection-1"></div>
      <div class="button__reflection-2"></div>
    </div>

    <img
      src="static/images/form/icons/runner.png"
      alt=""
      class="runner-1"
    />
    <img
      src="static/images/form/icons/runner.png"
      alt=""
      class="runner-2"
    />

    <div class="button__shadow"></div>
  </a>
</div>

<div class="container2">
  <a
    href="#"
    class="button2 start-button"
    id="restButton"
    onclick="chooseAction(${playerId}, 'rest')"
  >
    <div class="button__content2">
      <span class="button__text2">Rest</span>

      <div class="button__reflection-12"></div>
      <div class="button__reflection-22"></div>
    </div>

    <img src="static/images/form/icons/rest.png" alt="" class="rest-1" />
    <img src="static/images/form/icons/rest.png" alt="" class="rest-2" />

    <div class="button__shadow2"></div>
  </a>
</div>

<div class="container3">
  <a
    href="#"
    class="button3 start-button"
    id="attackButton"
    onclick="chooseAction(${playerId}, 'attack')"
  >
    <div class="button__content3">
      <span class="button__text3">Attack</span>

      <div class="button__reflection-13"></div>
      <div class="button__reflection-23"></div>
    </div>

    <img
      src="static/images/form/icons/swords.png"
      alt=""
      class="swords-1"
    />
    <img
      src="static/images/form/icons/swords.png"
      alt=""
      class="swords-2"
    />

    <div class="button__shadow3"></div>
  </a>
</div>
  `;
}

function chooseAction(playerId, action) {
  console.log("Action: ", action, playerId);

  const actionContainer = document.getElementById("Actions");
  if (action === "move") {
    actionContainer.innerHTML = `
    <div class="container4">
    <a
      href="#"
      class="button4 start-button"
      onclick="movePlayer(${playerId}, 'r')"
    >
      <div class="button__content4">
        <span class="button__text4">Right</span>

        <div class="button__reflection-14"></div>
        <div class="button__reflection-24"></div>
      </div>

      <img
        src="static/images/form/icons-action/right-arrow.png"
        alt=""
        class="right-1"
      />
      <img
        src="static/images/form/icons-action/right-arrow.png"
        alt=""
        class="right-2"
      />

      <div class="button__shadow4"></div>
    </a>
  </div>

  <div class="container5">
    <a
      href="#"
      class="button5 start-button"
      onclick="movePlayer(${playerId}, 'l')"
    >
      <div class="button__content5">
        <span class="button__text5">Left</span>

        <div class="button__reflection-15"></div>
        <div class="button__reflection-25"></div>
      </div>

      <img
        src="static/images/form/icons-action/turn-left.png"
        alt=""
        class="left-1"
      />
      <img
        src="static/images/form/icons-action/turn-left.png"
        alt=""
        class="left-2"
      />

      <div class="button__shadow5"></div>
    </a>
  </div>

  <div class="container6">
    <a
      href="#"
      class="button6 start-button"
      onclick="movePlayer(${playerId}, 'u')"
    >
      <div class="button__content6">
        <span class="button__text6">Up</span>

        <div class="button__reflection-16"></div>
        <div class="button__reflection-26"></div>
      </div>

      <img
        src="static/images/form/icons-action/arrow-up.png"
        alt=""
        class="up-1"
      />
      <img
        src="static/images/form/icons-action/arrow-up.png"
        alt=""
        class="up-2"
      />

      <div class="button__shadow6"></div>
    </a>
  </div>

  <div class="container7">
    <a
      href="#"
      class="button7 start-button"
      onclick="movePlayer(${playerId}, 'd')"
    >
      <div class="button__content7">
        <span class="button__text7">Down</span>

        <div class="button__reflection-17"></div>
        <div class="button__reflection-27"></div>
      </div>

      <img
        src="static/images/form/icons-action/down-arrow.png"
        alt=""
        class="down-1"
      />
      <img
        src="static/images/form/icons-action/down-arrow.png"
        alt=""
        class="down-2"
      />

      <div class="button__shadow7"></div>
    </a>
  </div>
        `;
  } else if (action === "rest") {
    restPlayer(playerId);
  } else if (action === "attack") {
    attackPlayer(playerId);
  }
}

function getPlayerId() {
  // Logic to get the playerId
  return 1; // Replace this with actual logic
}

async function movePlayer(playerId, direction) {
  // Create the form HTML
  const formHtml = `
  <div class="distance-input-form">
    <a href="#" class="button8 start-button" id="howFarButton">
      <div class="button__content8">
        <span class="button__text8">How far?</span>
        <input type="number" id="distanceInput" />
      </div>
    </a>
  </div>
  `;

  // Insert the form HTML into the container
  document.getElementById("distanceInputContainer").innerHTML = formHtml;

  // Add event listener to handle form submission when Enter key is pressed
  document
    .getElementById("distanceInput")
    .addEventListener("keydown", async function (event) {
      if (event.key === "Enter") {
        const distance = document.getElementById("distanceInput").value;
        document.getElementById("distanceInputContainer").innerHTML = ""; // Clear the form
        const response = await fetch("/move", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            player_id: playerId,
            direction: direction,
            distance: parseInt(distance, 10),
          }),
        });
        const data = await response.json();
        console.log(data);

        if (data.game_over) {
          console.log(
            `Game Over! Redirecting to winner page with winner ${data.winner}`
          );
          window.location.href = `/winner?winner=${data.winner}`;
        } else {
          if (data.players_removed && data.players_removed.length > 0) {
            data.players_removed.forEach((removedPlayerId) => {
              triggerEliminationEffect(removedPlayerId);
            });

            setTimeout(() => {
              currentPlayer = (currentPlayer % totalPlayers) + 1;
              getGameState();
            }, 1000); // Match this duration with the animation duration
          } else {
            currentPlayer = (currentPlayer % totalPlayers) + 1;
            getGameState();
          }
        }
      }
    });
}

async function restPlayer(playerId) {
  const response = await fetch("/rest", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      player_id: playerId,
    }),
  });
  const data = await response.json();
  console.log(data);

  // Update game state and proceed to the next player
  currentPlayer = (currentPlayer % totalPlayers) + 1;
  getGameState();
}

async function attackPlayer(playerId) {
  const response = await fetch("/attack", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      player_id: playerId,
    }),
  });
  const data = await response.json();
  console.log(data);

  if (data.game_over) {
    window.location.href = `/winner?winner=${data.winner}`;
  } else {
    // Check if there were any players removed
    if (data.players_removed) {
      data.players_removed.forEach((removedPlayerId) => {
        triggerEliminationEffect(removedPlayerId); // Trigger explosion for each eliminated player
      });
    } else if (data.message === "No players were in range for the attack") {
      alert("No players were in range for the attack");
    } else {
      alert("You don't have a weapon for an attack");
    }
  }

  // Delay the game state update to ensure explosion effect is visible
  setTimeout(() => {
    currentPlayer = (currentPlayer % totalPlayers) + 1;
    getGameState();
  }, 1000); // Match this duration with the animation duration
}

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM fully loaded and parsed");

  // Initial game state load
  getGameState();
});

function highlightCurrentPlayer(currentPlayerId, players) {
  console.log(`Highlighting player ${currentPlayerId}`);

  // Remove glowing effect from all cells
  document.querySelectorAll(".cell").forEach((cell) => {
    cell.classList.remove("glowing-cell");
    cell.classList.remove("red-glowing-cell");
  });

  // Find the current player's data
  const currentPlayer = players.find((player) => player.id === currentPlayerId);
  if (!currentPlayer) {
    console.log(`No player found with ID ${currentPlayerId}`);
    return;
  }

  // Find and highlight the current player's cell
  const playerCell = document.querySelector(
    `[data-player-id='${currentPlayerId}']`
  );

  if (playerCell) {
    console.log(`Found cell for player ${currentPlayerId}`);
    if (currentPlayer.energy === 0) {
      playerCell.classList.add("red-glowing-cell");
    } else {
      playerCell.classList.add("glowing-cell");
    }
  } else {
    console.log(`No cell found for player ${currentPlayerId}`);
  }
}

function triggerEliminationEffect(playerId) {
  const playerCell = document.querySelector(`[data-player-id='${playerId}']`);
  if (playerCell) {
    console.log(`Triggering elimination effect for player ${playerId}`);

    // Create and add the explosion element
    const explosion = document.createElement("div");
    explosion.classList.add("explosion");
    playerCell.appendChild(explosion);

    // Remove the explosion element after the animation is done
    setTimeout(() => {
      if (playerCell.contains(explosion)) {
        playerCell.removeChild(explosion);
        console.log(`Explosion removed for player: ${playerId}`);
      } else {
        console.error("Explosion element was not found for removal.");
      }
    }, 1000); // Match this duration with the animation duration
  } else {
    console.error(`No cell found for player ${playerId}`);
  }
}
