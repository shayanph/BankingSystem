from datetime import date
import pickle


class User:
    def __init__(self, user_id='', pincode=-1, name='', address='', amount=0, limit=2000):
        self.id = user_id
        self.pinCode = pincode
        self.name = name
        self.address = address
        self.amount = amount
        self.transaction_limit = limit
        self.status = True

    def check_balance(self):
        print("Current Balance: " + str(self.amount))

    def deposit(self, amount):
        self.amount += amount

        towrite = "{},{},Deposit,{},{}\n".format(self.id, self.name, amount, date.today().strftime("%d/%m/%Y"))

        transaction_file = open("transactions.csv", 'a')
        transaction_file.write(towrite)
        transaction_file.close()

        user = User(self.id, self.pinCode, self.name, self.address, self.amount, self.transaction_limit)
        self.update_user(user)

    def withdraw(self, amount):
        if amount <= self.amount:
            self.amount -= amount

            towrite = "{},{},Withdraw,{},{}\n".format(self.id, self.name, amount, date.today().strftime("%d/%m/%Y"))

            transaction_file = open("transactions.csv", 'a')
            transaction_file.write(towrite)
            transaction_file.close()

            user = User(self.id, self.pinCode, self.name, self.address, self.amount, self.transaction_limit)
            self.update_user(user)

    def printstatment(self, show=10):
        list_transactions = []
        try:
            with open("transactions.csv", mode="r") as file:
                count = 0
                for line in file:
                    if line.split(',')[0] == self.id:
                        list_transactions.append(line.strip('\n'))
        except FileNotFoundError:
            print("File of transactions not Found")
            return

        # Print in the reverse order to show the latest transactions
        total = len(list_transactions)
        i = total - 1
        while i > total - show and i >= 0:
            print(list_transactions[i])
            i -= 1

    def __str__(self):
        return f"ID: {self.id}\nName: {self.name}\nTransaction Limit: {self.transaction_limit}\nBalance: {self.amount}"

    def transfer(self, uid, amount):
        data_list = []
        found = False
        with open("user_data", mode="rb") as f:
            try:
                while True:
                    data = pickle.load(f)
                    if data.id == uid:
                        found = True
                        self.withdraw(amount)
                        data.deposit(amount)

                    data_list.append(data)
            except EOFError:
                pass
        if found:
            pickle_write = open("user_data", "wb")
            for users in data_list:
                pickle.dump(users, pickle_write)
            pickle_write.close()

            print("Transfer Success")
        else:
            print("No user found against the ID")

    def change_pin(self, newpin):
        user = User(self.id, newpin, self.name, self.address, self.amount, self.transaction_limit)
        self.update_user(user)

    def update_user(self, user):
        list_of_users = []
        found = False
        with open("user_data", mode="rb") as f:
            try:
                while True:
                    data = pickle.load(f)
                    if data.id == user.id:
                        data = user
                    list_of_users.append(data)
            except EOFError:
                pass

        pickle_write = open("user_data", "wb")
        for users in list_of_users:
            pickle.dump(users, pickle_write)
        pickle_write.close()

    def menu(self):
        while True:
            print("#################################")
            menustring = "1.Deposit Amount\n2.Withdraw Amount\n3.Check Balance\n4.Transfer Amount\n5.Change Pin" \
                         "\n6.Check Transaction History\n7.Account statement\n8.Logout" \
                         "\nThank you for using the system build by Shayan Asghar"
            try:
                choice = int(input(menustring + "\nEnter your choice: "))
                if choice == 1:
                    try:
                        print("#################################")
                        amount = int(input("Enter an amount to deposit: "))
                        self.deposit(amount)

                    except ValueError:
                        print("Only Enter Integer values")

                elif choice == 2:
                    try:
                        print("#################################")
                        amount = int(input("Enter an amount to withdraw: "))
                        self.withdraw(amount)

                    except ValueError:
                        print("Only Enter Integer values")
                elif choice == 3:
                    print("#################################")
                    self.check_balance()
                elif choice == 4:
                    print("#################################")
                    uid = input("Enter the ID to transfer balance: ")
                    try:
                        amount = int(input("Enter an amount to transfer: "))
                        if amount > self.transaction_limit:
                            print("Amount is greater than Transaction limit. Cannot Transfer")
                        else:
                            self.transfer(uid, amount)
                    except ValueError:
                        print("Only Enter Integer values")

                elif choice == 5:
                    try:
                        print("#################################")
                        pin = int(input("Enter a new pin: "))
                        self.change_pin(pin)
                    except ValueError:
                        print("Only Enter Integer values")

                elif choice == 6:
                    print("#################################")
                    self.printstatment(100000)
                elif choice == 7:
                    print("#################################")
                    self.printstatment()
                elif choice == 8:
                    break
                else:
                    print("Wrong choice Try again")
            except ValueError:
                print("Pls enter integer input only")
