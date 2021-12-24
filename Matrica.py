from copy import deepcopy
from typing import ContextManager, List
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
   
    def getCopy(self) : 
        pass
    def addPlayers(self,playerX: Player, playerO: Player):
        self.playerX = playerX
        self.playerO = playerO

        #postavljanje na tabli
        self.mat[playerX.pawn1.x][playerX.pawn1.y].player = playerX
        self.mat[playerX.pawn2.x][playerX.pawn2.y].player = playerX

        self.mat[playerO.pawn1.x][playerO.pawn1.y].player = playerO
        self.mat[playerO.pawn2.x][playerO.pawn2.y].player = playerO


        
    def printBoard(self):
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
         

    def changeStateWithWalls(self, player: Player, pawnNo: int, xDir: int, yDir: int, wallType: int, wallPositions: List[int]) -> bool:
        '''Promena stanja igre ako validnost uspe, ako ne vratiti false'''

        validMove = self.validateMove(player,pawnNo,xDir,yDir)
        validWall = self.validateWall(wallType, wallPositions)
        validString  = "invalid move" if not validMove else "invalid wall" 
        if validMove and validWall:
            pawn = player.getPawn(pawnNo)
            return self.movePawn(player, pawnNo, [pawn.x + xDir, pawn.y + yDir]) and self.PutWall(player, wallType, wallPositions)
        else:
            print(validString)
            return False
        
    def changeStateWithoutWalls(self, player: Player, pawnNo: int, xDir: int, yDir: int) -> bool:
        '''Promena stanja igre ako validnost uspe, ako ne vratiti false'''

        if self.validateMove(player,pawnNo,xDir,yDir):
            pawn = player.getPawn(pawnNo)
            return self.movePawn(player, pawnNo,[pawn.x + xDir, pawn.y + yDir])
        else:
            return False



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
            if player.pawn1.checkEnd(self.startPosO1, self.startPosO2) or player.pawn2.checkEnd(self.startPosO1, self.startPosO2):
                return True
            else:
                return False
        elif player.sign == "O":
            if player.pawn1.checkEnd(self.startPosX1, self.startPosX2) or player.pawn2.checkEnd(self.startPosX1, self.startPosX2):
                return True
            else:
                return False

    def validateMove(self, player: Player, pawnNo: int, xDir: int, yDir: int) -> bool: 
        '''xDir moving in x-dimension (rows) (-2,-1,0,+1,+2)
           yDir moving in y-dimension (columns) (-2,-1,0,+1,+2)'''
           
        #are sum of distances between x and y coordinate greater than 3? 
        totalSteps = abs(xDir) + abs(yDir)
        if  totalSteps > 2 or totalSteps == 0:
            return False
        pawn = player.getPawn(pawnNo)
        #is move out of range? 
        if self.isOutOfRange(pawn.getPositions(),xDir,yDir):
            return False

        #pomeranje dva polja po jednoj dimenziji ili jedno polje dijagonalno
        if abs(xDir) == abs(yDir) : #pomeranje dijagonalno
            canPass = self.validateDiagonalMove(player,pawn.getPositions(),xDir,yDir)
            canJump = self.canJump(player,pawn.x + xDir, pawn.y + yDir)
            return canPass == True and canJump == True  
        else: #pomeranje po jednoj osi 
            if totalSteps == 1:
                canPass2 = self.validateNormalMove(player,pawn.getPositions(),xDir,yDir,2)
                canPass1 = self.validateNormalMove(player,pawn.getPositions(),xDir,yDir, 1)
                canJump2 = self.canJump(player,pawn.x + 2*xDir, pawn.y + 2*yDir)
                if canPass2 == True and canPass1 == True :
                    return True if canJump2 == False else False
                return False                
                
            canPass = self.validateNormalMove(player,pawn.getPositions(),xDir,yDir,totalSteps)
            canJump = self.canJump(player,pawn.x + xDir, pawn.y + yDir)
            return canPass == True and canJump == True

    
    def validateNormalMove(self,player: Player, pawnPositions: List[int],xDir: int, yDir: int, totalSteps: int) -> bool: 
        '''For validating moving in one direction one or two steps'''
        pawn = Pawn(pawnPositions)
        step = 0
        if xDir != 0: 
            step = int(xDir / 2) if totalSteps > 1 else xDir # po X 
        else: #yDir != 0
            step = int(yDir / 2)  if totalSteps > 1 else yDir # po Y
        oldPawn = pawn.getCopy() 
        nextPawn = pawn.getCopy() 
        wallsBetween = False
        for i in range(0,totalSteps):
            if xDir != 0: 
                nextPawn.x = oldPawn.x + step
                wallsBetween = self.areWallsBetwween(oldPawn,nextPawn,step,0)
            else: #yDir != 0
                nextPawn.y = oldPawn.y + step
                wallsBetween = self.areWallsBetwween(oldPawn,nextPawn,0,step)
            if wallsBetween:
                return False #vraca false, i na prvi i na drugi zid da naidje
            oldPawn.x = nextPawn.x
            oldPawn.y = nextPawn.y
        return True
        

    def canJump(self,player: Player, x: int, y: int) -> bool:
        sign = player.sign.lower()
        cellSign = self.checkGoal(x,y)

        if self.mat[x][y].player == None: #free position
            return True
        else: #some pawn is on that position
            if cellSign in ['x','o']: #goal position
                if sign != cellSign: #enemy on that position
                    return True #can jump 
                else: 
                    return False #my pawn on that position
            return False #cannot jump 

    def validateDiagonalMove(self, player: Player, pawnPositions: List[int], xDir: int, yDir: int) -> bool:
        '''xDir, yDir can be +1,-1'''
        pawn = Pawn(pawnPositions)
        #prvi pristup, prvo menjamo x pa y
        wallsBetween = False
        tmpPawn = Pawn([pawn.x + xDir, pawn.y])
        wallsBetween_X = self.areWallsBetwween(pawn, tmpPawn,xDir,0)
        

        tmpPawn.y = tmpPawn.y + yDir
        wallsBetween_Y = self.areWallsBetwween(pawn, tmpPawn,0,yDir)
        
        if wallsBetween_X == False and wallsBetween_Y == False: 
            return True
            # return self.canJump(player,pawn.x + xDir, pawn.y + yDir)


        #drugi pristup, prvo menjamo y pa x
        tmpPawn = Pawn([pawn.x, pawn.y + yDir])
        wallsBetween_X = self.areWallsBetwween(pawn, tmpPawn,0,yDir)
       

        tmpPawn.y = tmpPawn.x + xDir
        wallsBetween_Y = self.areWallsBetwween(pawn, tmpPawn,xDir,0)

        if wallsBetween_X == False and wallsBetween_Y == False:
            #provera jel slobodno polje 
            return True
            # return self.canJump(player,pawn.x + xDir, pawn.y + yDir)
        return False


    #ovo je neki komentar
    def areWallsBetwween(self, currentPawn: Pawn, nextPawn: Pawn, xDir: int, yDir: int) -> bool:
        '''Checking if there is wall between two adjacent cells
           Up: xDir == -1, yDir == 0
           Down: xDir == 1, yDir == 0
           Left: xDir == 0, yDir == -1
           Right: xDir == 0, yDir == 1'''

        if xDir != 0:
            if xDir == 1:
                return self.mat[currentPawn.x][currentPawn.y].bottomWall 
            else: #xDir == -1
                return self.mat[nextPawn.x][nextPawn.y].bottomWall 
        
        else: #yDir != 0
            if yDir == 1: 
                return self.mat[currentPawn.x][currentPawn.y].rightWall 
            else: #yDir == -1
                return self.mat[nextPawn.x][nextPawn.y].rightWall 
                

    def isOutOfRange(self, pawnPositions: List[int], xDir: int, yDir: int) -> bool:
        '''Checking if move is out of board'''
        x = pawnPositions[0]
        y = pawnPositions[1]
        if x + xDir >= self.dimX or x + xDir < 0:
            return True
        if y + yDir >= self.dimY or y + yDir < 0:
            return True
        return False

    def clone(self):
        return deepcopy(self)