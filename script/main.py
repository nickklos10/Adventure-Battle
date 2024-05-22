from __future__ import division
import math
from game import Game
from randomNum import Random
import sys

# Initialize Random instance
rand = Random()
if len(sys.argv) > 1:
    rand.setSeed(int(sys.argv[1]))

def main():
    w = int(input("Enter the width of the game board: "))
    h = int(input("Enter the height of the game board: "))
    numPlayers = int(input("How many players will play? "))
    
    # Create Game instance with rand passed as argument
    g = Game(w, h, numPlayers, rand)
    g.play()

if __name__ == "__main__":
    main()