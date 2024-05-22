class Player :

    # the constructor (initialize all Player variables)
    def __init__(self, initialX, initialY, symb) :     
        self.x = initialX
        self.y = initialY
        self.energy = 8.0
        self.collectedTreasures = []
        self.collectedWeapons = []
        self.gameBoardSymbol = symb
    
    
    def getPoints(self):
        totalPoints = 0
        for i in self.collectedTreasures:
          totalPoints += i.pointValue
        return totalPoints
    
    def dist(pt1,pt2):
     return ((pt1.x-pt2.x)**2 + (pt1.y-pt2.y)**2)**.5
  
    def collectTreasure(self, treasureItem):
        self.collectedTreasures.append(treasureItem)
        
    
    def collectWeapon(self, weaponItem):
        self.collectedWeapons.append(weaponItem)
        
      
    
    def move(self, direction, distanceToMove):
        if direction == "r":
            if self.energy * 2 < distanceToMove:
              distanceToMove = self.energy * 2
              
                
            self.x = self.x + distanceToMove
            self.energy -= 0.5 * distanceToMove
        elif direction == "l":
            if self.energy * 2 < distanceToMove:
              distanceToMove = self.energy * 2
            self.x = self.x - distanceToMove
            self.energy -= 0.5 * distanceToMove
        elif direction == "u":
            if self.energy * 2 < distanceToMove:
              distanceToMove = self.energy * 2
            self.y = self.y - distanceToMove
            self.energy -= 0.5 * distanceToMove
        elif direction == "d":
            if self.energy * 2 < distanceToMove:
              distanceToMove = self.energy * 2
            self.y = self.y + distanceToMove
            self.energy -= 0.5 * distanceToMove
        else:
            print("That is not a valid direction")