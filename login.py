from sql import SQL
from user import User
import globals as g
import re, datetime, pwinput
from dateutil.relativedelta import relativedelta

class Login():

    def __init__(self):
        self.logged = False
        self.user = User()
        self.sql = SQL()

    def login(self):
        email = input(f'{g.bcolors.OKBLUE}Email: {g.bcolors.ENDC}')
        #password = input(f'Password: ')
        password = pwinput.pwinput(prompt=f'{g.bcolors.OKBLUE}Password: {g.bcolors.ENDC}',mask='*')
        if self.sql.login(email=email,password=password):
            self.user.setCredentials(email,password)
            self.logged = True
        else:
            self.logged = False

    def register(self):
        valid_email = False
        while not valid_email:
            email = input(f'{g.bcolors.OKBLUE}Email: {g.bcolors.ENDC}')
            if re.search(r'[a-zA-Z0-9].*@.*\.(pt|com)', email):
                valid_email = True
            else:
                print(f'{g.bcolors.WARNING}Insert a valid email!{g.bcolors.ENDC}')
        valid_user = False
        while not valid_user:
            if (user := input(f'{g.bcolors.OKBLUE}Username: {g.bcolors.ENDC}')) != '':
                valid_user = True
            else:
                print(f'{g.bcolors.WARNING}Insert a valid username!{g.bcolors.ENDC}')
        valid_password = False
        while not valid_password:
            if (password := input(f'{g.bcolors.OKBLUE}Password: {g.bcolors.ENDC}')) != '':
                valid_password = True
            else:
                print(f'{g.bcolors.WARNING}Insert a valid password!{g.bcolors.ENDC}')
        # Verificar se IBAN é valido
        valid_iban = False
        while not valid_iban:
            iban = input(f'{g.bcolors.OKBLUE}IBAN: {g.bcolors.ENDC}')
            if re.search(r'[A-Z]{2}[0-9]{23}', iban):
                valid_iban = True
            else:
                print(f'{g.bcolors.WARNING}Insert a valid IBAN!{g.bcolors.ENDC}')
        bday_form_correct = False
        while not bday_form_correct:
            bday = input(f'{g.bcolors.OKBLUE}Enter your birthday (YYYY-MM-DD): {g.bcolors.ENDC}')
            if re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', bday):
                # Verificar se >18 e <100
                today = datetime.date.today()
                compare = datetime.date.fromisoformat(bday)
                years = relativedelta(today,compare)
                if years.years >= 18 and years.years <= 100:
                    bday_form_correct = True
                else:
                    print(f'{g.bcolors.WARNING}You can not register!{g.bcolors.ENDC}')
                    return
            else:
                print(f'{g.bcolors.WARNING}Wrong Date Format! Please try again!{g.bcolors.ENDC}')
        g.print_coins()
        while True:
            try:
                option = g.tipo_moedas[int(input(f'{g.bcolors.OKBLUE}Choose the coin you want do deposit: {g.bcolors.ENDC}'))]
                break
            except Exception:
                print(f'{g.bcolors.WARNING}ERROR: Invalid option!{g.bcolors.ENDC}')
        # Verificar se é > montante minimo
        while (amount := int(input(f'{g.bcolors.OKBLUE}Amount (min: 5): {g.bcolors.ENDC}'))) < 5:
            print(f'{g.bcolors.WARNING}ERROR: Value Inferior to Minimum Deposit{g.bcolors.ENDC}')
        # Cehck for valid CC
        valid_cc = False
        while not valid_cc:
            cc = input(f"{g.bcolors.OKBLUE}CC: {g.bcolors.ENDC}")
            if re.search(r'[0-9]{8}', cc):
                valid_cc = True
            else:
                print(f'{g.bcolors.WARNING}Insert a valid CC!{g.bcolors.ENDC}')
        try:
            self.sql.register(email=email,user=user,password=password,amount=amount,iban=iban,cc=cc,tipo_moeda=option,montante=amount,bday=bday)
        except Exception:
            print(f'{g.bcolors.WARNING}User Already Exists!{g.bcolors.ENDC}')

        print(f'{g.bcolors.OKGREEN}User sucessfuly registered!{g.bcolors.ENDC}')

    def accountManagement(self):
        acc = int(input(f"""{g.bcolors.OKBLUE}#################################{g.bcolors.ENDC}"""
+f"""\n        1- {g.bcolors.OKGREEN}Check Balance{g.bcolors.ENDC}""" 
+f"""\n        2- {g.bcolors.OKGREEN}Change Password{g.bcolors.ENDC}"""
+f"""\n        3- {g.bcolors.OKGREEN}Deposit{g.bcolors.ENDC}"""
+f"""\n        4- {g.bcolors.OKGREEN}Withdraw{g.bcolors.ENDC}"""
+f"""\n        5- {g.bcolors.OKGREEN}Convert Currency{g.bcolors.ENDC}"""
+f"""\n        0- {g.bcolors.OKGREEN}Exit{g.bcolors.ENDC}"""
+f"""\n{g.bcolors.OKBLUE}#################################{g.bcolors.ENDC}"""
+f"""\n{g.bcolors.HEADER}Option: {g.bcolors.ENDC}"""))
        if acc == 1:
            self.sql.checkBalance(self.user.email)
        elif acc == 2:
            old_pass = input(f"{g.bcolors.OKBLUE}Enter old password: {g.bcolors.ENDC}")
            if old_pass == self.user.password:
                new_pass = input(f"{g.bcolors.OKBLUE}Enter new password: {g.bcolors.ENDC}")
                confirm_pass = input(f"{g.bcolors.OKBLUE}Confirm new password: {g.bcolors.ENDC}")
                if new_pass == confirm_pass:
                    self.sql.changePassword(new_pass,self.user.email)
        elif acc == 3:
            g.print_coins()
            option = g.tipo_moedas[int(input('Choose the coin you want do deposit: '))]
            amount = int(input(f'{g.bcolors.OKBLUE}Amount: {g.bcolors.ENDC}'))
            self.sql.deposit(self.user.email,option,amount)
            print(f'{g.bcolors.OKGREEN}Deposit successfull!{g.bcolors.ENDC}')
        elif acc == 4:
            self.sql.checkBalance(self.user.email)
            g.print_coins()
            option = g.tipo_moedas[int(input('Choose the coin you want do withdraw: '))]
            amount = int(input(f'{g.bcolors.OKBLUE}Amount: {g.bcolors.ENDC}'))
            self.sql.withdraw(self.user.email,option,amount)
            print(f'{g.bcolors.OKGREEN}Withdraw successfull!{g.bcolors.ENDC}')
        elif acc == 5:
            self.sql.checkBalance(self.user.email)
            g.print_coins()
            to_convert = g.tipo_moedas[int(input(f'Choose the coin you want {g.bcolors.BOLD}to convert{g.bcolors.ENDC}: '))]
            converted = g.tipo_moedas[int(input(f'Choose the coin you want {g.bcolors.BOLD}to convert to{g.bcolors.ENDC}: '))]
            amount = float(input(f'{g.bcolors.OKBLUE}Amount: {g.bcolors.ENDC}'))
            self.sql.convertCoin(self.user.email,to_convert,converted,amount)
        elif acc == 0:
            return
        else:
            print(f'{g.bcolors.WARNING}ERROR: Invalid option!{g.bcolors.ENDC}')