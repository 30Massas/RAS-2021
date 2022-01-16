import threading, time
import mysql.connector as mysql
from user import User

class Observer:

    def __init__(self):
        config = {
            "host" : "127.0.0.1",
            "user" : "rasuser",
            "password" : "ras123",
            "database" : "rasdb"
        }
        self.connection = mysql.connect(**config)
        self.user = None

    def setObservant(self, user):
        self.user = user

    def run(self):
        handler = threading.Thread(target=self.handleResults,daemon=True)
        handler.start()

    def handleResults(self):
        # Verificar de X em X tempo se os jogos já terminaram e atribuir um vencedor
        while True:
            time.sleep(120)
            # Fetch all games from user check if finished and won
            print('\nPING\n')
            cursor = self.connection.cursor()
            # Fetch all Boletim
            cursor.execute("SELECT * FROM boletim where user_email=%(user)s and estado='Aberta'",{'user': self.user.email})
            boletins = cursor.fetchall()
            bets = {}
            for entry in boletins:
                # For each boletim fetch game_id in bet and see if state == 'Fechado'
                cursor.execute("SELECT jogo_id FROM bet WHERE id=%(bet_id)s",{'bet_id' : entry[1]})
                game = cursor.fetchone()
                cursor.execute("SELECT estado_apostavel FROM jogo WHERE id=%(jogo_id)s", {'jogo_id' : game[0]})
                estado = cursor.fetchone()
                if entry[2] not in bets:
                    bets[entry[2]] = {
                        'valor' : entry[3],
                        'odd' : entry[4],
                        'moeda' : entry[6],
                        'games' : [(game[0],estado[0])]
                    }
                else:
                    bets[entry[2]]['games'].append((game[0],estado[0]))
            # If all games betted in boletim have state == 'Fechado' and user betted correctly on all , return amount, else 
            for boletim in bets.keys():
                aux = set()
                for game in  bets[boletim]['games']:
                    aux.add(game[1])
                # Verifies if all games are finished
                if len(aux) == 1 and 'Fechada' in aux:
                    ganhos_totais = bets[boletim]['valor'] * bets[boletim]['odd']
                    coin_info = {
                        'tipo' : bets[boletim]['moeda'],
                        'user' : self.user.email,
                        'montante' : ganhos_totais
                    }
                    cursor.execute("UPDATE moeda SET montante = montante + %(montante)s WHERE user_email=%(user)s AND tipo=%(tipo)s",coin_info)
                    cursor.execute("UPDATE boletim SET estado = 'Fechada' WHERE id=%(b_id)s", {'b_id' : boletim})
                    print(f'Boletim#{boletim} now closed!')
                    self.connection.commit()
                else:
                    print(f'Not all games are finished for boletim #{boletim}!')
            cursor.close()

