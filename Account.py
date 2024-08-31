from Players import Player
from PlayersTable import addAccount, checkAccount

#Creates an account for the player
def CreateAccount():

    successful=False
    valid=False
    valid2=False

    print("Enter \"EXIT\" if you dont want to create an account.")
    while(successful!=True):

        #Username part
        while(valid==False):
            user=input("Create a username (Max length: 10 characters): ")
            
            if(checkIfExit(user)==True):
                return None
            
            elif(len(user)>10):
                print("Username is too long. Try again.\n")

            else:
                valid=True
        
        #password part
        while(valid2==False):
            password=input("Create a password (Max length: 10 characters): ")
            
            if(checkIfExit(password)==True):
                return None
            
            elif(len(password)>10):
                print("Password is too long. Try again.\n")
            
            else:
                valid2=True

        #puts account info in a tuple and then checks if its in the database
        login=(user,password)
        successful=addAccount(login)


    player = Player()
    player.username=login[0]
    print("Account created.")
    
    return player

#Logins in the account if its in the database
def LoginToAccount():

    accessible=False
    print("Enter \"EXIT\" to leave login.")

    while(accessible!=True):
        user=input("Enter your username: ")    
        if(checkIfExit(user)==True):
            return None
        
        password=input("Enter your password: ")
        if(checkIfExit(password)==True):
            return None
        
        #puts account info in a tuple and then checks if its in the database
        login=(user,password)
        accessible=checkAccount(login)
        if(accessible==False):
            print("Account not found. Try again.\n")
    
    player = Player()
    player.username=login[0]#assigns player's username

    return player


#checks if player entered EXIT
def checkIfExit(userlogin):
    try:
        response = userlogin.upper()#just in case its in lowercase letter
        if(response =="EXIT"):
            return True
        
        else:
            return False

    except:
        return False 
