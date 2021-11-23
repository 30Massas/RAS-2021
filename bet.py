from sql import SQL

"""
Aposta 
    -Id
    -Odd Vitoria Casa
    -Odd Empate
    -Odd Vitoria Visitante
"""

class Bet():

    def __init__(self):
        self.sql = SQL()