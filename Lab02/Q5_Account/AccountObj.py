class Account:
    def __init__(self, name, balance):
        self.__name = name
        self.__balance = balance

    def account_info(self):
        print("-- Account Details -- \n Name: {0} \n Balance: ${1}".format(self.__name, self.__balance))

    def get_acc_name(self):
        return self.__name

    def get_acc_balance(self):
        return self.__balance

    def deposit(self, amt):
        self.__balance += amt
        print("You have successfully deposited, Your balance is: ${0}".format(self.get_acc_balance()))

    def set_balance(self, new_balance):
        self.__balance = new_balance

    def withdraw(self, amt):
        if amt > self.get_acc_balance() or amt == 0:
            print("You dont have that much in your account \n Balance: ${0}".format(self.get_acc_balance()))
        else:
            new_balance = self.get_acc_balance() - amt
            self.set_balance(new_balance)
            print("You have successfully take ${0} \n Your new Balance: ${1}".format(amt, self.get_acc_balance()))
