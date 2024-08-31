from Players import Player, Computer, Guest
from Account import CreateAccount, LoginToAccount
import PlayersTable

def Main():
    Introduction()
    Menu()
    Selection()
    PlayersTable.closePlayersTable()

#Introduction to the game 
def Introduction():
    print("Welcome to my TicTacToe game.")
    print("You start the game by first picking a symbol 'X' or 'O'. Then you play. ")
    print("To win the game, you need to three X's or O's in a row, column, or diagonal. ")
    print("You can play against another player or against the computer.")
    print("You can also create an account if you want to save your stats of the game.")
    print("Lets get started.\n")

#Displays a list of all the options for the game
def Menu():
    print("Select any of the options below.")
    print("1. View menu. \n" +
          "2. Play the game \n" +
          "3  Create an Account \n" +
          "4. Delete your account \n" +
          "5. View your stats \n" +
          "6. View all the players in table \n" +
          "7. Remove all existing players in the table\n" +
          "8. Exit the program \n")
    
#Player selects what they want to do
def Selection():

    again=True
    while again == True:
        
        valid = False
        while valid != True:
            try:
                response = input("Type in your choice: ")
                response = int(response)

                #range from 0-8
                if(response>0 and response<9):
                    valid=True
                
                else:
                    print("Not a valid choice. Try again.\n ")
            
            except:
                print("ERROR\n")

        #View Menu
        if(response==1):
            Menu()
         
        #play TicTacToe
        if(response==2):
            print("\nYou are now playing TicTacToe.")
            Tictactoe()

        #creates account
        if(response==3):
            print("\nYour creating an account.")
            CreateAccount()

        #deletes account
        if(response==4):
            print("\nLogin to delete your account.")
            player=LoginToAccount()
            if(player!=None):
                tup=(player.username,)#needs to be in a tuple for SQL query
                PlayersTable.deleteAccount(tup)
                print("Account deleted.") 

        #view stats
        if(response==5):
            print("\nTo view your stats you need to login.")
            player=LoginToAccount()
            if(player!=None):
                print("\nThis is " + player.username + "'s stats.")
                tup=(player.username,)
                PlayersTable.displayStats(tup)

        #view all players
        if(response==6):
            PlayersTable.displayPlayersTable()
        
        #clears the database
        if(response==7):
            PlayersTable.clearPlayersTable()
            print("Database cleared.")

        #exits program
        if(response==8):
            again=False

        if(again==True):
            print("\nWhat do you want to do now?")

#This where players are set up and play the game     
def Tictactoe():
    
    board = [[ " ", " ", " "], [ " ", " ", " "], [ " ", " ", " "]]
    player1 = SetupPlayer()

    print("\nAre you playing against a computer or another player?")
    ans=input("Type 'player' or 'computer': ")

    while ans!='player' and ans!='computer':
        print("Not a valid choose. Try again.\n")
        ans = input("Type 'player' or 'computer': ")  

    print("")
    if(ans == "computer"):
        player2 = Computer()

    else:
        player2 = SetupPlayer()

    PickSymbols(player1,player2)
    PlayGame(player1,player2,board)


#Sets up a player
def SetupPlayer():
    user=None
    response=input("Are you a returning player? ('YES' or 'NO'): ")
    response=response.upper()

    while(response!='YES' and response!='NO'):
        print("Not a valid response. Try again.")
        response=input("\nAre you a returning player? ('YES' or 'NO'): ")
        response=response.upper()

    if response=='YES':
        user=LoginToAccount()
        if(user == None):
            print("You'll be playing as a guest.")
            user = Guest()

    elif(response == 'NO'):
        print("You'll be playing as a guest.")
        user = Guest()
    

    return user

#Players pick their symbols
def PickSymbols(player1,player2):
    valid=False

    print("Player 1:")
    symbol=input("Select X or O: ")

    while(valid==False):
        if (symbol=='X' or symbol=='x' or symbol=='O' or symbol=='o'): 
            valid=True

        else:
            symbol=input("This is not a valid symbol. Please enter an  ' X ' or ' O' : ")

    #Changes the 'x' or 'o' into uppercase characters, just in case they are lowercase
    player1.symbol=symbol.upper() 

    if player1.symbol == 'X':
        player2.symbol = 'O'

    else: 
        player2.symbol = 'X'

    if(type(player2)==Computer):
        print("Player 1 will be '" + player1.symbol + "' and Computer  will be " + player2.symbol + "'.")

    else:
        print("Player 1 will be '" + player1.symbol + "' and Player 2 will be '" + player2.symbol + "'.")

    #sets players turns, player 1 will go first
    player1.turn=True
    player2.turn=False

    return player1,player2


