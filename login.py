from sql import SQL
from user import User
import globals as g
import re, datetime
from dateutil.relativedelta import relativedelta

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
        valid_email = False
        while not valid_email:
            email = input("Email: ")
            if re.search(r'[a-zA-Z0-9].*@.*\.(pt|com)', email):
                valid_email = True
            else:
                print('Insert a valid email!')
        valid_user = False
        while not valid_user:
            if (user := input("Username: ")) != '':
                valid_user = True
            else:
                print('Insert a valid username!')
        valid_password = False
        while not valid_password:
            if (password := input('Password: ')) != '':
                valid_password = True
            else:
                print('Insert a valid password!')
        # Verificar se IBAN é valido
        valid_iban = False
        while not valid_iban:
            iban = input("IBAN: ")
            if re.search(r'[A-Z]{2}[0-9]{23}', iban):
                valid_iban = True
            else:
                print('Insert a valid IBAN!')
        bday_form_correct = False
        while not bday_form_correct:
            bday = input("Enter your birthday (YYYY-MM-DD): ")
            if re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', bday):
                # Verificar se >18 e <100
                today = datetime.date.today()
                compare = datetime.date.fromisoformat(bday)
                years = relativedelta(today,compare)
                if years.years >= 18 and years.years <= 100:
                    bday_form_correct = True
                else:
                    print('You can not register!')
                    return
            else:
                print('Wrong Date Format. Please Try Again!')
        g.print_coins()
        while True:
            try:
                option = g.tipo_moedas[int(input('Choose the coin you want do deposit: '))]
                break
            except Exception:
                print('ERROR: Invalid Option')
        # Verificar se é > montante minimo
        while (amount := int(input('Amount: '))) < 5:
            print('ERROR: Value Inferior to Minimum Deposit')
        # Cehck for valid CC
        valid_cc = False
        while not valid_cc:
            cc = input("CC: ")
            if re.search(r'[0-9]{8}', cc):
                valid_cc = True
            else:
                print('Insert a valid CC!')
        try:
            self.sql.register(email=email,user=user,password=password,amount=amount,iban=iban,cc=cc,tipo_moeda=option,montante=amount,bday=bday)
        except Exception:
            print('User Already Exists!')

        print('User sucessfuly registered!')

    def accountManagement(self):
        acc = int(input("""
#################################
        1- Check Balance 
        2- Change Password
        3- Deposit
        4- Withdraw
        5- Convert Currency
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
        elif acc == 5:
            self.sql.checkBalance(self.user.email)
            g.print_coins()
            to_convert = g.tipo_moedas[int(input('Choose the coin you want to convert: '))]
            converted = g.tipo_moedas[int(input('Choose the coin you want to convert to: '))]
            amount = float(input('Amount: '))
            self.sql.convertCoin(self.user.email,to_convert,converted,amount)
        elif acc == 0:
            return
        else:
            print('ERROR: Not a valid option!')