from typing import List


class Pawn:

    def __init__(self, positions: List[int]):
        self.x = positions[0]
        self.y = positions[1]

    def setPositions(self, x: int, y: int): 
        '''Setting x and y positions for a pawn'''
        self.x = x
        self.y = y
    