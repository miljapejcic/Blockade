import copy
from typing import List, Tuple
from Cell import *
from Player import *
from Pawn import *
from functools import reduce
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
        self.mat = None


    def clone(self):
        klon = Matrica(self.dimX, self.dimY,self.startPosX1,self.startPosX2,self.startPosO1,self.startPosO2)
        klon.mat = []
        for i in range(0,klon.dimX):
            klon.mat.append([])
            for j in range(0,klon.dimY):
                klon.mat[i].append(self.mat[i][j].clone())
        
        klon.addPlayers(self.playerX.clone(),self.playerO.clone())
        return klon
        # return copy.deepcopy(self)

    def makeMatrix(self):
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
        self.mat[playerX.pawn1.x][playerX.pawn1.y].player = self.playerX
        self.mat[playerX.pawn2.x][playerX.pawn2.y].player = self.playerX

        self.mat[playerO.pawn1.x][playerO.pawn1.y].player = self.playerO
        self.mat[playerO.pawn2.x][playerO.pawn2.y].player = self.playerO


        
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
            return self.PutWall(player, wallType, wallPositions) and self.movePawn(player, pawnNo, [pawn.x + xDir, pawn.y + yDir])
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
    def calcHeuristic(self,start: List[int], end: List[int]) -> int:
        '''Manhatan heuristika, suma, abs, cilj - start'''
        result = 0
        for i in [0,1]:
            result += abs(end[i] - start[i])
        return result


    

    def A_star(self, player:Player, pawnNo: int, end: List[int]) -> List:
        '''Returns path as a list of tuples if there is one, otherwise returns empty list'''
        #init
        # self.printBoard()
        pawn = player.getPawn(pawnNo)
        start = pawn.getPositions()
        path = []
        startTup = tuple(start)
        endTup = tuple(end)

        if start == end:
            path.append(endTup)
            path.append(startTup)
            return path
        found_node = False
        openList = dict()
        closedList = []
        prev_nodes = dict()
        g = dict() #udaljenosti od starta 
        g[startTup] = 0 
        prev_nodes[startTup] = None
        f = 0 + self.calcHeuristic(start,end) #funkcija evaluacije f = g + h
        openList[startTup] = f
        while len(openList) > 0 and not found_node:
            minEl = min(openList.items(), key= lambda x: x[1])
            nodeTup = minEl[0] #tuple
            openList.pop(nodeTup)
            
            if nodeTup == endTup:
                found_node = True
                break
            #potrebni zbog parametara funkcije samo 
            playerTmp = Player(player.sign,0)
            pawnTmp = Pawn(nodeTup)
            playerTmp.pawn1 = pawnTmp
            moves = pawnTmp.getMoves()
            for move in moves: 
                moveTmp = list(move)
                moveTup = tuple(move)
                moveTmp[0] -= pawnTmp.x #dirX 
                moveTmp[1] -= pawnTmp.y #dirY
                if self.validateMove(playerTmp,1,moveTmp[0],moveTmp[1]):
                    steps =  sum(list(map(lambda x: abs(x),moveTmp)))
                    distance = g[nodeTup] + steps
                    heur = self.calcHeuristic(move,end)
                    f = distance + heur
                    
                    #odigrane poteze preskace u ovom ifu 
                    if  moveTup not in openList.keys() and moveTup not in closedList: #nikad nije obidjen 
                        openList[moveTup] = f
                        prev_nodes[moveTup] = nodeTup
                        g[moveTup] = distance

                    elif moveTup in openList.keys(): #mozda je vec dodat u niz
                        #proveravamo distance
                        if g[moveTup] > distance:
                            #nova vrednost je bolja vrednost
                            g[moveTup] = distance
                            prev_nodes[moveTup] = nodeTup
                            nadjen = list(filter(lambda x: x == moveTup, openList.keys()))
                            openList.pop(nadjen[0])
                            openList[nadjen[0]] = f + distance
            closedList.append(nodeTup)
        if found_node:
            tmpTup = endTup
            while (tmpTup is not None): 
                path.append(tmpTup)
                tmpTup = prev_nodes[tmpTup]
            
            return path
        return path

    def isBlocking(self):
        '''Returns True if there is no path, False if there is path'''
        path = self.A_star(self.playerX,1,self.startPosO1)
        if len(path) == 0:
            return True
        path = self.A_star(self.playerX,1,self.startPosO2)
        if len(path) == 0:
            return True
        path = self.A_star(self.playerX,2,self.startPosO1)
        if len(path) == 0:
            return True
        path = self.A_star(self.playerX,2,self.startPosO2)
        if len(path) == 0:
            return True
        path = self.A_star(self.playerO,1,self.startPosX1)
        if len(path) == 0:
            return True
        path = self.A_star(self.playerO,1,self.startPosX2)
        if len(path) == 0:
            return True
        path = self.A_star(self.playerO,2,self.startPosX1)
        if len(path) == 0:
            return True
        path = self.A_star(self.playerO,2,self.startPosX2)
        if len(path) == 0:
            return True
        return False
    

    def validateWall(self, wallType: int,wallPositions: List[int]) -> bool:
        '''WallType == 0 horizontal walls
           WallType == 1 vertical walls
        '''
        zX=wallPositions[0]
        zY=wallPositions[1]

        if wallType ==0:
            #zid izvan tabele  
            if(zX>=self.dimX or zY>=self.dimY or zY+1>=self.dimY or zX<0 or zY<0):
                return False
            #horizontalni zid da li se poklapa sa drugim
            if self.mat[zX][zY].bottomWall==True or self.mat[zX][zY+1].bottomWall==True:
                return False 
        else:
            #zid izvan tabele    
            if (zX>=self.dimX or zY>=self.dimY or zX+1>=self.dimX  or zX<0 or zY<0):
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
        if player.sign == 'X':
            self.playerX.movePawn(pawnNo,x,y)
        else:
            self.playerO.movePawn(pawnNo,x,y)

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
            if self.isBlocking():
                self.mat[x][y].bottomWall = False
                self.mat[x][y+1].bottomWall = False
                player.horWallNum = player.horWallNum + 1
                # print("ne smete da blokirate ciljeve ili pesake")
                return False
            return True
        else:
            self.mat[x][y].rightWall = True
            self.mat[x+1][y].rightWall = True
            player.vertWallNum = player.vertWallNum - 1
            if  self.isBlocking():
                self.mat[x][y].rightWall = False
                self.mat[x+1][y].rightWall = False
                player.vertWallNum = player.vertWallNum + 1
                # print("ne smete da blokirate ciljeve ili pesake")
                return False
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

                #slucaj da ne moze da prodje
                canPass1 = self.validateNormalMove(player,pawn.getPositions(),xDir,yDir, 1)
                if canPass1 == False:
                    return False

                #slucaj da je birana pozicija cilj, ne gleda se da li ima pesaka ili nema i da li ima zida na canpass2 i da li moze da skoci na canjump2
                goalPos = self.isGoalPosition(player.sign,self.checkGoal(pawn.x + xDir, pawn.y + yDir))
                if goalPos:
                    return True
                
                canPass2 = False #default-ne vrednosti
                canJump2 = False  #default-ne vrednosti
           
                if not self.isOutOfRange(pawn.getPositions(),2*xDir,2*yDir):
                    canPass2 = self.validateNormalMove(player,pawn.getPositions(),xDir,yDir,2)
                    canJump2 = self.canJump(player,pawn.x + 2*xDir, pawn.y + 2*yDir)

                #ovaj uslov je jedini od svih mogucih koji dopusta skakanje, samo da canJump to dozvoli 
                if canPass2 == True and canJump2 == False:
                    return self.canJump(player,pawn.x + xDir, pawn.y + yDir)
                return False
      
                               
            #total steps = 2   
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
            return self.isGoalPosition(sign,cellSign)
            # if cellSign in ['x','o']: #goal position
            #     if sign != cellSign: #enemy on that position
            #         return True #can jump 
            #     else: 
            #         return False #my pawn on that position
            # return False #cannot jump 

    def isGoalPosition(self, playerSign: str, cellSign: str)-> bool:
        # sign = player.sign.lower()
        # cellSign = self.checkGoal(x,y)
        if cellSign in ['x','o']: #goal position
            if playerSign != cellSign: #enemy on that position
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
        
        pawn = Pawn(tmpPawn.getPositions())
        tmpPawn.y = tmpPawn.y + yDir
        wallsBetween_Y = self.areWallsBetwween(pawn, tmpPawn,0,yDir)
        
        if wallsBetween_X == False and wallsBetween_Y == False: 
            return True
            # return self.canJump(player,pawn.x + xDir, pawn.y + yDir)


        #drugi pristup, prvo menjamo y pa x
        pawn = Pawn(pawnPositions)
        tmpPawn = Pawn([pawn.x, pawn.y + yDir])
        wallsBetween_Y = self.areWallsBetwween(pawn, tmpPawn,0,yDir)
       
        pawn = Pawn(tmpPawn.getPositions())
        tmpPawn.x = tmpPawn.x + xDir
        wallsBetween_X = self.areWallsBetwween(pawn, tmpPawn,xDir,0)

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

    
    