#Displays board 
def displayBoard(board):

    print("")
    
    for i in range(len(board)):
        print( "", board[i][0] , "|" , board[i][1] , "|" , board[i][2])

        if(i < 2): 
            print("-----------")

    print("")


#Plays the TicTacToe game
def PlayGame(player1,player2,board):

    CurrentPlayer=None
    full=None
    winner=False
    displayBoard(board)

    while(winner==False):

        if(player1.turn==True):
            print("Player 1: " + '"' + player1.symbol + '",' + " it's your turn.")

            #Sets up player 2 to play next round
            player1.turn=False
            player2.turn=True
            CurrentPlayer=player1

        else:
            if(type(player2)==Computer):
                print("It's Computer's turn.")

            else:
                print("Player 2: " + '"' + player2.symbol + '",' + " it's your turn.")

            #Sets up player 1 to play next round
            player1.turn=True
            player2.turn=False
            CurrentPlayer=player2
 
        valid=False

        #checks if cordinates are valid
        while(valid==False):

            if(type(CurrentPlayer)==Computer):
                row=CurrentPlayer.chooseRandom()
                column=CurrentPlayer.chooseRandom()
               
            else: 
                row=int(input("Type in row (Upper row is 0, Middle row is 1, Lower row is 2): "))
                column=int(input("Type in column (Left column is 0, Middle column is 1, Right column is 2): "))

            valid=Move(CurrentPlayer,row,column,board)

        displayBoard(board)
        full = FullBoard(board)   
        winner = checkWinner(CurrentPlayer,board)
     
        if(winner==True):
            UpdatePlayerStats(player1,player2)

        elif(full==True):
            print("The board is full.")
            print("NO WINNER.")
            break


#Player makes a move on the board
def Move(player,row,column,board):
    try:

        if(board[row][column] == 'X' or board[row][column] == 'O'): 
            
            #this is so a message doesn't get displayed when player 2 is the computer
            if(type(player)==Computer):
                return False
            
            else:
                print("This position is already taken. Pick another one.\n")
                return False

        else:        
            board[row][column] = player.symbol
            return True
    
    except:
        print("The position you entered is out of length. Please try again.\n")
        return False


#Checks if player has 3 marks in a row
def checkWinner(player,board):

    winner=False
    
    for i in range(len(board)):
            
            #Checks the rows
            if ((board[i][0]==player.symbol) and  (board[i][1]==player.symbol) and (board[i][2]==player.symbol)): 
                winner=True
            
            #Checks the columns
            elif((board[0][i]==player.symbol) and  (board[1][i]==player.symbol) and (board[2][i]==player.symbol)): 
                winner=True

    #Checks left diagonal
    if ((board[0][0]==player.symbol) and  (board[1][1]==player.symbol) and (board[2][2]==player.symbol)):
        winner=True    
    
    #Checks right diagonal
    elif((board[0][2]==player.symbol) and  (board[1][1]==player.symbol) and (board[2][0]==player.symbol)):
        winner=True  

    if(winner==True):
        player.winner=True

    return winner

#Updates the stats of the players 
def UpdatePlayerStats(player1,player2):
    
    if player1.winner==True:

        if(type(player1) == Player or type(player1) == Guest): 
            print("Player 1 is the winner!!!!")

            if(type(player1)== Player):
                player1stats=(player1.username,)
                PlayersTable.updateGamesWon(player1stats)
     
            if(type(player2)==Player):
                player2stats=(player2.username,)
                PlayersTable.updateGamesLost(player2stats)
            
    elif player2.winner==True:
        if(type(player2) == Computer):
            print("Computer is the winner!!!!")
            
            player1stats=(player1.username,)
            PlayersTable.updateGamesLost(player1stats)
            
        
        elif(type(player2)==Player):
            print("Player 2 is the winner!!!!")

            player2stats=(player2.username,)
            PlayersTable.updateGamesWon(player2stats)

            player1stats=(player1.username,)
            PlayersTable.updateGamesLost(player1stats)


#Checks if the board is full
def FullBoard(board):

    for i in range(len(board)):
        if ((board[i][0]==' ') or (board[i][1]==' ') or (board[i][2]==' ')):
                return False

    return True

#Calls Main 
Main()
