import json
from sql import SQL

class Login():

    def __init__(self):
        self.info = {}
        self.user = {}
        self.logged = False
        self.sql = SQL()

    def login(self):
        email = input('Email: ')
        password = input('Password: ')
        if self.sql.login(email=email,password=password):
            self.logged = True
        else:
            self.logged = False

    def register(self):
        email = input("Email: ")
        user = input("Username: ")
        password = input("Password: ")
        amount = int(input("Amount to debit: "))
        self.sql.register(email=email,user=user,password=password,amount=amount)

        print('User sucessfuly registered!')
