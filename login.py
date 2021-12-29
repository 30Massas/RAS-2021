from sql import SQL
from user import User
import re
import globals as g

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
        iban = input("IBAN: ")
        bday_form_correct = False
        while not bday_form_correct:
            bday = input("Enter your birthday (YYYY-MM-DD): ")
            if re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', bday):
                bday_form_correct = True
            else:
                print('Wrong Date Format. Please Try Again!')
        g.print_coins()
        option = g.tipo_moedas[int(input('Choose the coin you want do deposit: '))]
        amount = int(input('Amount: '))
        cc = input("CC: ")
        self.sql.register(email=email,user=user,password=password,amount=amount,iban=iban,cc=cc,tipo_moeda=option,montante=amount,bday=bday)

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
            g.print_coins()
            option = g.tipo_moedas[int(input('Choose the coin you want do deposit: '))]
            amount = int(input('Amount: '))
            self.sql.deposit(self.user.email,option,amount)
        elif acc == 4:
            self.sql.checkBalance(self.user.email)
            g.print_coins()
            option = g.tipo_moedas[int(input('Choose the coin you want do withdraw: '))]
            amount = int(input('Amount: '))
            self.sql.withdraw(self.user.email,option,amount)
        elif acc == 0:
            return