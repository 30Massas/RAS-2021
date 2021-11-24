from sql import SQL

"""
Aposta 
    -Id
    -Odd Vitoria Casa
    -Odd Empate
    -Odd Vitoria Visitante
"""

"""
0 - None
1 - Futebol
2 - Ténis
3 - Basquetebol
"""

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
        choice = int(input(""" 1-Bet | 2-Exit \n"""))
        if choice == 1:
            game_id = int(input("Enter the GameID you want to bet on: "))
            amount = int(input("Enter the amount you want to bet: "))
            self.sql.betOnGameSimple(user_id,game_id,amount)
        else:
            return

    def seeBestHistory(self,email):
        self.sql.seeBetHistory(email)
        pass