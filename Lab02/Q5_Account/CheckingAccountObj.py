from AccountObj import Account


class CheckAccount(Account):
    def __init__(self, name, balance, overdraft_limit):
        super().__init__(name, balance)
        self.__overdraft_limit = overdraft_limit

    def withdraw(self, amt):
        limit = self.get_acc_balance() + self.__overdraft_limit
        if limit - amt < 0:
            print("Your over the overdraft limit is {0}".format(self.__overdraft_limit))
        else:
            self.set_balance(self.get_acc_balance() - amt)
            print("Your new balance is: {0}".format(self.get_acc_balance()))
