import mysql.connector as mysql

class SQL():

    def __init__(self):
        config = {
            "host" : "127.0.0.1",
            "user" : "rasuser",
            "password" : "ras123",
            "database" : "rasdb"
        }
        self.connection = mysql.connect(**config)
        
###################### User Managing ######################

    def login(self,email,password):
        cursor = self.connection.cursor()

        cursor.execute('SELECT email FROM user WHERE user.email=%(email)s',{'email' : email})
        user = cursor.fetchone()
        if user:
            cursor.execute("SELECT password FROM user WHERE user.email=%(email)s AND user.password = %(password)s", {'email' : email, 'password' : password})
            if cursor.fetchone():
                return True
            else:
                print('Incorrect password!')
                return False
        else:
            print('No user with that email was found!')
            return False

        cursor.close()

    def register(self,**kw):
        cursor = self.connection.cursor()
        values = {
            'email' : kw['email'],
            'name' : kw['user'],
            'password' : kw['password'],
            'debit' : kw['amount']
        }
        cursor.execute("INSERT INTO user VALUES (%(email)s,%(name)s,%(password)s,%(debit)s)",values)
        self.connection.commit()
        cursor.close()

    def checkBalance(self,user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT debit FROM user WHERE email=%(email)s", {'email':user_id})
        db = cursor.fetchone()
        print(f"Your Current Balance: {db[0]}€")
        cursor.close()

    def changePassword(self,new_password,user_id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE user SET password = %(pass)s WHERE email = %(id)s", {'pass' : new_password, 'id' : user_id})
        self.connection.commit()
        cursor.close()


###################### Betting ###################### 

    def listAllBets(self, sport):
        cursor = self.connection.cursor()
        cursor.execute("SELECT odd_vitoriaCasa, equipaCasa, odd_empate, equipaVisitante, odd_vitoriaVisitante, id FROM jogo WHERE jogo.desporto=%(sport)s" , {'sport' : sport})
        games = cursor.fetchall()
        print("###################### Games to Bet ######################")
        print("Game ID --> TeamA OddWinA - OddTie - OddWinB TeamB")
        for game in games:
            print(f"{game[5]} --> {game[1]} {game[0]} - {game[2]} - {game[4]} {game[3]} ")
        print("#########################################################")
        cursor.close()

    def betOnGameSimple(self,user_id,game_id,amount):
        cursor = self.connection.cursor()
        values = {
            'user_id' : user_id,
            'game_id' : game_id,
            'amount' : amount
        }
        cursor.execute("INSERT INTO bet (user_email,jogo_id,valor) VALUES (%(user_id)s,%(game_id)s,%(amount)s)", values)
        cursor.execute("UPDATE user SET debit = debit - %(amount)s WHERE email = %(user_id)s ", {'amount' : amount, 'user_id' : user_id})
        self.connection.commit()
        cursor.close()

    def seeBetHistory(self,email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM bet WHERE user_email = (%(email)s)", {'email' : email})
        bets = cursor.fetchall()
        for bet in bets:
            print(bet)
        cursor.close()