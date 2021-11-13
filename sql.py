import mysql.connector as mysql

class SQL():

    def __init__(self):
        config = {
            "host" : "127.0.0.1",
            "user" : "rasuser",
            "password" : "ras123",
            "database" : "rasdb"
        }
        self.connection = mysql.connect(**config)
        

    def login(self,email,password):
        cursor = self.connection.cursor()

        cursor.execute('SELECT email FROM user WHERE user.email=%(email)s',{'email' : email})
        user = cursor.fetchone()
        if user:
            cursor.execute("SELECT password FROM user WHERE user.email=%(email)s AND user.password = %(password)s", {'email' : email, 'password' : password})
            if cursor.fetchone():
                return True
            else:
                print('Incorrect password!')
                return False
        else:
            print('No user with that email was found!')
            return False

        cursor.close()

    def register(self,**kw):
        cursor = self.connection.cursor()
        values = {
            'email' : kw['email'],
            'name' : kw['user'],
            'password' : kw['password'],
            'debit' : kw['amount']
        }
        cursor.execute("INSERT INTO user VALUES (%(email)s,%(name)s,%(password)s,%(debit)s)",values)
        self.connection.commit()
        cursor.close()