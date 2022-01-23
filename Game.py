from cmath import exp
from ctypes import sizeof
from threading import Timer
from typing import Set
from winsound import PlaySound
from zlib import DEF_BUF_SIZE
from Matrica import * 
import itertools
import time
class Game: 

    def __init__(self) :
        self.matrica = None
        self.onTurn = 'X'
        self.players = { 
            'X' : None,
            'O' : None
        }
        #Mozda treba da obelezimo ko ce da bude PC a ko covek
        #Ili ove ili unutar player-a kao atribut 
        #self.Computer = 'X' or 'Y', kada se izabere ko igra prvi
        self.temp = None
    
    def matrixInit(self): 
        '''Creating matrix: dimensions and starting positions for pawns
           Starting positions for pawns are target for other player's pawns'''
        #dimenzije
        dimX = int(input("Uneti broj vrsta table: "))        
        dimY = int(input("Uneti broj koloni table: "))
        
        #startne pozicije
        [x,y] = input("Uneti startnu poziciju prvog pesaka igraca X:").split(',')
        player1_pawn1 = [int(x), int(y)]
        [x,y] = input("Uneti startnu poziciju drugog pesaka igraca X:").split(',')
        player1_pawn2 = [int(x), int(y)]
        [x,y] = input("Uneti startnu poziciju prvog pesaka igraca O:").split(',')
        player2_pawn1 = [int(x), int(y)]
        [x,y] = input("Uneti startnu poziciju drugog pesaka igraca O:").split(',')
        player2_pawn2 = [int(x), int(y)]

        
        self.matrica = Matrica(dimX,dimY,player1_pawn1,player1_pawn2,player2_pawn1,player2_pawn2)
        self.matrica.mat = self.matrica.makeMatrix()
        wallNums = int(input("Uneti broj zidova: "))

        #prvi igrac X 
        pawn1 = Pawn(player1_pawn1)
        pawn2 = Pawn(player1_pawn2)
        local_playerX = Player("X",wallNums)
        local_playerX.AddPawns(pawn1,pawn2)
        
        #drugi igrac O
        pawn1 = Pawn(player2_pawn1)
        pawn2 = Pawn(player2_pawn2)
        local_playerO = Player("O",wallNums)
        local_playerO.AddPawns(pawn1,pawn2)

        #adding players to the matrix
        self.matrica.addPlayers(local_playerX, local_playerO)
        self.players['X'] = local_playerX
        self.players['O'] = local_playerO
    
    def printBoard(self):
        '''Printing board on the console'''
        print("Trenutno stanje matrice:", end="\n")
        self.matrica.printBoard() 

    
    def isFinishedGame(self, player: Player) -> bool:
        '''Provera da li je player pobedio'''
        return self.matrica.isEndOfGame(player)
 
    def playGame(self): #promeniti ovu funkciju tako da neizmenicno igraju igrac i kompjuter
        '''Zapocni igru, igraju igraci naizmenicno'''
        winner = None #Player()
        self.printBoard() 
        while True:
            if self.onTurn == 'X':
                currentPlayer = self.playTurn(self.matrica.playerX)
                self.players['X'] = currentPlayer
                self.onTurn = 'O'
            else:
                currentPlayer = self.playComputer(self.matrica.playerO)
                self.players['O'] = currentPlayer
                self.onTurn = 'X'

            if self.isFinishedGame(currentPlayer):
                winner = currentPlayer
                break
        print(f"Igra je zavrsena.\nPobednik je: {winner.sign}", end="\n")

    # def changePlayer():
    #     return None

