import json
from sql import SQL

class Login():

    def __init__(self):
        self.logged = False
        self.id = ""
        self.password = ""
        self.sql = SQL()

    def login(self):
        email = input('Email: ')
        password = input('Password: ')
        if self.sql.login(email=email,password=password):
            self.id = email
            self.password = password
            self.logged = True
        else:
            self.logged = False

    def register(self):
        email = input("Email: ")
        user = input("Username: ")
        password = input('Password: ')
        amount = int(input("Amount to debit: "))
        self.sql.register(email=email,user=user,password=password,amount=amount)

        print('User sucessfuly registered!')

    def accountManagement(self):
        acc = int(input("""
#################################
        1- Check Balance 
        2- Change Password
        3- 
        0- Exit
#################################
Option: """))
        if acc == 1:
            self.sql.checkBalance(self.id)
        elif acc == 2:
            old_pass = input("Enter old password: ")
            if old_pass == self.password:
                new_pass = input("Enter new password: ")
                confirm_pass = input("Confirm new password: ")
                if new_pass == confirm_pass:
                    self.sql.changePassword(new_pass,self.id)
        elif acc == 3:
            pass
        elif acc == 0:
            return