import mysql.connector as mysql
import globals as g

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
                print(f'{g.bcolors.FAIL}Incorrect password!{g.bcolors.ENDC}')
                return False
        else:
            print(f'{g.bcolors.FAIL}No User Found!{g.bcolors.ENDC}')
            return False

        cursor.close()

    def register(self,**kw):
        cursor = self.connection.cursor()
        user_info = {
            'email' : kw['email'],
            'name' : kw['user'],
            'password' : kw['password'],
            'bday' : kw['bday'],
            'iban' : kw['iban'],
            'cc' : kw['cc']
        }
        cursor.execute("INSERT INTO user VALUES (%(email)s,%(name)s,%(password)s,%(iban)s,%(bday)s,%(cc)s)",user_info)
        moeda_info = {
            "tipo" : kw['tipo_moeda'],
            "montante" : kw['montante'],
            "user" : kw['email']
        }
        cursor.execute("INSERT INTO moeda (tipo,montante,user_email) VALUES (%(tipo)s,%(montante)s,%(user)s)",moeda_info)
        self.connection.commit()
        cursor.close()

    def checkBalance(self,user_id):
        cursor = self.connection.cursor()
        cursor.execute("""
SELECT montante,tipo FROM moeda
WHERE user_email=%(email)s""", {'email':user_id})
        print(f'{g.bcolors.OKBLUE}##### Current Balance #####{g.bcolors.ENDC}')
        if db := cursor.fetchall():
            for coins in db:
                print(f'\t{coins[0]} {coins[1]}')
        else:
            print(f'{g.bcolors.WARNING}You Have No Currency In Your Account!{g.bcolors.ENDC}')
        print(f'{g.bcolors.OKBLUE}###########################{g.bcolors.ENDC}')
        cursor.close()

    def changePassword(self,new_password,user_id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE user SET password = %(pass)s WHERE email = %(id)s", {'pass' : new_password, 'id' : user_id})
        self.connection.commit()
        cursor.close()

    def deposit(self,user_id,option,amount):
        cursor = self.connection.cursor()
        cursor.execute("SELECT EXISTS(SELECT * FROM moeda WHERE user_email=%(user)s AND tipo=%(tipo)s)",{"user":user_id,"tipo":option})
        if (r:=cursor.fetchone()[0]) == 1: 
            cursor.execute("UPDATE moeda SET montante = montante + %(amount)s WHERE user_email = %(id)s AND tipo=%(tipo)s", {"amount":amount,"id":user_id,"tipo":option} )
        else:
            cursor.execute("INSERT INTO moeda (tipo,montante,user_email) VALUES (%(tipo)s,%(amount)s,%(id)s)", {"amount":amount,"id":user_id,"tipo":option})
        self.connection.commit()
        cursor.close()

    def withdraw(self,user_id,option,amount):
        cursor = self.connection.cursor()
        cursor.execute("SELECT EXISTS(SELECT * FROM moeda WHERE user_email=%(user)s AND tipo=%(tipo)s)",{"user":user_id,"tipo":option})
        if (r:=cursor.fetchone()[0]) == 1: 
            cursor.execute("SELECT montante FROM moeda WHERE user_email=%(user)s AND tipo=%(tipo)s",{"user":user_id,"tipo":option})
            r = cursor.fetchone()
            if r[0] >= amount:
                cursor.execute("UPDATE moeda SET montante = montante - %(amount)s WHERE user_email = %(id)s AND tipo=%(tipo)s", {"amount":amount,"id":user_id,"tipo":option} )
            else:
                print(f'{g.bcolors.WARNING}ERROR: Withdraw Not Possible.{g.bcolors.ENDC}')    
        else:
            print(f'{g.bcolors.WARNING}ERROR: Withdraw Not Possible.{g.bcolors.ENDC}')
        self.connection.commit()

        cursor.close()

    def convertCoin(self,user_id,to_convert,converted,amount):
        cursor = self.connection.cursor()
        cursor.execute("SELECT EXISTS(SELECT * FROM moeda WHERE user_email=%(user)s AND tipo=%(tipo)s)",{"user":user_id,"tipo":to_convert})
        if (r:=cursor.fetchone()[0]) == 1: 
            cursor.execute("SELECT montante FROM moeda WHERE user_email=%(user)s AND tipo=%(tipo)s",{"user":user_id,"tipo":to_convert})
            r = cursor.fetchone()
            if r[0] >= amount:
                converted_amount = g.convertCoin(to_convert, converted, amount)
                cursor.execute("SELECT EXISTS(SELECT * FROM moeda WHERE user_email=%(user)s AND tipo=%(tipo)s)",{"user":user_id,"tipo":converted})
                if (m:=cursor.fetchone()[0]) == 1:
                    cursor.execute("UPDATE moeda SET montante = montante - %(amount)s WHERE user_email = %(id)s AND tipo=%(tipo)s", {"amount":amount,"id":user_id,"tipo":to_convert} )
                    cursor.execute("UPDATE moeda SET montante = montante + %(amount)s WHERE user_email = %(id)s AND tipo=%(tipo)s", {"amount":converted_amount,"id":user_id,"tipo":converted} )
                else:
                    cursor.execute("UPDATE moeda SET montante = montante - %(amount)s WHERE user_email = %(id)s AND tipo=%(tipo)s", {"amount":amount,"id":user_id,"tipo":to_convert})
                    cursor.execute("INSERT INTO moeda (tipo,montante,user_email) VALUES (%(tipo)s,%(amount)s,%(id)s)", {"amount":converted_amount,"id":user_id,"tipo":converted})
        self.connection.commit()
        cursor.close()

###################### Betting ###################### 

    def listAllBets(self, sport, categoria):
        cursor = self.connection.cursor()
        cursor.execute("SELECT odd_vitoriaCasa, equipaCasa, odd_empate, equipaVisitante, odd_vitoriaVisitante, id, horario, estado_apostavel FROM jogo WHERE jogo.desporto=%(sport)s" , {'sport' : sport})
        if games := cursor.fetchall():
            print("Game ID --> TeamA OddWinA - OddTie - OddWinB TeamB")
            print(f"{g.bcolors.OKBLUE}###################### Games to Bet ######################{g.bcolors.ENDC}")
            for game in games:
                if categoria == 1:
                    if game[7] == 'Aberta':
                        print(f"{game[5]} --> {game[1]} {game[0]} - {game[2]} - {game[4]} {game[3]} ")
                else:
                    if game[7] == 'Aberta':
                        print(f"{game[5]} --> {game[1]} {game[0]} - {game[4]} {game[3]} ")
            print(f"{g.bcolors.OKBLUE}#########################################################{g.bcolors.ENDC}")
        else:
            print(f'{g.bcolors.WARNING}No Games Were Found!{g.bcolors.ENDC}')
        cursor.close()

    def betOnGameSimple(self,user_id,game_id,option,amount,odd_choice):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Boletim ORDER BY id DESC LIMIT 1")
        if r := cursor.fetchone():
            #print(r)
            boletim_id = r[2]+1
        else:
            boletim_id = 1
        coin_info={
            'tipo' : option,
            'montante' : amount,
            'user' : user_id
        }
        bet_info = {
            'jogo' : game_id,
            'equipa' : odd_choice
        } 
        boletim_info = {
            'user' : user_id,
            'estado' : 'Aberta',
            'b_id' : boletim_id,
            'valor' : amount,
            'moeda' : option
        }
        # Checking if gameId actually exists
        cursor.execute("SELECT * FROM jogo WHERE id = %(id)s AND estado_apostavel='Aberta'",{'id' : game_id})
        try:
            if r:=cursor.fetchone():
                valor_odd = r[1+odd_choice]
                bet_info['valor_odd'] = valor_odd
                boletim_info['valor_odd'] = valor_odd
                choice = int(input('1-Confirm\n2-Exit\nOption: '))
                if choice == 1:
                    # Check if money is enough
                    cursor.execute("SELECT montante FROM moeda WHERE user_email=%(user)s AND tipo=%(tipo)s",coin_info)
                    try:
                        if debit:=cursor.fetchone()[0] > amount:
                            # Commit bet
                            cursor.execute("INSERT INTO bet (jogo_id,odd,equipaEscolhida) VALUES (%(jogo)s,%(valor_odd)s,%(equipa)s)",bet_info)
                            # Commit boletim
                            boletim_info['bet'] = cursor.lastrowid
                            cursor.execute("INSERT INTO Boletim (user_email,bet_id,id,valor,total_odd,estado,moeda) VALUES (%(user)s,%(bet)s,%(b_id)s,%(valor)s,%(valor_odd)s,%(estado)s,%(moeda)s)",boletim_info)
                            cursor.execute("UPDATE moeda SET montante = montante - %(amount)s WHERE user_email=%(id)s AND tipo=%(tipo)s", {"amount":amount,"id":user_id,"tipo":option} )
                            self.connection.commit()
                        else:
                            print(f'{g.bcolors.WARNING}ERROR: Insufficient Funds{g.bcolors.ENDC}')
                            return
                    except Exception:
                        print(f'{g.bcolors.WARNING}ERROR: No balance for {g.bcolors.FAIL}{option}{g.bcolors.ENDC}!{g.bcolors.ENDC}')
                elif choice == 2:
                    print(f'{g.bcolors.WARNING}Bet Cancelled{g.bcolors.ENDC}')
                    return
                else:
                    print(f'{g.bcolors.WARNING}ERROR: Invalid Option{g.bcolors.ENDC}')
            else:
                print(f'{g.bcolors.WARNING}ERROR: Invalid GameID chosen!{g.bcolors.ENDC}')
        except Exception:
            print(f'{g.bcolors.WARNING}ERROR: Invalid GameID chosen!{g.bcolors.ENDC}')
        cursor.close()
    
    def betOnGameMultiple(self,user_id,games_betted,option,amount):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Boletim ORDER BY id DESC LIMIT 1")
        if r := cursor.fetchone():
            boletim_id = r[2]+1
        else:
            boletim_id = 1
        coin_info={
            'tipo' : option,
            'montante' : amount,
            'user' : user_id
        }
        boletim_info = {
            'user' : user_id,
            'estado' : 'Aberta',
            'b_id' : boletim_id,
            'valor' : amount,
            'moeda' : option
        }
        bets = []
        # Fazer como na bet simples mas repetir para cada jogo que esteja no games_betted
        # Obter row do boletim depois da primeira bet e guardar numa variabel e inserir aí
        total_odd = 1
        for game,choice in games_betted.items():
            bet_info = {
            'jogo' : game,
            'equipa' : choice,
            }
            # Checking if gameId actually exists
            cursor.execute("SELECT * FROM jogo WHERE id = %(id)s AND estado_apostavel='Aberta'",{'id' : game})
            try:
                if r:=cursor.fetchone():
                    valor_odd = r[1+choice]
                    bet_info['valor_odd'] = valor_odd
                    total_odd = total_odd * valor_odd
                    # Check if money is enough
                    cursor.execute("SELECT montante FROM moeda WHERE user_email=%(user)s AND tipo=%(tipo)s",coin_info)
                    if debit:=cursor.fetchone()[0] > amount:
                        # Commit bet
                        cursor.execute("INSERT INTO bet (jogo_id,odd,equipaEscolhida) VALUES (%(jogo)s,%(valor_odd)s,%(equipa)s)",bet_info)
                        # Commit boletim
                        last_id = cursor.lastrowid
                        bets.append(last_id)
                    else:
                        print(f'{g.bcolors.WARNING}ERROR: Insufficient Funds{g.bcolors.ENDC}')
                        return
                else:
                    print(f'{g.bcolors.WARNING}ERROR: Invalid GameID chosen!{g.bcolors.ENDC}')
            except Exception:
                print(f'{g.bcolors.WARNING}ERROR: Invalid GameID chosen!{g.bcolors.ENDC}')
        for bet in bets:
            boletim_info['bet'] = bet
            boletim_info['valor_odd'] = total_odd
            cursor.execute("INSERT INTO Boletim (user_email,bet_id,id,valor,total_odd,estado,moeda) VALUES (%(user)s,%(bet)s,%(b_id)s,%(valor)s,%(valor_odd)s,%(estado)s,%(moeda)s)",boletim_info)
        valid=False
        while not valid:    
            choice = int(input('1-Confirm\n2-Exit\nOption: '))
            if choice == 1:
                cursor.execute("UPDATE moeda SET montante = montante - %(amount)s WHERE user_email=%(id)s AND tipo=%(tipo)s", {"amount":amount,"id":user_id,"tipo":option} )
                self.connection.commit()
                valid=True
            elif choice == 2:
                print(f'{g.bcolors.WARNING}Bet Cancelled{g.bcolors.ENDC}')
                valid=True
                return
            else:
                print(f'{g.bcolors.WARNING}ERROR: Invalid Option{g.bcolors.ENDC}')

        cursor.close()

    def seeBetHistory(self,email):
        cursor = self.connection.cursor()
        # Fecth all Boletins
        # For each boletim fetch all bets
        # Print bets
        # Tentar fazer paginação
        b_ids = set()
        cursor.execute("SELECT * FROM Boletim WHERE user_email=%(user)s", {'user':email})
        if boletins := cursor.fetchall():
            for b in boletins:
                if b[2] in b_ids:
                    pass
                else:
                    print(f'Boletim #{b[2]} -> {b[5]}')
                    print(f'Amount: {b[3]} {b[6]}')
                    b_ids.add(b[2])
                cursor.execute("SELECT * FROM bet WHERE id=%(id)s", {'id':b[1]})
                if bets := cursor.fetchall():
                    for bet in bets:
                        cursor.execute("SELECT * FROM jogo WHERE id=%(id)s",{'id':bet[1]})
                        if jogo:=cursor.fetchone():
                            if int(bet[3]) == 1:
                                print(f'GameID# {bet[1]} -> {jogo[5]} ({jogo[2]})')
                            elif int(bet[3]) == 2:
                                print(f'GameID# {bet[1]} -> Tie ({jogo[3]})')
                            else:
                                print(f'GameID# {bet[1]} -> {jogo[6]} ({jogo[4]})')
        cursor.close()