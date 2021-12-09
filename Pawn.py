from typing import List


class Pawn:

    def __init__(self, positions: List[int]):
        self.x = positions[0]
        self.y = positions[1]

    def setPositions(self, x: int, y: int): 
        '''Setting x and y positions for a pawn'''
        self.x = x
        self.y = y
    
    def checkEnd(self, position1: List[int],position2: List[int]):
        if (self.x == position1[0] and self.y == position1[1]) or (self.x == position2[0] and self.y == position2[1]) :
            return True
        else:
            return False