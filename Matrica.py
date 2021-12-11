from typing import List
from Cell import *
from Player import *
from Pawn import *
class Matrica: 
    
    '''Za pomeranje levo-desno se menja y koordinata
       Za pomeranje gore-dole se menja x koordinata'''

    def __init__(self, dimX: int, dimY: 
                int, x1: List[int], x2: List[int],
                o1: List[int], o2: List[int]):
        ''' dimX - broj vrsta matrice
            dimY - broj kolona matrice
            x1 - starting positions for pawn1 of playerX (x,y)
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
        self.mat = self.__make_matrix__()
        

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
            for j in range(0,self.dimY):  
                if self.checkGoal(i, j) != ' ' and not self.mat[i][j].hasPlayer():
                    print(self.checkGoal(i,j), end="")
                elif self.mat[i][j].hasPlayer():
                   print(self.mat[i][j].player.sign , end="")
                else:
                    print(" ", end="")
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

    def checkGoal(self, i: int, j: int):
        if (i == self.startPosO1[0] and j == self.startPosO1[1]) or (i == self.startPosO2[0] and j == self.startPosO2[1]):
            return 'o'
        elif (i == self.startPosX1[0] and j == self.startPosX1[1]) or (i == self.startPosX2[0] and j == self.startPosX2[1]):
            return 'x'
        else:
            return ' '
         

    #NOT IMPLEMENTED!!!!! 
    def changeStateWithWalls(self, player: Player, pawnNo: int, pawnPositions: List[int],
                                 wallType: int, wallPositions: List[int]) -> bool:
        '''Promena stanja igre ako validnost uspe, ako ne vratiti false'''

        validMove = self.validateMove(player.getPawn(pawnNo), pawnPositions)
        validWall = self.validateWall(wallType, wallPositions)

        if validMove and validWall:
            return self.movePawn(player, pawnNo,pawnPositions) and self.PutWall(player, wallType, wallPositions)
        else:
            return False;
        
    def changeStateWithoutWalls(self, player: Player, pawnNo: int, pawnPositions: List[int]) -> bool:
        '''Promena stanja igre ako validnost uspe, ako ne vratiti false'''

        if self.validateMove(player.getPawn(pawnNo), pawnPositions):
            return self.movePawn(player, pawnNo,pawnPositions)
        else:
            return False;


    def validateMove(self, pawn: Pawn, pawnPosition: List[int]) ->bool :
        nX=pawnPosition[0] #nove koord
        nY=pawnPosition[1]
        sX=pawn.x
        sY=pawn.y
        if nX < 0 or nX > self.dimX:
            return False
        if nY < 0 or nY > self.dimY:
            return False
        
        #Condition 2 - are sum of distances between x and y coordinate greater than 3? 
        if (abs(pawn.x - nX) + abs(pawn.y - nY)) > 2: 
            return False
        
        if self.mat[nX][nY].player != None:
            return False
        #gore
        if nX-sX==2 and nY==sY :
            if self.mat[sX-1][sY].bottomWall==True or self.mat[sX-2][sY].bottomWall==True:
                return False
                #gore za 1
        if nX-sX==1 and nY==sY :
            if self.mat[sX-1][sY].bottomWall==True or self.mat[sX-2][sY].bottomWall==True:
                return False
            if self.mat[sX-2][sY].player==None:
                return False
        #dole
        if sX-nX==2 and nY==sY:
            if self.mat[sX][sY].bottomWall==True or self.mat[sX+1][sY].bottomWall==True:
                return False
            #dole za 1
        if sX-nX==1 and nY==sY:
            if self.mat[sX][sY].bottomWall==True or self.mat[sX+1][sY].bottomWall==True:
                return False
            if self.mat[sX+2][sY].player==None:
                return False
        #desno
        if nY-sY==2 and nX==sX:
            if self.mat[sX][sY].rightWall==True or self.mat[sX][sY+1].rightWall==True:
                return False
            #desno za 1
        if nY-sY==1 and nX==sX:
            if self.mat[sX][sY].rightWall==True or self.mat[sX][sY+1].rightWall==True:
                return False
            if self.mat[sX][sY+2].player==None:
                return False
        #levo
        if sY-nY==2 and nX==sX:
            if self.mat[sX][sY-1].rightWall==True or self.mat[sX][sY-2].rightWall==True:
                return False
            #levo za 1
        if sY-nY==1 and nX==sX:
            if self.mat[sX][sY-1].rightWall==True or self.mat[sX][sY-2].rightWall==True:
                return False
            if self.mat[sX][sY-1].player==None:
                return False
        #dij levo gore
        if nX==sX-1 and nY==sY-1 :
            if self.mat[sX][sY+1].bottomWall==True and self.mat[nX][nY].bottomWall==True:
                return False
            elif self.mat[sX][sY-1].rightWall==True and self.mat[sX-1][sY-1].rightWall==True:
                return False
        #dij levo dole
        if nX==sX+1 and nY==sY-1:
            if self.mat[sX][sY].bottomWall==True and self.mat[sX][sY-1].bottomWall==True:
                return False
            elif self.mat[sX][sY-1].rightWall==True and self.mat[sX+1][sY-1].rightWall==True:
                return False
        #dij desno gore
        if nX==sX-1 and nY==sY+1:
            if self.mat[sX][sY].rightWall==True and self.mat[sX-1][sY].rightWall==True:
                return False
            if self.mat[sX][sY].bottomWall==True and self.mat[sX-1][sY+1].bottomWall==True:
                return False
        #dij desno dole
        if nX==sX+1 and nY==sY+1:
            if self.mat[sX][sY].rightWall==True and self.mat[sX+1][sY].rightWall==True:
                return False
            if self.mat[sX][sY].bottomWall==True and self.mat[sX][sY+1].bottomWall==True:
                return False

        return True

    def validateWall(self, wallType: int,wallPositions: List[int]) -> bool:
        '''WallType == 0 horizontal walls
           WallType == 1 vertical walls
        '''
        zX=wallPositions[0]
        zY=wallPositions[1]

        if wallType ==0:
            #zid izvan tabele  
            if(zX>self.dimX and zY>self.dimY) or (zX>self.dimX and zY+1>self.dimY):
                return False
            #horizontalni zid da li se poklapa sa drugim
            if self.mat[zX][zY].bottomWall==True or self.mat[zX][zY+1].bottomWall==True:
                return False 
        else:
            #zid izvan tabele    
            if (zX>self.dimX and zY>self.dimY) or (zX+1>self.dimX and zY>self.dimY):
                return False
            #vertikalni zid da li se poklapa sa drugim
            if self.mat[zX][zY].rightWall==True or self.mat[zX+1][zY].rightWall==True:
                return False
        
        return True



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
        return True
    
    def PutWall(self, player: Player, wallType: int,wallPositions: List[int]) -> bool:
        '''WallType == 0 horizontal walls
           WallType == 1 vertical walls
           Validnost je vec okej'''
        if wallType not in [0,1]:
            return False
        x = wallPositions[0]
        y = wallPositions[1]
        if wallType == 0: 
            self.mat[x][y].bottomWall = True
            self.mat[x][y+1].bottomWall = True
            player.horWallNum = player.horWallNum - 1
            return True
        else:
            self.mat[x][y].rightWall = True
            self.mat[x+1][y].rightWall = True
            player.vertWallNum = player.vertWallNum - 1
            return True

    def isEndOfGame(self, player: Player) -> bool:
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

#provera da li nam rade validacije i kod iz matrice 
mat = Matrica(10,11,[3,3],[4,4],[8,8],[9,9])
walls = 5
playerX = Player('X',walls)
playerO = Player('O',walls)
playerX.AddPawns(Pawn([3,3]),Pawn([4,4]))
playerO.AddPawns(Pawn([8,8]),Pawn([9,9]))
mat.addPlayers(playerX,playerO)
print("Prikaz matrice nakon inicijalizacije")
mat.printBoard()
if mat.changeStateWithWalls(playerX,1,[1,3],0,[4,5]):
# mat.movePawn(playerX,1,[1,3])
# mat.PutWall(playerX,0,[4,5])
    print("PlayerX pomerio pesaka na [1,3] i postavio horizontalni zid na [4,5]")
else : 
    print("PlayerX izabrao lose polje za pesaka ili za zid")

print("Nakon promene stanja na tabli")
mat.printBoard()

if mat.changeStateWithWalls(playerO,1,[1,3],0,[4,5]):
# mat.movePawn(playerX,1,[1,3])
# mat.PutWall(playerX,0,[4,5])
    print("PlayerX pomerio pesaka na [1,3] i postavio horizontalni zid na [4,5]")
else : 
    print("PlayerX izabrao lose polje za pesaka ili za zid")

print("Nakon promene stanja na tabli")
mat.printBoard()

