from login import Login
from sql import SQL
from bet import Bet

l = Login()
b = Bet()

while not l.logged:

    if int(input("1-Login\n2-Register\n")) == 1:
        l.login()
    else:
        l.register()
        
logout = False

while not logout:
    
    print("""#################################
        1- Choose Sport (Current: """ + b.currentSport() + """)  
        2- Bet Simple
        3- Bet Multiple
        4- See Bet History
        5- Account Management
        0- Exit
#################################""")
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
            pass
        elif choice == 4:
            b.seeBestHistory(l.user.email)
        elif choice == 5:
            l.accountManagement()
            
                

