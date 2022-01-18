from sql import SQL
import globals as g

sports = {
        0 : "None",
        1: "Football",
        2: "Tennis",
        3: "Basketball"
    }

coletivos = [1,3]
individuais = [2]

class Bet():


    def __init__(self):
        self.sql = SQL()
        self.sport = 0

    def listAllPossibleBets(self):
        if self.sport in coletivos:
            self.sql.listAllBets(self.currentSport(),1)
        else:
            self.sql.listAllBets(self.currentSport(),0)

    def currentSport(self):
        try:
            return sports[self.sport]
        except KeyError:
            print(f'{g.bcolors.WARNING}ERROR: Sport not avaiable!{g.bcolors.ENDC}')
            return sports[0]

    def changeSport(self):
        print(
"""
1 - Football
2 - Tennis
3 - Basketball
""")
        self.sport = int(input("What sport do you want to bet on? "))
        if self.sport not in sports:
            self.sport=0

    def betOnGameSimple(self,user_id):
        self.listAllPossibleBets()
        choice = int(input(f"""{g.bcolors.HEADER}1-Bet | 2-Exit \nOption: {g.bcolors.ENDC}"""))
        if choice == 1:
            game_id = int(input("Enter the GameID you want to bet on: "))
            if self.sport in coletivos:
                valid=False
                while not valid:
                    odd_choice = int(input("Choose the winner (1-TeamA, 2-Tie, 3-TeamB): "))
                    if not(odd_choice<1) or not(odd_choice>3):
                        valid=True
                    else:
                        print(f'{g.bcolors.WARNING}ERROR: Please choose a valid option!{g.bcolors.ENDC}')
            else:
                valid=False
                while not valid:
                    try:
                        odd_choice = int(input("Choose the winner (1-TeamA, 3-TeamB): "))
                        if not(odd_choice==1) or not(odd_choice==3):
                            valid=True
                        else:
                            print(f'{g.bcolors.WARNING}ERROR: Please choose a valid option!{g.bcolors.ENDC}')
                    except ValueError:
                        print(f'{g.bcolors.WARNING}ERROR: Insert a valid option!{g.bcolors.ENDC}')
            g.print_coins()
            valid=False
            while not valid:
                try:
                    option = g.tipo_moedas[int(input('Choose the coin you want to bet with: '))]
                    valid = True
                except Exception:
                    print(f'{g.bcolors.WARNING}ERROR: Invalid Option!{g.bcolors.ENDC}')
            amount = int(input("Enter the amount you want to bet: "))
            self.sql.betOnGameSimple(user_id,game_id,option,amount,odd_choice)
        elif choice == 2:
            return
        else:
            print(f'{g.bcolors.WARNING}ERROR: Invalid Option{g.bcolors.ENDC}')

    def seeBestHistory(self,email):
        self.sql.seeBetHistory(email)

    def betOnGameMultiple(self,user_id):
        games = {}
        teams = {1: 'TeamA', 2: 'Tie', 3: 'TeamB'}
        choice = -1
        while choice != 3:
            self.listAllPossibleBets()
            print(f'{g.bcolors.OKBLUE}###### Current Bet ######{g.bcolors.ENDC}')
            print('GameID - Team')
            for game,team in games.items():
                print(f'#{game} -> {teams[team]}')
            try:
                valid=False
                while not valid:
                    choice = int(input(f"""{g.bcolors.HEADER}1-Bet | 2-Remove Bet | 3-Finish Bet | 0-Exit \nOption: {g.bcolors.ENDC}"""))
                    if not(choice<0) or not(choice>3):
                        valid=True
                    else:    
                        print(f'{g.bcolors.WARNING}ERROR: Invalid Option{g.bcolors.ENDC}')
            except Exception:
                print(f'{g.bcolors.WARNING}ERROR: Invalid Option{g.bcolors.ENDC}')
            # Permitir a remoção de uma aposta do boletim
            # Permitir visualizar o boletim
            if choice == 1:
                game_id = int(input("Enter the GameID you want to bet on: "))
                if self.sport in coletivos:
                    odd_choice = int(input("Choose the winner (1-TeamA, 2-Tie, 3-TeamB): "))
                else:
                    odd_choice = int(input("Choose the winner (1-TeamA, 3-TeamB): "))
                games[game_id] = odd_choice
            elif choice == 2:
                game_id = int(input('Enter the GameID you want to remove: '))
                games.pop(game_id)
            elif choice == 0:
                return
            elif choice>3:
                print(f'{g.bcolors.WARNING}ERROR: Invalid Option{g.bcolors.ENDC}')
        else:
            g.print_coins()
            valid=False
            while not valid:
                try:
                    option = g.tipo_moedas[int(input('Choose the coin you want to bet with: '))]
                    valid = True
                except Exception:
                    print(f'{g.bcolors.WARNING}ERROR: Invalid Option!{g.bcolors.ENDC}')
            amount = int(input("Enter the amount you want to bet: "))
            self.sql.betOnGameMultiple(user_id,games,option,amount)
