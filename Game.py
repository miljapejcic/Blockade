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
            self.printBoard() #prints board after each turn
            #change whose turn is next
            self.onTurn = 'X' if self.onTurn == 'O' else 'O'
            if self.isFinishedGame(currentPlayer):
                winner = currentPlayer
                break
        print(f"Igra je zavrsena.\nPobednik je: {winner.sign}", end="\n")

    
    def playTurn(self, player: Player) -> Player: 
        '''Player (Human or Computer) plays the turns'''
        #prvo cemo da napravimo da radi PvP
        moveDone = False
        print(f"Trenutno igra {player.sign} \n")
        while (not moveDone):
            pawnNo = int(input("Izaberi pesaka: 1 ili 2: "))
            # self.generateNewStates(player,pawnNo) #ubaceno samo zbog testiranja 
            # print("Moguce napraviti samo dva koraka")
            # print("\nX-osa (vrste): -2,-1,0,1,2\nY-osa (kolone): -2,-1,0,1,2")
            cilj = player.getPawn(pawnNo)
            [x,y] = input("Unesite novu poziciju pesaka: ").split(',')
            xDir = cilj.getPositions()[0] - int(x)
            yDir = cilj.getPositions()[1] - int(y)
            # [xDir,yDir] = input("Unesite pravce kretanja:" ).split(',')
            # xDir = int(xDir)
            # yDir = int(yDir)
            if player.hasAnyWalls(): 
                wallType = int(input("Unesite tip zida: Horizontalni = 0 Vertikalni = 1 : "))
                if player.hasWalls(wallType):
                    [wallX,wallY] = input("Unesite nove pozicije zida: (pozX,pozY): ").split(',')
                    wallPositions = [int(wallX), int(wallY)]
                    if self.matrica.changeStateWithWalls(player,pawnNo,xDir,yDir,wallType,wallPositions):
                        self.printMove(player,pawnNo)
                        self.printWall(player,wallType,wallPositions)
                        moveDone = True        
                else: 
                    print("Nemate trazeni tip zida")
            else: 
                if not self.matrica.changeStateWithoutWalls(player,pawnNo,xDir,yDir):
                    print("Pozicija pesaka nije dozvoljena") #OVAJ IF TREBA ANALIZIRATI
                else: 
                    self.printMove(player,pawnNo)
                    moveDone = True
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

    def bes(self,player):
        statesPawn1 = self.generateNewStates(player,1)
        statesPawn2 = self.generateNewStates(player,2)


    def generateNewStates(self, player : Player, pawnNo)-> List[Matrica]:
        #generisi validne porteze 
        #kloniraj matrice map fja 
        #i odigraj potez map fja 
        #vrati klon matrice 
        pawn= player.getPawn(pawnNo)
        x=pawn.x
        y=pawn.y
        validMoves= self.generateMoves(player,pawnNo)
        playersClones = []
        clonedMatrice = []
        # clonedMatrice = list(itertools.repeat(self.cloneMatrix(),len(validMoves)))
        for i in range(0, len(validMoves)):
            clonedMatrice.append(self.cloneMatrix())
            playersClones.append(copy.deepcopy(player))
            print(f'Matrica_{i} = {id(clonedMatrice[i])}')
            clonedMatrice[i].printBoard()
            
        for i in range(0, len(validMoves)):
            clonedMatrice[i].changeStateWithoutWalls(playersClones[i],pawnNo,validMoves[i][0] - x, validMoves[i][1] - y)
            print(f'Matrica_{i} = {id(clonedMatrice[i])}')
            clonedMatrice[i].printBoard()
        print(f'Matrica_ORG = {id(self.matrica)}')
        self.matrica.printBoard()
        return clonedMatrice

            
        

        # print(self.matrica)
        # print(clone)
    
game = Game()
game.matrixInit()
game.playGame()
#test komentar u moving&validating grani 
