from Accounts import Savings


def main():
    print("Savings Bank")
    hp_account = Savings("Harry Potter", 1000)
    hp_account.account_info()
    hp_account.withdraw(250)
    hp_account.withdraw(250)
    hp_account.withdraw(250)
    hp_account.withdraw(250)

    hp_account.deposit(150)

    hp_account.account_info()


if __name__ == '__main__':
    main()
