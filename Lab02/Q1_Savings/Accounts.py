class Savings:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def account_info(self):
        print("Name : {0} \t Balance: {1}".format(self.name, self.balance))


    def get_acc_name(self):
        return self.name

    def get_acc_balance(self):
        return self.balance

    def deposit(self, amt):
        self.balance += amt
        print("You have successfully deposit £{0}".format(amt))
        print("Your new balance is £{0}".format(self.balance))

    def withdraw(self,amt):
        if self.balance <=0 or amt >= self.balance:
            print("Sorry, insufficient funds avaliable, Your balance {0}".format(self.balance))
        else:
            self.balance -= amt
            print("${0} - Withdraw, your new balance is ${1}".format(amt, self.balance))
