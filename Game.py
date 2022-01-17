from threading import Timer
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
        tmp = self.minimax(self.matrica, 2, -1000, 1000, player)
        self.matrica = tmp[0]
        # self.players['O'] = tmp[0].playerO
        self.printBoard()
        timePcEnd = time.perf_counter()
        print(f'General PC time: {timePcEnd - timePcStart}')
        return self.matrica.playerO



    def playTurn(self, player: Player) -> Player: 
        '''Player (Human or Computer) plays the turns'''
        #prvo cemo da napravimo da radi PvP
        # moveDone = False
        print(f"Trenutno igra {player.sign} \n")
        # if player.sign == 'O': #ovo obrisati ako je sve testirano
        #     self.generateNewStates(player) 
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

    def generateNewStates(self,player:Player, state:Matrica):
        statesPawn1 = self.generateStatesForPawn(player,1, state)
        # print(f'Counter == {len(statesPawn1)}')
        statesPawn2 = self.generateStatesForPawn(player,2, state)
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

    def generateSetOfPossibleWallsForOne(self, expPut:List):
        setOfPossibleWalls=set()
        for i in expPut:
            setOfPossibleWalls.add((i[0],i[1]))
            setOfPossibleWalls.add((i[0],i[1]-1))
            setOfPossibleWalls.add((i[0]-1,i[1]-1))
            setOfPossibleWalls.add((i[0]-1,i[1]))
        return setOfPossibleWalls

    def generateSetOfPossibleWalls(self, put1:List[List[int]],put2:List[List[int]],put3:List[List[int]],put4:List[List[int]]):
        ePut1=self.generateExpandedPath(put1)
        ePut2=self.generateExpandedPath(put2)
        ePut3=self.generateExpandedPath(put3)
        ePut4=self.generateExpandedPath(put4)
        setOfPossibleWalls = set()
        setOfPossibleWalls.update(self.generateSetOfPossibleWallsForOne(ePut1))
        setOfPossibleWalls.update(self.generateSetOfPossibleWallsForOne(ePut2))
        setOfPossibleWalls.update(self.generateSetOfPossibleWallsForOne(ePut3))
        setOfPossibleWalls.update(self.generateSetOfPossibleWallsForOne(ePut4))
        return setOfPossibleWalls

    def generateStatesForPawn(self, player : Player, pawnNo, state:Matrica)-> List[Matrica]:
        ''' Funckija vraca sve validna stanja za jednog pesaka'''
        #generisi validne porteze 
        #kloniraj matrice map fja 
        #i odigraj potez map fja 
        #vrati klon matrice 

        
        # startGeneralTime = time.perf_counter()
        pawn= player.getPawn(pawnNo)
        x=pawn.x #ovo se ne koristi
        y=pawn.y
        validMoves= self.generateMoves(player,pawnNo)
        playersClones = []
        clonedMatrice = []
        matriceNewState =[]
        for i in range(0, len(validMoves)):
            clonedMatrice.append(self.cloneMatrix(state)) #nekaMat.clone()   self.Clone(nekaMat)
            playersClones.append(player.clone())
            #OVO SAM JEDINO MENJALA
            if player.sign == 'X':
                plO = state.playerO.clone()
                clonedMatrice[i].addPlayers(playersClones[i], plO)
                clonedMatrice[i].movePawn(clonedMatrice[i].playerX, pawnNo,validMoves[i])
            else:
                plX = state.playerX.clone()
                clonedMatrice[i].addPlayers(plX, playersClones[i])
                clonedMatrice[i].movePawn(clonedMatrice[i].playerO,pawnNo,validMoves[i])
                
            # clonedMatrice[i].movePawn(playersClones[i],pawnNo,validMoves[i])
            # print('------')
            # clonedMatrice[i].printBoard()
        # for i in range(0, len(validMoves)):
           
        #ako nema zidova    
        if not player.hasAnyWalls():  
                    
            # endGeneralTime = time.perf_counter()
            # print(f'General time: {endGeneralTime - startGeneralTime}')
            return clonedMatrice

        setSvihZidova=set()

        if player.sign == 'X':
            list1 = self.matrica.A_star(self.matrica.playerX,1,self.matrica.startPosO1)
            list2 = self.matrica.A_star(self.matrica.playerX,1,self.matrica.startPosO2)
            list3 = self.matrica.A_star(self.matrica.playerX,2,self.matrica.startPosO1)
            list4 = self.matrica.A_star(self.matrica.playerX,2,self.matrica.startPosO2)
            setSvihZidova = self.generateSetOfPossibleWalls(list1, list2, list3, list4)
        else:
            list1 = self.matrica.A_star(self.matrica.playerO,1,self.matrica.startPosX1)
            list2 = self.matrica.A_star(self.matrica.playerO,1,self.matrica.startPosX2)
            list3 = self.matrica.A_star(self.matrica.playerO,2,self.matrica.startPosX1)
            list4 = self.matrica.A_star(self.matrica.playerO,2,self.matrica.startPosX2)
            setSvihZidova = self.generateSetOfPossibleWalls(list1, list2, list3, list4)

        time_A_star = 0

        def addMatrix(mat: Matrica, i,j,wallType,player, matriceNewState):
            # startAStar = time.perf_counter()
            tmp = mat.clone()
            if player.sign=='X':
                plO = self.players['O'].clone()
                tmp.addPlayers(player, plO)
            else:
                plX = self.players['X'].clone()
                tmp.addPlayers(plX, player)
                
            tr= tmp.PutWall(player,wallType,[i,j])
            
            if tr:
                matriceNewState.append(tmp)
                # print('------')
                # tmp.printBoard()
            # endAStar = time.perf_counter()
            # return endAStar - startAStar

        for ind in range(0,len(clonedMatrice)):
            mat = clonedMatrice[ind]
            for par in setSvihZidova:
                tmpLista = list(par)
                
                if playersClones[ind].hasWalls(0) and mat.validateWall(0, tmpLista):
                    #kloniranje i postavljanje zida
                    naruto = playersClones[ind].clone()
                    addMatrix(mat,tmpLista[0],tmpLista[1],0,naruto,matriceNewState)
                if playersClones[ind].hasWalls(1) and mat.validateWall(1, tmpLista):
                    #kloniranje i postavljanje zida
                    naruto = playersClones[ind].clone()
                    addMatrix(mat,tmpLista[0],tmpLista[1],1,naruto,matriceNewState)

                    
        endGeneralTime = time.perf_counter()
        # print(f'General time: {endGeneralTime - startGeneralTime}')
        # print(f'A_star time: {time_A_star}')
        return matriceNewState               

    def minimax(self, state: Matrica, depth: int,alfa:int, beta:int, player: Player):
        #procena stanja, vracanje procene za krajnje stanje
        if depth == 0 or self.isFinishedGame(player): 
            if player.sign== 'X':
                return [state, self.procenaStanja(state, state.playerX, state.startPosO1, state.startPosO2)]
            else:
                return [state, self.procenaStanja(state, state.playerO, state.startPosX1, state.startPosX2)]
        tmpMatrica = state
        # clonedPlayer = player.clone()
        children = self.generateNewStates(player, state)
        if player.sign == 'O':
            maxEval= -1000
            for child in children:
                # plX = child.playerX.clone()
                eval=self.minimax(child, depth-1, alfa, beta, child.playerX)
                if eval[1] > maxEval:
                    maxEval = eval[1]
                    tmpMatrica = child
                # maxEval=max(maxEval, eval[1])
                alfa= max(alfa, eval[1])
                if beta <= alfa:
                    break
            return [tmpMatrica,maxEval]
        else:
            minEval=1000
            for child in children:
                # plO = child.playerO.clone()
                eval=self.minimax(child, depth-1, alfa, beta, child.playerO)
                # minEval=max(minEval, eval[1])
                if eval[1] < minEval:
                    minEval = eval[1]
                    tmpMatrica = child
                beta= min(beta, eval[1])
                if beta <= alfa:
                    break
            return [tmpMatrica,minEval]
        
    def procenaStanja(self, state:Matrica, player: Player, cilj1: List[int], cilj2: List[int])-> int:
        dist=0
        list1 = state.A_star(player,1,cilj1)
        list2 = state.A_star(player,1,cilj2)
        list3 = state.A_star(player,2,cilj1)
        list4 = state.A_star(player,2,cilj2)
        distX1C1= 0 if len(list1)==1 else len(list1)#razdaljina izmedju x1 i c1
        distX1C2= 0 if len(list2)==1 else len(list2)  #raz izmedju x1 i c2
        distX2C1= 0 if len(list3)==1 else len(list3)  #raz izmedju x2 i c1
        distX2C2= 0 if len(list4)==1 else len(list4)  #raz izmedju x2 i c2
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
