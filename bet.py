from sql import SQL
import globals as g

sports = {
        0 : "None",
        1: "Football",
        2: "Tennis",
        3: "Basketball"
    }

class Bet():


    def __init__(self):
        self.sql = SQL()
        self.sport = 0

    def listAllPossibleBets(self,sport):
        self.sql.listAllBets(sport)

    def currentSport(self):
        global sports
        return sports[self.sport]

    def changeSport(self):
        print(
"""
1 - Football
2 - Tennis
3 - Basketball
""")
        self.sport = int(input("What sport do you want to bet on? "))

    def betOnGameSimple(self,user_id):
        self.listAllPossibleBets(self.currentSport())
        choice = int(input("""1-Bet | 2-Exit \n"""))
        if choice == 1:
            game_id = int(input("Enter the GameID you want to bet on: "))
            odd_choice = int(input("Choose the winner (1-TeamA, 2-Tie, 3-TeamB): "))
            g.print_coins()
            option = option = g.tipo_moedas[int(input('Choose the coin you want to bet with: '))]
            amount = int(input("Enter the amount you want to bet: "))
            self.sql.betOnGameSimple(user_id,game_id,option,amount,odd_choice)
        elif choice == 2:
            return
        else:
            print('ERROR: Invalid Option')

    def seeBestHistory(self,email):
        self.sql.seeBetHistory(email)

    def betOnGameMultiple(self,user_id):
        games = {}
        self.listAllPossibleBets(self.currentSport())
        choice = -1
        while choice != 2:
            choice = int(input("""1-Bet | 2-Finish Bet | 3-Exit \n"""))
            if choice == 1:
                game_id = int(input("Enter the GameID you want to bet on: "))
                odd_choice = int(input("Choose the winner (1-TeamA, 2-Tie, 3-TeamB): "))
                amount = int(input("Enter the amount you want to bet: "))
                games[game_id] = (odd_choice,amount)
            else:
                return
        else:
            self.sql.betOnGameMultiple(user_id,games)
