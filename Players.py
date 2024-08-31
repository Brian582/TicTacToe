from random import randrange

#Players attributes for the game
class Player:
    def __init__(self):
        self.username=''
        self.symbol=''
        self.turn=None
        self.winner=False

#Has the same attributes as a player but will run on its own
class Computer(Player):
    def __init__(self):
        super().__init__()
        self.username = 'Computer'

    #Computer makes a move in the game
    def chooseRandom(self):
        return randrange(0,3) 

#Used if player doesn't login with an account; information won't be saved to database
class Guest(Player):
    def __init__(self):
        super().__init__()
        self.username = 'Guest'
   
