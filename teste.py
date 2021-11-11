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
1- \n2- \n3- \n0- Exit
#################################""")
    choice = int(input("Option: "))

    if choice == 0:
        print('Hope you comeback!')
        logout = True
    else:
        if choice == 1:
            print(l.user["username"])
        elif choice == 2:
            print(l.user["debit"])
        elif choice == 3:
            pass

