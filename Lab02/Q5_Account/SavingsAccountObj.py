from AccountObj import Account

class SavingsAccount(Account):
    def __init__(self, name, balance, interest_rate):
        super().__init__(name, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        int_rate = self.interest_rate / 100
        interest = self.get_acc_balance() * int_rate
        super().deposit(interest)


