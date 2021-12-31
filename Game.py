from Matrica import * 
import itertools
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
 
    def playGame(self):
        '''Zapocni igru, igraju igraci naizmenicno'''
        winner = None #Player()
        self.printBoard() 
        while True:
            currentPlayer = self.playTurn(self.players[self.onTurn])
            # self.printBoard() #prints board after each turn
            #change whose turn is next
            self.onTurn = 'X' if self.onTurn == 'O' else 'O'
            if self.isFinishedGame(currentPlayer):
                winner = currentPlayer
                break
        print(f"Igra je zavrsena.\nPobednik je: {winner.sign}", end="\n")

    
    def playTurn(self, player: Player) -> Player: 
        '''Player (Human or Computer) plays the turns'''
        #prvo cemo da napravimo da radi PvP
        # moveDone = False
        print(f"Trenutno igra {player.sign} \n")
        if player.sign == 'O':
            self.generateNewStates(player)
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

    def cloneMatrix(self) -> Matrica:
       
        return   self.matrica.clone()
       

    def generateMoves(self, player: Player, pawnNo : int)-> List[List[int]]:
        pawn=player.getPawn(pawnNo)
        x=pawn.x
        y=pawn.y
        potezi= []
        for i in range(pawn.x-1,pawn.x+2):
            for j in range(pawn.y-1, pawn.y+2):
                if not (pawn.x==i and pawn.y==j):
                    if self.matrica.validateMove(player,pawnNo,i-x,j-y):
                        potezi.append([i,j])
        nizX  = [-2,2,0,0]
        nizY = [0,0,-2,2]
        for i in range(0,4):
            if self.matrica.validateMove(player,pawnNo, nizX[i], nizY[i]):
                potezi.append([x+nizX[i],y+nizY[i]])

        return potezi

    def generateNewStates(self,player):
        statesPawn1 = self.generateStatesForPawn(player,1)
        statesPawn2 = self.generateStatesForPawn(player,2)


    def generateStatesForPawn(self, player : Player, pawnNo)-> List[Matrica]:
        ''' Funckija vraca sve validna stanja za jednog pesaka'''
        #generisi validne porteze 
        #kloniraj matrice map fja 
        #i odigraj potez map fja 
        #vrati klon matrice 

        print("Starting generating matrices...")
        pawn= player.getPawn(pawnNo)
        x=pawn.x
        y=pawn.y
        validMoves= self.generateMoves(player,pawnNo)
        playersClones = []
        clonedMatrice = []
        matriceNewState =[]
        for i in range(0, len(validMoves)):
            clonedMatrice.append(self.cloneMatrix())
            playersClones.append(copy.deepcopy(player))
        for i in range(0, len(validMoves)):
            clonedMatrice[i].movePawn(playersClones[i],pawnNo,validMoves[i])
            # print(f'Matrica_{i} = {id(clonedMatrice[i])}')
            # clonedMatrice[i].printBoard()   
        #ako nema zidova    
        if not player.hasAnyWalls():            
            return clonedMatrice
                #print(f'Matrica_{i} = {id(clonedMatrice[i])}')
                #clonedMatrice[i].printBoard()
        #ako ima zidova
        counter = 0
        for ind in range(0,len(clonedMatrice)):
            mat=clonedMatrice[ind]
            for i in range(0,mat.dimX-1):
                for j in range(0,mat.dimY-1):
                    
                    def addMatrix(mat: Matrica, i,j,wallType,player, matriceNewState):
                        if mat.validateWall(wallType, [i,j]):
                            tmp = mat.clone()
                            tr= tmp.PutWall(player,wallType,[i,j])
                            if tr:
                                matriceNewState.append(tmp)
                                # print(f'Matrica_{i} = {id(tmp)}')
                                # tmp.printBoard()
                    naruto = copy.deepcopy(player)
                    if playersClones[ind].hasWalls(0):
                        counter += 1
                        addMatrix(mat,i,j,0,naruto,matriceNewState)
                        # if mat.validateWall(0, [i,j]):
                        #     tmp = mat.clone()
                        #     tr= tmp.PutWall(playersClones[ind],0,[i,j])
                        #     if tr:
                        #         matriceNewState.append(tmp)
                    if playersClones[ind].hasWalls(1):
                        counter += 1
                        addMatrix(mat,i,j,1,naruto,matriceNewState)

                        # if mat.validateWall(1, [i,j]):
                        #     tmp = mat.clone()
                        #     tr= tmp.PutWall(playersClones[ind],1,[i,j])
                        #     if tr:
                        #         matriceNewState.append(tmp)
        print(f'Counter == {counter}')
        return matriceNewState        


        

        # #print(f'Matrica_ORG = {id(self.matrica)}')
        # # clonedMatrice = list(itertools.repeat(self.cloneMatrix(),len(validMoves)))
        # for i in range(0, len(validMoves)):
        #     clonedMatrice.append(self.cloneMatrix())
        #     playersClones.append(copy.deepcopy(player))
        #     print(f'Matrica_{i} = {id(clonedMatrice[i])}')
        #     clonedMatrice[i].printBoard()
        
            
        # for i in range(0, len(validMoves)):
        #     clonedMatrice[i].changeStateWithoutWalls(playersClones[i],pawnNo,validMoves[i][0] - x, validMoves[i][1] - y)
        #     print(f'Matrica_{i} = {id(clonedMatrice[i])}')
        #     clonedMatrice[i].printBoard()
        # print(f'Matrica_ORG = {id(self.matrica)}')
        # self.matrica.printBoard()
        # return matriceNewState

            
        

        # print(self.matrica)
        # print(clone)
    
game = Game()
game.matrixInit()
game.playGame()
#test komentar u moving&validating grani 
