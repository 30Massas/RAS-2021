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
            'debit' : kw['amount'],
            'iban' : kw['iban']
        }
        cursor.execute("INSERT INTO user VALUES (%(email)s,%(name)s,%(password)s,%(debit)s,%(iban)s)",values)
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

    def deposit(self,user_id,amount):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE user SET debit = debit + %(amount)s WHERE email = %(id)s", {"amount":amount,"id":user_id} )
        self.connection.commit()
        cursor.close()

    def withdraw(self,user_id,amount):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE user SET debit = debit - %(amount)s WHERE email = %(id)s", {"amount":amount,"id":user_id} )
        self.connection.commit()
        cursor.close()


###################### Betting ###################### 

    def listAllBets(self, sport):
        cursor = self.connection.cursor()
        cursor.execute("SELECT odd_vitoriaCasa, equipaCasa, odd_empate, equipaVisitante, odd_vitoriaVisitante, id FROM jogo WHERE jogo.desporto=%(sport)s" , {'sport' : sport})
        if games := cursor.fetchall():
            print("Game ID --> TeamA OddWinA - OddTie - OddWinB TeamB")
            print("###################### Games to Bet ######################")
            for game in games:
                print(f"{game[5]} --> {game[1]} {game[0]} - {game[2]} - {game[4]} {game[3]} ")
            print("#########################################################")
        else:
            print('No games were found!')
        cursor.close()

    def betOnGameSimple(self,user_id,game_id,amount,odd_choice):
        cursor = self.connection.cursor()
        values = {
            'user_id' : user_id,
            'game_id' : game_id,
            'amount' : amount,
            'equipa' : odd_choice
        }
        # Checking if gameId actually exists
        cursor.execute("SELECT * FROM jogo WHERE id = %(id)s",{'id' : game_id})
        if r:=cursor.fetchone():
            # Adding bet to user's bet
            valor_odd = r[1+odd_choice]
            values['valor_odd'] = valor_odd
            cursor.execute("SELECT debit FROM user WHERE email = %(user_id)s",values)
            debit = cursor.fetchone()
            if debit[0] > amount:
                cursor.execute("INSERT INTO bet (user_email,jogo_id,valor,total_odd,equipaEscolhida) VALUES (%(user_id)s,%(game_id)s,%(amount)s,%(valor_odd)s,%(equipa)s)", values)
                cursor.execute("UPDATE user SET debit = debit - %(amount)s WHERE email = %(user_id)s ", values)
            else:
                print("Insuficient Funds!")
            self.connection.commit()
        else:
            print('No game was found for that GameID!\nBet could not be placed!')
        cursor.close()

    def seeBetHistory(self,email):
        cursor = self.connection.cursor()
        cursor.execute("""
SELECT equipaCasa, odd_vitoriaCasa, odd_empate, odd_vitoriaVisitante, equipaVisitante, b.id, b.equipaEscolhida FROM jogo
LEFT JOIN bet b ON jogo.id=b.jogo_id
WHERE b.user_email = (%(email)s)""", {'email' : email})
        if bets := cursor.fetchall():
            print("#################### BET HISTORY ####################")
            for bet in bets:
                if bet[6] == '1':
                    print(f"{bet[5]} - **{bet[0]}** ({bet[1]}) - {bet[2]} - ({bet[3]}) {bet[4]}")
                elif bet[6] == '2':
                    print(f"{bet[5]} - {bet[0]} ({bet[1]}) - **{bet[2]}** - ({bet[3]}) {bet[4]}")
                else:
                    print(f"{bet[5]} - {bet[0]} ({bet[1]}) - {bet[2]} - ({bet[3]}) **{bet[4]}**")
            print("#####################################################")
        else:
            print("No bets have been made yet!")
        cursor.close()