#dodati funkciju koja odigrava potez kompjutera
    def playComputer(self, player: Player):
        timePcStart = time.perf_counter()
        print("PC is thinking..")
        if player.hasAnyWalls():
            tmp = self.minimax(self.matrica,2,1000, -1000, player)
        else:
            tmp = self.minimax(self.matrixInit,3,1000,-1000,player)
        self.matrica = tmp[0]
        
        self.printBoard()
        timePcEnd = time.perf_counter()
        print(f'General PC time: {timePcEnd - timePcStart}')
        return self.matrica.playerO



    def playTurn(self, player: Player) -> Player: 
        '''Player (Human or Computer) plays the turns'''
       
        print(f"Trenutno igra {player.sign} \n")
        
        movePawnDone = False
        while not movePawnDone:
            pawnNo = int(input("Izaberi pesaka(1 ili 2): "))
            if pawnNo not in [1,2]:
                print("Nevalidan broj pesaka!")
                continue
            tmpP = player.getPawn(pawnNo)
            [x,y] = input("Unesite novu poziciju pesaka: ").split(',')
            xDir = int(x)-tmpP.getPositions()[0]
            yDir = int(y)-tmpP.getPositions()[1]
            if self.matrica.validateMove(player, pawnNo, xDir, yDir):
                pawn = player.getPawn(pawnNo)
                if self.matrica.movePawn(player, pawnNo, [pawn.x + xDir, pawn.y + yDir]):
                    movePawnDone = True
                   

                    self.printMove(player, pawnNo)
                    self.printBoard()
            else:
                print("Nevalidan skok, pokusajte ponovo!")

        if player.hasAnyWalls(): 
            putWallDone = False
            while not putWallDone:
                wallType = int(input("Unesite tip zida (Horizontalni = 0 Vertikalni = 1): "))
                if wallType not in [0,1]:
                    print("Nevalidan tip zida!")
                    continue
                if player.hasWalls(wallType):
                    [wallX,wallY] = input("Unesite nove pozicije zida: (pozX,pozY): ").split(',')
                    wallPositions = [int(wallX), int(wallY)]
                    if self.matrica.validateWall(wallType, wallPositions):
                        if self.matrica.PutWall(player, wallType, wallPositions):
                           
                            
                            self.printWall(player,wallType,wallPositions)
                            self.printBoard()
                            putWallDone = True
                        else: 
                            print("Nevalidna pozicija zida!")
                    else: 
                        print("Nevalidna pozicija zida!")
                else:     
                    print("Nemate trazeni tip zida!")

        return player


    def printMove(self, player: Player, pawnNo: int):
        pawn = player.getPawn(pawnNo)
        print(f"Igrac {player.sign} je odigrao potez pesakom: {pawnNo} na poziciju [{pawn.x},{pawn.y}]")
    
    def printWall(self, player: Player, wallType: int, wallPositions: List[int]):
        '''WallType == 0 horizontal walls
           walltype == 1 vertical walls'''
        x = wallPositions[0]
        y = wallPositions[1]
        # betweenFields = [(x,y),(x,y+1),(x+1,y),(x+1,y+1)] #radi i za vertikalne i horizontalne zidove
        tipZida = "horizontalni" if wallType == 0 else "vertikalni" 
        print(f"Igrac {player.sign} je postavio zid {tipZida} izmedju polja [({x},{y}),({x},{y+1}),({x+1},{y}),({x+1},{y+1})]")

    def cloneMatrix(self, state:Matrica) -> Matrica:
        return state.clone()
       

    def generateMoves(self, player: Player, pawnNo : int)-> List[List[int]]:
        pawn=player.getPawn(pawnNo)
        x=pawn.x
        y=pawn.y
        moves = pawn.getMoves()
        validMoves = []
        
        for move in moves:
            tmpMove = list(move)
            tmpMove[0] -= x
            tmpMove[1] -= y
            if self.matrica.validateMove(player,pawnNo,tmpMove[0],tmpMove[1]):
                validMoves.append(move)
        return validMoves


    def generateAllWalls(self,player,state: Matrica) -> Set: 
        '''Generating all possible walls for shortest path for opponent'''
        setSvihZidova=set()
        lists = []
        sizes = []

        if player.sign == 'X':
            lists.insert(0, state.A_star(state.playerO,1,state.startPosX1))
            lists.insert(1, state.A_star(state.playerO,1,state.startPosX2))
            lists.insert(2, state.A_star(state.playerO,2,state.startPosX1))
            lists.insert(3, state.A_star(state.playerO,2,state.startPosX2))
        else:
            lists.insert(0, state.A_star(state.playerX,1,state.startPosO1))
            lists.insert(1, state.A_star(state.playerX,1,state.startPosO2))
            lists.insert(2, state.A_star(state.playerX,2,state.startPosO1))
            lists.insert(3, state.A_star(state.playerX,2,state.startPosO2))
        
        for path in lists:
            setSvihZidova.update(self.generateSetOfPossibleWalls(path))
        setValidnih = set(filter(lambda wall: state.validateWall(wall[1],list(wall[0])),setSvihZidova))
        return setValidnih

    def generateNewStates(self,player:Player, state:Matrica):
        allWalls = self.generateAllWalls(player,state)
        statesPawn1 = self.generateStatesForPawn(player,1, state, allWalls)
        # print(f'Counter == {len(statesPawn1)}')
        statesPawn2 = self.generateStatesForPawn(player,2, state, allWalls)
        # print(f'Counter == {len(statesPawn2)}')

        return statesPawn1 + statesPawn2

    def generateExpandedPath(self, put:List):
        expandedPut=[]
        for i in range(0,len(put)-1):
            expandedPut.append(put[i])
            if (put[i][0]==put[i+1][0]) and (abs(put[i][1]-put[i+1][1])==2):
                tmp=int((put[i][1]+put[i+1][1])/2)
                noviEl = (put[i][0],tmp)
                expandedPut.append(noviEl)
            elif (put[i][1]==put[i+1][1]) and (abs(put[i][0]-put[i+1][0])==2):
                tmp=int((put[i][0]+put[i+1][0])/2)
                noviEl = (tmp, put[i][1])
                expandedPut.append(noviEl)
        expandedPut.append(put[len(put)-1])
        return expandedPut

   
        

    def generateSetOfPossibleWalls(self, put:List[List[int]]):
        
        ePut=self.generateExpandedPath(put)
        ePut.reverse()
        setOfPossibleWalls=set()

        for i in range (0,len(ePut)-1):
            tmp = (ePut[i])
            tmpNext = (ePut[i+1])
            xDir = tmpNext[0] - tmp[0]
            yDir = tmpNext[1] - tmp[1]
            if abs(xDir) == abs(yDir):
                if xDir == -1 and yDir == -1:
                    setOfPossibleWalls.add((tmpNext,0))
                    setOfPossibleWalls.add((tmpNext,1))
                if xDir == -1 and yDir == 1:
                    sused = (tmp[0] - 1,tmp[1])
                    setOfPossibleWalls.add((sused,0))
                    setOfPossibleWalls.add((sused,1))
                if xDir == 1 and yDir == -1: 
                    sused = (tmp[0],tmp[1]-1)
                    setOfPossibleWalls.add((sused,0))
                    setOfPossibleWalls.add((sused,1))
                if xDir == 1 and yDir == 1:
                    setOfPossibleWalls.add((tmp,0))
                    setOfPossibleWalls.add((tmp,1))
                continue
            if xDir != 0:
                if xDir == 1:
                    setOfPossibleWalls.add((tmp,0))
                    sused = (tmp[0],tmp[1]-1)
                    setOfPossibleWalls.add((sused,0))
                else: #xDir == -1
                    setOfPossibleWalls.add((tmpNext,0))
                    sused = (tmpNext[0],tmpNext[1]-1)
                    setOfPossibleWalls.add((sused,0))
            if yDir != 0: #yDir != 0
                if xDir == 1:
                    setOfPossibleWalls.add((tmp,1))
                    sused = (tmp[0]-1,tmp[1])
                    setOfPossibleWalls.add((sused,1))
                else: #xDir == -1
                    setOfPossibleWalls.add((tmpNext,1))
                    sused = (tmpNext[0]-1,tmpNext[1])
                    setOfPossibleWalls.add((sused,1))
        
        return setOfPossibleWalls
        

    def generateStatesForPawn(self, player : Player, pawnNo, state:Matrica,setSvihZidova: Set)-> List[Matrica]:
        ''' Funckija vraca sve validna stanja za jednog pesaka'''
        #generisi validne porteze 
        #kloniraj matrice map fja 
        #i odigraj potez map fja 
        #vrati klon matrice 

        matriceNewState = []
        # startGeneralTime = time.perf_counter()
        pawn= player.getPawn(pawnNo)
        x=pawn.x #ovo se ne koristi
        y=pawn.y
        ciljevi = []
        if player.sign == 'X':
            cilj1 = state.A_star(player,pawnNo,state.startPosO1)
            cilj2 = state.A_star(player,pawnNo,state.startPosO2)
        else: 
            cilj1 = state.A_star(player,pawnNo,state.startPosX1)
            cilj2 = state.A_star(player,pawnNo,state.startPosX2)
        ciljevi.append(cilj1)
        ciljevi.append(cilj2)

        sizes = []
        sizes.append(len(cilj1))
        sizes.append(len(cilj2))
        minimumSize = 1000
        ind = -1
        for i in range(0,2):
            if sizes[i] < minimumSize:
                minimumSize = sizes[i]
                ind = i
        nextMove = ciljevi[ind].pop() #ovaj mi ne treba 
        nextMove = ciljevi[ind].pop()

        stateClone = state.clone()
        playerClone = player.clone()
        if player.sign=='X':
            plO = state.playerO.clone()
            stateClone.addPlayers(playerClone, plO)
        else:
            plX = state.playerX.clone()
            stateClone.addPlayers(plX, playerClone)
        stateClone.movePawn(playerClone,pawnNo,nextMove)
            
           
           
        #ako nema zidova    
        if not player.hasAnyWalls():  
            return stateClone

       
        def addMatrix(mat: Matrica, i,j,wallType,player, matriceNewState):
            # startAStar = time.perf_counter()
            tmp = mat.clone()
            if player.sign=='X':
                plO = mat.playerO.clone()
                tmp.addPlayers(player, plO)
            else:
                plX = mat.playerX.clone()
                tmp.addPlayers(plX, player)
                
            tr = tmp.PutWall(player,wallType,[i,j])
            
            if tr:
                matriceNewState.append(tmp)

        for par in setSvihZidova:
            tmpLista = list(par[0])
            wallType = par[1]
            if playerClone.hasWalls(wallType):  #and mat.validateWall(wallType, tmpLista):
                #kloniranje i postavljanje zida
                naruto = playerClone.clone()
                addMatrix(stateClone,tmpLista[0],tmpLista[1],wallType,naruto,matriceNewState)

        return matriceNewState               



    def minimax(self, state: Matrica, depth: int,alfa:int, beta:int, player: Player):
        #procena stanja, vracanje procene za krajnje stanje
        if  self.isFinishedGameOnCurrentState(state,player): 
            return [state,0]
        if depth == 0:
           return [state, self.procenaStanja(state, state.playerO, state.startPosX1, state.startPosX2)]
        # clonedPlayer = player.clone()
        children = self.generateNewStates(player, state)
       
        if player.sign == 'O': #maximizer
            bestState = state
            shortestPath = 1000
            for child in children:
                # plX = child.playerX.clone()
                value=self.minimax(child, depth-1, alfa, beta, child.playerX)
                if value[1] < shortestPath:
                    shortestPath = value[1]
                    bestState = child
                alfa= min(alfa, shortestPath)
                if beta >= alfa: #???
                    break
            return [bestState,shortestPath]
        else: #player.sign == 'X' #minimizer
            worstState = state
            longestPath = -1000
            for child in children:
                # plO = child.playerO.clone()
                value=self.minimax(child, depth-1, alfa, beta, child.playerO)
                if value[1] > longestPath:
                    longestPath = value[1]
                    worstState = child
                beta= max(beta, longestPath)
                if beta >= alfa:
                    break
            return [worstState,longestPath]
        
    def isFinishedGameOnCurrentState(self, state:Matrica,player:Player):
        return state.isEndOfGame(player)

   

    def procenaStanja(self, state:Matrica, player: Player, cilj1: List[int], cilj2: List[int])-> int:
        dist=0
        
        list1 = state.A_star(player,1,cilj1)
        list2 = state.A_star(player,1,cilj2)
        list3 = state.A_star(player,2,cilj1)
        list4 = state.A_star(player,2,cilj2)
        #zato sto se ukljucuju i prvi i poslednji cvor broj skokova je len - 1
        distX1C1 = len(list1)-1    #razdaljina izmedju x1 i c1
        distX1C2 = len(list2)-1    #raz izmedju x1 i c2
        distX2C1 = len(list3)-1   #raz izmedju x2 i c1
        distX2C2 = len(list4)-1   #raz izmedju x2 i c2
        dist= min(min(distX1C1,distX1C2), min(distX2C1, distX2C2))
        return dist

    def calcDistance(self, start: List[int], end: List[int]) -> int:
        result = 0
        for i in [0,1]:
            result += abs(end[i] - start[i])
        return result


game = Game()
game.matrixInit()
game.playGame()

# print(game.generateExpandedPath([(3,9),(4,9),(4,7),(4,5),(6,5),(7,4),(6,3)]))
#test komentar u moving&validating grani 
