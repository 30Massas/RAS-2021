from login import Login
from bet import Bet
from observer import Observer
import globals as g

try:
    try:
        l = Login()
        b = Bet()
        o = Observer()
    except Exception as e:
        print(e)
        print(f'{g.bcolors.FAIL}Something Went Wrong.{g.bcolors.ENDC}')
        exit()

    while not l.logged:
        try:
            if (r:=int(input(f"{g.bcolors.OKGREEN}1-Login\n2-Register\n0-Exit{g.bcolors.ENDC}\n{g.bcolors.HEADER}Option: {g.bcolors.ENDC}"))) == 1:
                l.login()
                o.setObservant(l.user)
            elif r==2:
                l.register()
            elif r==0:
                print(f'{g.bcolors.BOLD}Hope you comeback!{g.bcolors.ENDC}')
                exit()
            else:
                print(f'{g.bcolors.WARNING}ERROR: Invalid Option{g.bcolors.ENDC}')
        except Exception:
            print(f'{g.bcolors.WARNING}ERROR: Insert a valid option!{g.bcolors.ENDC}')

    logout = False

    while not logout:
        o.run()
        print(f"""{g.bcolors.OKBLUE}######################################{g.bcolors.ENDC}"""
    +f"""\n    1- {g.bcolors.OKGREEN}Choose Sport{g.bcolors.ENDC} ({g.bcolors.WARNING}Current:{g.bcolors.ENDC} """ + b.currentSport() + """)"""  
    +f"""\n    2- {g.bcolors.OKGREEN}Bet Simple{g.bcolors.ENDC}"""
    +f"""\n    3- {g.bcolors.OKGREEN}Bet Multiple{g.bcolors.ENDC}"""
    +f"""\n    4- {g.bcolors.OKGREEN}See Bet History{g.bcolors.ENDC}"""
    +f"""\n    5- {g.bcolors.OKGREEN}See Current Bets{g.bcolors.ENDC}"""
    +f"""\n    6- {g.bcolors.OKGREEN}Account Management{g.bcolors.ENDC}"""
    +f"""\n    0- {g.bcolors.OKGREEN}Exit{g.bcolors.ENDC}"""
    +f"""\n{g.bcolors.OKBLUE}######################################{g.bcolors.ENDC}""")
        try:
            choice = int(input(f"{g.bcolors.HEADER}Option: {g.bcolors.ENDC}"))

            if choice == 0:
                print(f'{g.bcolors.BOLD}Hope you comeback!{g.bcolors.ENDC}')
                logout = True
            else:
                if choice == 1:
                    b.changeSport()
                elif choice == 2:
                    if b.currentSport() == 'None':
                        print(f"{g.bcolors.WARNING}Choose a Sport to Bet on!!{g.bcolors.ENDC}")
                    else:
                        b.betOnGameSimple(l.user.email)
                elif choice == 3:
                    if b.currentSport() == 'None':
                        print(f"{g.bcolors.WARNING}Choose a Sport to Bet on!!{g.bcolors.ENDC}")
                    else:
                        b.betOnGameMultiple(l.user.email)
                elif choice == 4:
                    b.seeBestHistory(l.user.email)
                elif choice == 5:
                    b.seeActiveBets(l.user.email)
                elif choice == 6:
                    l.accountManagement()
                else:
                    print(f'{g.bcolors.WARNING}ERROR: Invalid Option{g.bcolors.ENDC}')
        except ValueError as e:
            print(e)
            print(f'{g.bcolors.WARNING}ERROR: Insert a valid option!{g.bcolors.ENDC}')
except KeyboardInterrupt:
    print(f'{g.bcolors.BOLD}\nHope You Comeback!{g.bcolors.ENDC}')

