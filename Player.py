from Pawn import *
class Player: 
    def __init__(self, sign: str, vertWallNum: int, horWallNum: int) :
        self.vertWallNum = vertWallNum
        self.horWallNum = horWallNum
        self.pawn1 = None
        self.pawn2 = None
        self.sign = sign

    def AddPawns(self, pawn1: Pawn, pawn2: Pawn) -> bool:
        '''Setting pawns for player. Player must have two pawns '''

        if pawn1 == None or pawn2 == None:
            return False
        self.pawn1 = pawn1
        self.pawn2 = pawn2
        return True
    
    def hasWalls(self, wallType: int) -> bool:
        '''WallType == 1 horizontal walls
           walltype == 2 vertical walls'''
        if wallType == 1 and self.horWallNum != 0:
            return True
        if wallType == 2 and self.vertWallNum != 0:
            return True
        return False

   

    def getPawn(self, pawnNo: int) -> Pawn:
        if pawnNo == 1:
            return self.pawn1
        else:
            return self.pawn2

    def movePawn(self, pawnNo: int, x: int, y: int):
        if pawnNo == 1:
            self.pawn1.x = x
            self.pawn1.y = y 
        else :
            self.pawn2.x = x
            self.pawn2.y = y
