document.querySelector(".start-button").addEventListener("click", (event) => {
  event.preventDefault();
  const width = document.getElementById("width").value;
  const height = document.getElementById("height").value;
  const num_players = document.getElementById("num_players").value;

  // Validate the input
  if (!width || !height || !num_players) {
    alert("Please fill in all the fields.");
    return;
  }

  const widthValue = parseInt(width, 10);
  const heightValue = parseInt(height, 10);
  const numPlayersValue = parseInt(num_players, 10);

  if (isNaN(widthValue) || isNaN(heightValue) || isNaN(numPlayersValue)) {
    alert("Please enter valid numbers.");
    return;
  }

  if (
    widthValue < 8 ||
    widthValue > 15 ||
    heightValue < 8 ||
    heightValue > 15
  ) {
    alert("Width and height must be between 8 and 15.");
    return;
  }

  // Prepare the data to send to the backend
  const gameSettings = {
    width: widthValue,
    height: heightValue,
    num_players: numPlayersValue,
  };

  // Send the data to the backend using the fetch API
  fetch("/start_game", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(gameSettings),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data); // Log the response from the server
      if (data.message === "Game started") {
        window.location.href = "/game_board"; // Redirect to the game board page
      }
    })
    .catch((error) => {
      console.error("Error starting the game:", error);
      alert("Failed to start the game.");
    });
});
