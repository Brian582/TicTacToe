import sqlite3

db = sqlite3.connect('PlayerStats.db')
curs = db.cursor()

#Creates a table to hold player accounts and their stats
curs.execute("""CREATE TABLE IF NOT EXISTS PlayerStats (
                 player_username VARCHAR(10) PRIMARY KEY, 
                 player_password VARCHAR(10),  
                 games_played  INTEGER,  
                 games_won  INTEGER,
                 games_lost  INTEGER
                 )""")


#Adds account to the database
def addAccount(account):
    try:
        query="""INSERT INTO PlayerStats (player_username, player_password, games_played, games_won, games_lost) 
                VALUES (?, ?, 0, 0, 0) """
        
        curs.execute(query, account)
        db.commit()

        return True

    except Exception as e:
        print("An error has occurred. Couldn't add account to the database.")
        print(e)
        return False

#Checks if the account is in the database
def checkAccount(account):
    try:
        query="""SELECT player_username, player_password FROM PlayerStats 
                WHERE player_username = ? AND player_password = ? """
        
        curs.execute(query, account)
        row=curs.fetchall()
        db.commit()
        
        #this would mean the row is empty, which means the account isn't in the database
        if(len(row)==0):
            return False
        
        else:
            return True
        
    except Exception as e:
        print("An error has occurred.")
        print(e)
        return False


#Deletes player's account from the database
def deleteAccount(account):
    try:
        query="DELETE FROM PlayerStats WHERE player_username = ?"
        curs.execute(query, account)
        db.commit()
        
    except:
        print("An error has occurred. Couldn't delete account.")


#Updates the games won stat for player
def updateGamesWon(gameWon):
    try:
        query="""UPDATE PlayerStats 
              SET games_won = games_won +1, games_played = games_played +1  
              WHERE player_username = ? """

        curs.execute(query, gameWon)
        db.commit()
        
    except Exception as e:
        print("An error has occurred. Couldn't update player's stats")


#Updates the games lost stat of the player
def updateGamesLost(gameLost):
    try:
        query="""UPDATE PlayerStats 
              SET games_lost = games_lost +1, games_played = games_played +1 
              WHERE player_username = ? """

        curs.execute(query, gameLost)
        db.commit()
        
    except:
        print("An error has occurred. Couldn't update player's stats")


#Displays the stats of the player
def displayStats(playerStats):
    try:
   
        query="SELECT * FROM PlayerStats WHERE player_username == ?"
        curs.execute(query, playerStats)
        player=curs.fetchall()
        db.commit()

        for column in player:
            print("\nPlayer's Username: " + column[0])
            print("Games Played: " + str(column[2]))
            print("Games Won: " + str(column[3]))
            print("Games Lost: " + str(column[4]))
        
    except Exception as e:
        print("An error has occurred.")
        print(e)


#Displays the database
def displayPlayersTable():
    try:
        query="""SELECT * FROM PlayerStats"""
        curs.execute(query)
        table=curs.fetchall()
        db.commit()

        #this means the database is empty
        if(len(table)==0):
           return print("There are no players in the database.")
        
        else:
            num=0
            
            print('')
            column_titles = "   {: ^12} {: ^12} {: ^12} {: ^12} {: ^10}"
            print(column_titles.format("Username","Password","Games played","Games Won", "Games Lost"))

            for column in table:
                num+=1
                line= " {: ^12} {: ^12} {: ^12} {: ^12} {: ^10} "
                print( str(num) + "." + line.format(column[0], column[1] , str(column[2]) , str(column[3]), str(column[4])))
                 
            print('')

    except Exception as e:
        print("An error has occurred.")
        print(e)


#Clears the database
def clearPlayersTable():
    try:
        query="DELETE FROM PlayerStats"
        curs.execute(query)
        db.commit()
        
    except:
        print("An error has occurred. Couldn't delete account.")


#Closes connection and database, its used at the end of the program
def closePlayersTable():
    curs.close()
    db.close()
