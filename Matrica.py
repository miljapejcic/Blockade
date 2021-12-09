from typing import List
from Cell import *
from Player import *
from Pawn import *
class Matrica: 
    
    def __init__(self, dimX: int, dimY: 
                int, x1: List[int], x2: List[int],
                o1: List[int], o2: List[int]):
        ''' x1 - starting positions for pawn1 of playerX (x,y)
            x2 - starting positions for pawn2 of playerX (x,y)
            o1 - starting positions for pawn1 of playerO (x,y)
            o1 - starting positions for pawn2 of playerO (x,y)'''

        self.dimX = dimX
        self.dimY = dimY
        self.playerX = None
        self.playerO = None
        self.startPosX1 = x1
        self.startPosX2 = x2
        self.startPosO1 = o1
        self.startPosO2 = o2
        self.mat = self.__make_matrix__() #radi li ?? 
        

    def __make_matrix__(self):
        '''Kreiranje matrice'''
        self.mat = [[ Cell(None,False,False) for i in range(0,self.dimY)] for j in range (0,self.dimX)]
        for i in range(0,self.dimY):
            self.mat[self.dimX - 1][i].bottomWall = True #postvljanje donjeg zide zadnjeg reda na konstatan zid
        for i in range(0,self.dimX): 
            self.mat[i][self.dimY - 1].rightWall = True #postvljanje desnog zide zadnje kolone na konstatan zid
        return self.mat
   
    def addPlayers(self,playerX: Player, playerO: Player):
        self.playerX = playerX
        self.playerO = playerO

        #postavljanje na tabli
        self.mat[playerX.pawn1.x][playerX.pawn1.y].player = playerX
        self.mat[playerX.pawn2.x][playerX.pawn2.y].player = playerX

        self.mat[playerO.pawn1.x][playerO.pawn1.y].player = playerO
        self.mat[playerO.pawn2.x][playerO.pawn2.y].player = playerO


    

    #NOT IMPLEMENTED!!!!! 
    def isValidMove(self, player: Player, x: int, y: int) -> bool:
        '''Validating move for current player to the positions x and y'''
        #     if x < 0 or y < 0:
        #         return False
        print("NOT IMPLEMENTED")

    #NOT IMPLEMENTED!!!!! 
    def __isValidMoveForPawn__(self, pawn: Pawn, x: int, y: int):
        '''Validating move for current pawn'''
        #     if x < 0 or y < 0: 
        #         return False
        #     if abs(pawn.x - x) == 1 and abs(pawn.y - y) == 1:
        #         return True #move one step diagonally
        print("NOT IMPLEMENTED")
        
    def printBoard(self):
        #needs refactoring
        '''Printing current state on the board'''
        print(" ", end="")
        for i in range(0,self.dimY):
            print(" {}".format(hex(i)[2:]), end="")
        print("\n", end=" ")
        for i in range(0,self.dimY):
            print(" =", end="")
        print("\n", end="")
        for i in range(0,self.dimX):
            print(f'{hex(i)[2:]}{chr(0x01C1)}', end="")
            # print("{} {}".format(chr(0x01C1)), end="")
            for j in range(0,self.dimY):
                #if i,j neki od startnih pozicija ? "S"
                if self.mat[i][j].hasPlayer():
                    print(" ", end="")
                else:
                    print(self.mat[i][j].player.sign , end="") #overwrite "S"
                if self.mat[i][j].rightWall == False:
                    print("|", end="")
                else:
                    print(chr(0x01C1), end="")
            print('\n', end="  ")
            for j in range(0, self.dimY):
                if self.mat[i][j].bottomWall == False:
                    print("-", end=" ")
                else:
                    print("=", end=" ")
            print("\n", end="")

    #NOT IMPLEMENTED!!!!! 
    def changeStateIfPossible(self, player: Player, pawnNo: int, pawnPositions: List[int],
                                 wallType: int, wallPosition: List[int]) -> bool:
        '''Promena stanja igre ako validnost uspe, ako ne vratiti false'''
        #valid funkcija za igraca
        #valid funkcija za zid
        #return false ako ne moze
        
        #movePawn
        self.movePawn(player, pawnNo,pawnPositions)
        if  player.hasWalls(wallType):
            self.PutWall(player, wallType, wallPosition)
        print("NOT IMPLEMENTED")

   
    def movePawn(self, player: Player ,pawnNo: int, pawnPositions: List[int]) -> bool:
        '''Pomeranje igraca na x,y celiji u matrici
           pawnNo == 1 => pawn1 
           pawnNo == 2 => pawn2
           Validnost je vec okej'''

        x = pawnPositions[0]
        y = pawnPositions[1]
        if player == None or pawnNo not in [1,2]:
            return False
        pawn = player.getPawn(pawnNo)
        self.mat[pawn.x][pawn.y].player = None #brisanje sa stare lokacije
        player.movePawn(pawnNo, x, y) #pomeranje pijuna u player 
        self.mat[x][y].player = player #nova pozicija

    def PutWall(self, player: Player, wallType: int,wallPositions: List[int]) -> bool:
        '''WallType == 0 horizontal walls
           WallType == 1 vertical walls
           Validnost je vec okej'''

        x = wallPositions[0]
        y = wallPositions[1]
        if wallType == 0: 
            self.mat[x][y].bottomWall = True
            self.mat[x][y+1].bottomWall = True
            player.horWallNum = player.horWallNum - 1
        else:
            self.mat[x][y].rightWall = True
            self.mat[x+1][y].rightWall = True
            player.vertWallNum = player.vertWallNum - 1

    def isEndOfGame(self, player: Player):
        if player.sign == "X":
            if player.pawn1.checkEnd(self.startPosO1, self.startPos02) or player.pawn2.checkEnd(self.startPosO1, self.startPosO2):
                return True
            else:
                return False
        elif player.sign == "O":
            if player.pawn1.checkEnd(self.startPosX1, self.startPosX2) or player.pawn2.checkEnd(self.startPosX1, self.startPosX2):
                return True
            else:
                return False

mat = Matrica(10,11,[3,3],[4,4],[8,8],[9,9])
playerX = Player('X',5,5)
playerO = Player('O',5,5)
playerX.AddPawns(Pawn([3,3]),Pawn([4,4]))
playerO.AddPawns(Pawn([8,8]),Pawn([9,9]))
mat.addPlayers(playerX,playerO)
print("Prikaz matrice nakon inicijalizacije")
mat.printBoard()
mat.movePawn(playerX,1,[1,3])
mat.PutWall(playerX,0,[4,5])
print("PlayerX pomerio pesaka na [1,3]")
mat.printBoard()

