from randomNum import Random
from player import Player
from treasure import Treasure
from weapon import Weapon

class Game:
    def __init__(self, gameBoardWidth, gameBoardHeight, numberofplayers, rand):
        self.gameBoardWidth = gameBoardWidth
        self.gameBoardHeight = gameBoardHeight
        self.numberofplayers = numberofplayers
        self.rand = rand  # Store rand instance
        self.listOfPlayers = []
        self.listOfTreasures = []
        self.listOfWeapons = []
        self.currentPlayerNum = 0  # Initialize the current player index

        number = 0
        for p in range(numberofplayers):
            number += 1
            while True:
                w = self.rand.randrange(gameBoardWidth)
                h = self.rand.randrange(gameBoardHeight)
                if self.is_position_empty(w, h):
                    self.listOfPlayers.append(Player(w, h, number))
                    break

        while True:
                w = self.rand.randrange(gameBoardWidth)
                h = self.rand.randrange(gameBoardHeight)
                if self.is_position_empty(w, h):
                    self.listOfTreasures.append(Treasure("silver", "S", 20, w, h))
                    break

        while True:
                w = self.rand.randrange(gameBoardWidth)
                h = self.rand.randrange(gameBoardHeight)
                if self.is_position_empty(w, h):
                    self.listOfTreasures.append(Treasure("gold", "G", 25, w, h))
                    break

        while True:
                w = self.rand.randrange(gameBoardWidth)
                h = self.rand.randrange(gameBoardHeight)
                if self.is_position_empty(w, h):
                    self.listOfTreasures.append(Treasure("platinum", "P", 50, w, h))
                    break

        while True:
                w = self.rand.randrange(gameBoardWidth)
                h = self.rand.randrange(gameBoardHeight)
                if self.is_position_empty(w, h):
                    self.listOfTreasures.append(Treasure("diamond", "D", 40, w, h))
                    break

        while True:
                w = self.rand.randrange(gameBoardWidth)
                h = self.rand.randrange(gameBoardHeight)
                if self.is_position_empty(w, h):
                    self.listOfTreasures.append(Treasure("emerald", "E", 35, w, h))
                    break

        while True:
                  w = self.rand.randrange(gameBoardWidth)
                  h = self.rand.randrange(gameBoardHeight)
                  if self.is_position_empty(w, h):
                      self.listOfWeapons.append(Weapon("gun", w, h, "/", 5))
                      break

        while True:
                w = self.rand.randrange(gameBoardWidth)
                h = self.rand.randrange(gameBoardHeight)
                if self.is_position_empty(w, h):
                    self.listOfWeapons.append(Weapon("grenade", w, h, "o", 3))
                    break

    def play(self):
        self.printInstructions()
      
        self.drawUpdatedGameBoard()
    
    
        # MAIN GAME LOOP to ask players what they want to do
        currentPlayerNum = 0
        while (len(self.listOfTreasures) >= 1):
            
            # get the player object for the player whose turn it is
            currentPlayer = self.listOfPlayers[currentPlayerNum];
         
            # ask the player what they would like to do
            choice = input("Player " + str(currentPlayer.gameBoardSymbol) + ", do you want to (m)ove, (r)est or (a)ttack? ")
            self.processPlayerInput(currentPlayer, choice)
            
            if len(self.listOfPlayers) < 2:
              break
            
            # show the updated player information and game board
            self.printUpdatedPlayerInformation();
            self.drawUpdatedGameBoard()
            
            # update whose turn it is
            currentPlayerNum += 1
            if currentPlayerNum >= len(self.listOfPlayers):
                currentPlayerNum = 0
        
        loop = 0 
        highest = 0
        

    
    def is_position_empty(self, x, y):
        for player in self.listOfPlayers:
            if player.x == x and player.y == y:
                return False
        for treasure in self.listOfTreasures:
            if treasure.x == x and treasure.y == y:
                return False
        for weapon in self.listOfWeapons:
            if weapon.x == x and weapon.y == y:
                return False
        return True
 
        
        
    
    def processPlayerInput(self, plyr, action) :
        if action == "m":  # move
            direction = input("Which direction (r, l, u, or d)? ")
            distance = int(input("How Far? "))
            plyr.move(direction,distance)


            # Check for player elimination
            for player in self.listOfPlayers:
              if plyr != player:
               if plyr.x == player.x and plyr.y == player.y:
                self.listOfPlayers.remove(player)
                print("You eliminated player", player.gameBoardSymbol ,"from the game!")

            for weapon in self.listOfWeapons:
              if plyr.x == weapon.x and plyr.y == weapon.y:
                plyr.collectWeapon(weapon)
                print("You acquired the", weapon.name + "!")
                self.listOfWeapons.remove(weapon)
                  
              
                
            # check to see if player moved to the location of another game item
            for treasure in self.listOfTreasures:
                if plyr.x == treasure.x and plyr.y == treasure.y:
                    plyr.collectTreasure(treasure)
                    print("You collected",treasure.name,"worth",treasure.pointValue,"points!")
                    self.listOfTreasures.remove(treasure)  # remove the treasure from the list of available treasures
                    break
        elif action == "a":
            # Determine the weapon with the greatest strike distance
            highest_strike_weapon = max(self.listOfWeapons, key=lambda weapon: weapon.strikedistance)
            
            # Check for player elimination within strike distance
            eliminated_players = []
            for player in list(self.listOfPlayers):
                if plyr != player:
                    distance = ((plyr.x - player.x) ** 2 + (plyr.y - player.y) ** 2) ** 0.5
                    if distance < highest_strike_weapon.strikedistance:
                        eliminated_players.append(player)
            
            for player in eliminated_players:
                self.listOfPlayers.remove(player)
                print(f"You eliminated player {player.gameBoardSymbol} from the game!")
         
        elif action == "r":
          plyr.energy += 4.0
        else :
            print("Sorry, that is not a valid choice")

        # Check if the game should continue
        if len(self.listOfPlayers) < 2 or len(self.listOfTreasures) == 0:
            self.end_game()
        else:
            # Update the current player index to the next valid player
            currentPlayerNum = self.listOfPlayers.index(plyr)
            currentPlayerNum = (currentPlayerNum + 1) % len(self.listOfPlayers)
            self.currentPlayer = self.listOfPlayers[currentPlayerNum]


            # Re-render the game board to update the highlighting effect
            self.drawUpdatedGameBoard()
    
    
    
    def printUpdatedPlayerInformation(self):
        for p in self.listOfPlayers:
            print("Player " + str(p.gameBoardSymbol) + " has " + str(p.getPoints()) + " points and has " + str(p.energy) + " energy")
      
    
    def drawUpdatedGameBoard(self) :     
        # loop through each game board space and either print the gameboard symbol
        # for what is located there or print a dot to represent nothing is there
        for y in range(0,self.gameBoardHeight):
            for x in range(0,self.gameBoardWidth):
                symbolToPrint = "."
                for treasure in self.listOfTreasures:
                   if treasure.x == x and treasure.y == y:
                      symbolToPrint = treasure.gameBoardSymbol
                for player in self.listOfPlayers:
                   if player.x == x and player.y == y:
                      symbolToPrint = player.gameBoardSymbol
                for weapon in self.listOfWeapons:
                  if weapon.x == x and weapon.y == y:
                      symbolToPrint = weapon.gameBoardSymbol
                print(symbolToPrint,end="")
            print() # go to next row
        print()
       
  
    def printInstructions(self) :
        print("Players move around the game board collecting treasures worth points")
        print("The game ends when all treasures have been collected or only 1 player is left")
        print("Here are the point values of all of the treasures:")
        for treasure in self.listOfTreasures :
            print( "   " + treasure.name + "(" + treasure.gameBoardSymbol + ") " + str(treasure.pointValue) )
        print()


    def end_game(self):
        if len(self.listOfPlayers) == 1:
            winner = self.listOfPlayers[0]
            print(f"Player {winner.gameBoardSymbol} wins with {winner.getPoints()} points!")
            return winner
        else:
            highest = 0
            for i in range(len(self.listOfPlayers)):
                if self.listOfPlayers[i].getPoints() > self.listOfPlayers[highest].getPoints():
                    highest = i
            winner = self.listOfPlayers[highest]
            print(f"Player {winner.gameBoardSymbol} wins with {winner.getPoints()} points!")
            return winner