from sql import SQL
from user import User

class Login():

    def __init__(self):
        self.logged = False
        self.user = User()
        self.sql = SQL()

    def login(self):
        email = input('Email: ')
        password = input('Password: ')
        if self.sql.login(email=email,password=password):
            self.user.setCredentials(email,password)
            self.logged = True
        else:
            self.logged = False

    def register(self):
        email = input("Email: ")
        user = input("Username: ")
        password = input('Password: ')
        amount = int(input("Amount to debit: "))
        iban = input("IBAN: ")
        self.sql.register(email=email,user=user,password=password,amount=amount,iban=iban)

        print('User sucessfuly registered!')

    def accountManagement(self):
        acc = int(input("""
#################################
        1- Check Balance 
        2- Change Password
        3- Deposit
        4- Withdraw
        0- Exit
#################################
Option: """))
        if acc == 1:
            self.sql.checkBalance(self.user.email)
        elif acc == 2:
            old_pass = input("Enter old password: ")
            if old_pass == self.user.password:
                new_pass = input("Enter new password: ")
                confirm_pass = input("Confirm new password: ")
                if new_pass == confirm_pass:
                    self.sql.changePassword(new_pass,self.user.email)
        elif acc == 3:
            amount = int(input('How much money do you want to deposit?: '))
            self.sql.deposit(self.user.email,amount)
        elif acc == 4:
            amount = int(input('How much money do you want to withdraw?: '))
            self.sql.withdraw(self.user.email,amount)
        elif acc == 0:
            return