class Weapon:
  def __init__(self,name,locationx,locationy,gameboardsymb,strikedistance):
    self.name = name
    self.x = locationx
    self.y = locationy
    self.gameBoardSymbol = gameboardsymb
    self.strikedistance = int(strikedistance)