class Account():
    def init(self,owner,balance):
        self.owner=owner
        self.balance=balance
    
    def deposit(self,amount):
        self.balance+=amount
    
    def withdraw(self,amount):
        if(amount>self.balance):
            print("Insufficient Funds")
        else:
            self.balance -= amount
            print(self.balance)


balance,withdraw_amount=map(int,input().split())

acc=Account("User",balance)
acc.withdraw(withdraw_amount)