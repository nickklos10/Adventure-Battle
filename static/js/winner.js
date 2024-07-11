document.addEventListener("DOMContentLoaded", function () {
  // Get the winner ID from the URL query string
  const urlParams = new URLSearchParams(window.location.search);
  const winner = urlParams.get("winner");

  // Display the winner message
  if (winner) {
    const winnerMessage = document.getElementById("winnerMessage");
    winnerMessage.innerHTML = `<h1>PLAYER ${winner} WINS !</h1>`;
    winnerMessage.style.display = "block";

    // Add some confetti for celebration
    confetti({
      particleCount: 150,
      spread: 70,
      origin: { y: 0.6 },
    });
  }
});
