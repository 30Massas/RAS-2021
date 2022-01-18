from login import Login
from bet import Bet
from observer import Observer

try:
    l = Login()
    b = Bet()
    o = Observer()
except Exception as e:
    print(e)
    print(f'Something Went Wrong.')
    exit()

while not l.logged:
    try:
        if (r:=int(input("1-Login\n2-Register\n0-Exit\nOption: "))) == 1:
            l.login()
            o.setObservant(l.user)
        elif r==2:
            l.register()
        elif r==0:
            print('Hope you comeback!')
            exit()
        else:
            print('ERROR: Invalid Option')
    except Exception:
        print('ERROR: Insert a valid option!')
        
logout = False

while not logout:
    o.run()
    print("""######################################
    1- Choose Sport (Current: """ + b.currentSport() + """)  
    2- Bet Simple
    3- Bet Multiple
    4- See Bet History
    5- Account Management
    0- Exit
######################################""")
    try:
        choice = int(input("Option: "))

        if choice == 0:
            print('Hope you comeback!')
            logout = True
        else:
            if choice == 1:
                b.changeSport()
            elif choice == 2:
                if b.currentSport() == 'None':
                    print("Choose a Sport to Bet on!!")
                else:
                    b.betOnGameSimple(l.user.email)
            elif choice == 3:
                if b.currentSport() == 'None':
                    print("Choose a Sport to Bet on!!")
                else:
                    b.betOnGameMultiple(l.user.email)
            elif choice == 4:
                b.seeBestHistory(l.user.email)
            elif choice == 5:
                l.accountManagement()
            else:
                print('ERROR: Invalid Option')
    except ValueError as e:
        print(e)
        print('ERROR: Insert a valid option!')


