from login import Login
from sql import SQL

l = Login()

while not l.logged:

    if int(input("1-Login\n2-Register\n")) == 1:
        login = l.login()
    else:
        user = l.register()
        
logout = False

while not logout:
    
    print("""#################################
        1- Choose Sport  
        2- Bet
        3- See Bet History
        0- Exit
#################################""")
    choice = int(input("Option: "))

    if choice == 0:
        print('Hope you comeback!')
        logout = True
    else:
        if choice == 1:
            pass
        elif choice == 2:
            pass
        elif choice == 3:
            pass

