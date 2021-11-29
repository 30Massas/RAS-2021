class User():

    def __init__(self):
        self.email = ""
        self.password = ""
        self.bets = []

    def setCredentials(self,email,password):
        self.email = email
        self.password = password