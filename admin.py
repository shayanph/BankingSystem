from user import *


class Admin:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    # Function 1- Create Account
    def create_account(self):
        pickle_data = None

        # Getting the ID from the admin and checking in the file for unique entry
        uid = input("Enter an ID for the user: ")
        try:
            with open("user_data", mode="rb") as f:
                try:
                    while True:
                        data = pickle.load(f)
                        print(data.id)
                        if data.id == uid:
                            print("ID ALREADY EXISTS")
                            return
                except EOFError:
                    pass

            print("ID available")
        except FileNotFoundError:
            print("File of transactions not Found")

        # Getting the pin from the admin
        while 1:
            try:
                pin = int(input("Enter a 4-digit pin code: "))
                count = 0
                copy_pin = pin
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

        # Getting the rest of the data
        name = input("Enter the name of the user: ")
        address = input("Enter the address of the user: ")
        balance = int(input("Enter the starting amount of account: "))
        limit = int(input("Enter the transaction limit: "))

        user = User(uid, pin, name, address, balance, limit)
        # Storing the data into the file using pickle
        pickle_file = open("user_data", "ab")
        pickle.dump(user, pickle_file)
        pickle_file.close()

    # Function 2- Show Transactions
    # Getting the data for transactions from the file
    def show_transactions(self):
        choice = input("Do you want to see a specific user's transactions(Y/N): ")

        if choice == 'y' or choice == 'Y':
            uid = input("Enter the userID: ")
            try:
                with open("transactions.csv", mode="r") as iFile:
                    count = 0
                    for line in iFile:
                        if line.split(',')[0] == uid:
                            print(line)
                            count += 1
                    if count == 0:
                        print("No transactions against the ID were found")
            except FileNotFoundError:
                print("File of transactions not Found")
        else:
            try:
                with open("transactions.csv", mode="r") as iFile:
                    for line in iFile:
                        print(line)
            except FileNotFoundError:
                print("File of transactions not Found")

    # Function 3 : Freeze Account
    def freezeaccount(self, user_id):
        list_of_users = []
        found = False
        with open("user_data", mode="rb") as f:
            try:
                while True:
                    data = pickle.load(f)
                    if data.id == user_id:
                        found = True
                        if data.status:
                            data.status = False
                        else:
                            data.status = True
                    list_of_users.append(data)
            except EOFError:
                pass

        if found:
            pickle_write = open("user_data", "wb")
            for users in list_of_users:
                pickle.dump(users, pickle_write)
            pickle_write.close()

    # Function 4 : Delete Account
    def deleteaccount(self, user_id):
        list_of_users = []
        found = False
        with open("user_data", mode="rb") as f:
            try:
                while True:
                    data = pickle.load(f)
                    if data.id == user_id:
                        found = True
                    else:
                        list_of_users.append(data)
            except EOFError:
                pass

        if found:
            pickle_write = open("user_data", "wb")
            for users in list_of_users:
                pickle.dump(users, pickle_write)
            pickle_write.close()
        else:
            print("No user found against this ID")

    # Function 5 : Set new Account limit
    def setlimit(self, user_id):
        list_of_users = []
        found = False
        with open("user_data", mode="rb") as f:
            try:
                while True:
                    data = pickle.load(f)
                    if data.id == user_id:
                        found = True
                        limit_new = int(input("Enter new limit for the user name " + data.name + ": "))
                        data.transaction_limit = limit_new

                    list_of_users.append(data)
            except EOFError:
                pass

        if found:
            pickle_write = open("user_data", "wb")
            for users in list_of_users:
                pickle.dump(users, pickle_write)
            pickle_write.close()
        else:
            print("No user found against this ID")

    def show_user(self):
        with open("user_data", mode="rb") as f:
            count = 1
            try:
                while True:
                    data = pickle.load(f)
                    print("#################################")
                    print(data)
                    print()
                    count += 1
            except EOFError:
                pass

    def generate_report(self, input_which, type_report, typecash):
        print("#################################")
        if typecash == 1:
            action = "Deposit"
        else:
            action = "Withdraw"

        if type_report == 0:
            print("####Day BASED REPORT#####")
        elif type_report == 1:
            print("####MONTH BASED REPORT#####")
        elif type_report == 2:
            print("####YEAR BASED REPORT#####")

        try:
            input_data = None
            file = open("transactions.csv", "r")
            count = 0
            for lines in file:
                tokenized = lines.strip('\n').split(",")
                if type_report == 0:
                    input_data = int(tokenized[4].split("/")[0])
                elif type_report == 1:
                    input_data = int(tokenized[4].split("/")[1])
                elif type_report == 2:
                    input_data = int(tokenized[4].split("/")[2])

                if input_data == input_which and action == tokenized[2]:
                    print(lines)
                    count += 1

            if count == 0:
                print("No Transactions found")
        except FileNotFoundError:
            print("No transactions found to generate report")

    def menu(self):
        while True:
            print("#################################")
            menuString = "1.Create Account\n2.Show Accounts\n3.Show Transactions\n4.Delete Account\n5.Freeze Account" \
                         "\n6.Set Transactions Limit\n7.View Reports\n8.Logout" \
                         "\nThank you for using the system build by Shayan Asghar"
            try:
                choice = int(input("{0}\nEnter your choice: ".format(menuString)))
                if choice == 1:
                    print("#################################")
                    self.create_account()
                elif choice == 2:
                    print("#################################")
                    self.show_user()
                elif choice == 3:
                    print("#################################")
                    self.show_transactions()
                elif choice == 4:
                    print("#################################")
                    uid = input("Enter the ID to delete: ")
                    self.deleteaccount(uid)
                elif choice == 5:
                    print("#################################")
                    uid = input("Enter the ID to Freeze: ")
                    self.freezeaccount(uid)
                elif choice == 6:
                    print("#################################")
                    uid = input("Enter the ID to change transaction limit: ")
                    self.setlimit(uid)
                elif choice == 7:
                    while 1:
                        try:
                            print("#################################")
                            choiceCash = int(input("Enter the type of report:\n1.Cash in\n2.Cash out\n---->"))
                            choice = int(input("1.By Day.\n2.By Month\n3.By year\n4.Exit\nEnter your choice: "))
                            if choice == 1:
                                day = int(input("Enter a day to see the report(1-31): "))
                                if day < 1 or day > 31:
                                    print("Input out of range")
                                else:
                                    self.generate_report(day, 0, choiceCash)
                            elif choice == 2:
                                month = int(input("Enter a month to see the report(1-12): "))
                                if month < 1 or month > 12:
                                    print("Input out of range")
                                else:
                                    self.generate_report(month, 1, choiceCash)
                            elif choice == 3:
                                year = int(input("Enter a year to see the report: "))
                                self.generate_report(year, 2, choiceCash)
                            elif choice == 4:
                                break
                            else:
                                print("Wrong input try again")
                        except ValueError:
                            print("Only integers allowed")
                elif choice == 8:
                    break
                else:
                    print("#################################")
                    print("Wrong choice Try again")
            except ValueError:
                print("Pls enter integer input only")

