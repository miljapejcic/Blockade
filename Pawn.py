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
    def getCopy(self):
        '''Copy constructor'''
        pawn = Pawn([self.x, self.y])
        return pawn
    
    def getPositions(self) -> List[int]:
        return [self.x,self.y]
    def getMoves(self) -> List[List[int]]:
        moves = []
        for i in range(self.x-1,self.x+2):
            for j in range(self.y-1, self.y+2):
                if not (self.x==i and self.y==j):
                    moves.append([i,j])
        nizX  = [-2,2,0,0]
        nizY = [0,0,-2,2]
        for i in range(0,4):
           moves.append([self.x + nizX[i],self.y + nizY[i]])
        return moves
    
    def clone(self): 
        pawn = Pawn(self.getPositions())
        return pawn