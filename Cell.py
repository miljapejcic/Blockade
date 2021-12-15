from Player import Player


from Player import *

class Cell: 
    
    def __init__(self, player: Player ,rightWall: bool, bottomWall: bool):
        '''Player or empty place, right wall or no wall, bottom wall or no wall'''
        self.player = player
        self.rightWall = rightWall
        self.bottomWall = bottomWall

    def hasPlayer(self) -> bool:
        return self.player != None

    
