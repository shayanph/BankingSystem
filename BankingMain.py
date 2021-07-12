from admin import *


class BankingMain:
    def __init__(self):
        file = open('user_data', 'ab')
        file.close()

        file = open('transactions.csv', 'a')
        file.close()

        self.admin = Admin("Shayan", "Lahore")
        self.user = User()

    def login(self):
        while True:
            login_id = input("Enter Login ID or Enter -1 to exit: ")
            if login_id == '-1':
                break
            while True:
                try:
                    login_pin = int(input("Enter pin code: "))
                    count = 0
                    copy_pin = login_pin
                    while copy_pin != 0:
                        rem = copy_pin % 10
                        count += 1
                        copy_pin = copy_pin // 10

                    if count != 4:
                        print("Pin must be of 4 digits.Try again")
                    else:
                        break
                except ValueError:
                    print("only Digits are allowed")

            if login_id == 'admin' and login_pin == 1234:
                self.admin.menu()
            else:
                found = False
                with open("user_data", mode="rb") as f:
                    try:
                        while True:
                            data = pickle.load(f)
                            if data.id == login_id and data.pinCode == login_pin:
                                found = True
                                self.user = data
                    except EOFError:
                        pass
                if found:
                    if self.user.status:
                        self.user.menu()
                    else:
                        print("Your account Has been Frozen.Pls Contact an Admin")
                else:
                    print("Wrong ID or password given")


if __name__ == '__main__':
    bank = BankingMain()
    bank.login()
