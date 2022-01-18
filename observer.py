import threading, time
import globals as g
import datetime as dd
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
        result_handler = threading.Thread(target=self.handleResults,daemon=True)
        game_handler = threading.Thread(target=self.handleGames,daemon=True)
        result_handler.start()
        game_handler.start()

    def handleResults(self):
        cursor = self.connection.cursor()
        # Verificar de X em X tempo se os jogos já terminaram e atribuir um vencedor
        while True:
            time.sleep(120)
            # Fetch all games from user check if finished and won
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
                    ganhos_totais = g.round_half_away_from_zero(bets[boletim]['valor'] * bets[boletim]['odd'])
                    coin_info = {
                        'tipo' : bets[boletim]['moeda'],
                        'user' : self.user.email,
                        'montante' : ganhos_totais
                    }
                    cursor.execute("UPDATE moeda SET montante = montante + %(montante)s WHERE user_email=%(user)s AND tipo=%(tipo)s",coin_info)
                    cursor.execute("UPDATE boletim SET estado = 'Fechada' WHERE id=%(b_id)s", {'b_id' : boletim})
                    print(f'\n{g.bcolors.OKBLUE}OBSERVER: Boletim#{boletim} now closed!{g.bcolors.ENDC}')
                    self.connection.commit()
            time.sleep(120)
        cursor.close()

    def handleGames(self):
        cursor=self.connection.cursor()
        while True:
            today = dd.datetime.today()
            time.sleep(15)
            cursor.execute("SELECT * FROM jogo WHERE estado_apostavel='Aberta'")
            jogos = cursor.fetchall()
            for jogo in jogos:
                if jogo[7] <= today:
                    print(f'\n{g.bcolors.OKBLUE}OBSERVER: Game#{jogo[0]} -> {jogo[5]} VS {jogo[6]} has finished!{g.bcolors.ENDC}')
                    cursor.execute("UPDATE jogo SET estado_apostavel='Fechada' WHERE id=%(id)s",{'id':jogo[0]})
            self.connection.commit()
        cursor.close()