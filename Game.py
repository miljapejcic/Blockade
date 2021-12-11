from Matrica import * 
class Game: 

    def __init__(self) :
        self.matrica = None
        self.onTurn = ''
        self.players = { 
            'X' : None,
            'O' : None
        }
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
        playerX = Player("X",wallNums,wallNums)
        playerX.AddPawns(pawn1,pawn2)
        
        #drugi igrac O
        pawn1 = Pawn(player2_pawn1)
        pawn2 = Pawn(player2_pawn2)
        playerO = Player("O",wallNums,wallNums)
        playerO.AddPawns(pawn1,pawn2)

        #adding players to the matrix
        self.matrica.addPlayers(playerX, playerO)
        self.players['X'] = playerX
        self.players['O'] = playerO
    
    def printBoard(self):
        '''Printing board on the console'''
        print("Trenutno stanje matrice:", end="\n")
        self.matrica.printBoard() #miljin kod za printing

    #NOT IMPLEMENTED!!!!!
    #mozda nam ovo i ne treba
    def finishedGame(self, player: Player):
        '''Provera da li je neko pobedio'''

        return self.matrica.isEndOfGame(player)
 
    #NOT IMPLEMENTED!!!!!
    def playGame(self):
        '''Zapocni igru, igraju igraci naizmenicno'''

        while True:
            currentPlayer = self.playTurn(self.players(self.onTurn))
            self.onTurn = 'X' if self.onTurn == 'O' else 'O'
            if self.finishedGame(currentPlayer):
                break

        # while (not_finished): 
        #     sadaIgra = self.onTurn
                #player = self.players[sadaIgra]
        # ako je moj potez igram
        # ako nije PCplays()
        #prompt (gde hoces da se pomeris, smer)
        #proveri potezz
        #pomeri igraca
        #kraj runde => onTurn menja vrednost


    #NOT IMPLEMENTED!!!!! 
    def computerPlays(self):
        '''kompjuter je na redu da igra'''
        print("NOT IMPLEMENTED")


    
game = Game()
game.matrixInit()
