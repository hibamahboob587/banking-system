import csv
import random
import datetime
from datetime import datetime
from abc import ABC,abstractmethod
class Account:
    def __init__(self,balance):
        self.balance = balance

    def deposit(self):
        pass

    def withdraw(self):
        pass

    def bank_enquiry(self):
        return self.balance

class Currentbalance(ABC):
    @abstractmethod
    def get_currentbalance(self):
        pass

class CheckingAccount(Account,Currentbalance):
    def __init__(self,username,password,balance=0,credit_limit=-1000, overdraft_fee=500):
        super().__init__(balance)
        self.ins_customer = Customer()
        self.credit_limit = credit_limit
        self.overdraft_fee = overdraft_fee
        self.username = username
        self.password = password
        self.account_name = "Checking"
        self.ins_customer.user_data.append(self.account_name)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ins_customer.user_data.append(timestamp)

    def get_currentbalance(self):
        return print(f'your current balance is:{self.balance}')

    def deposit(self):
        self.ins_customer.user_data.append(self.balance)
        with open('checking.csv', 'r+', newline='') as file:
            customer_data = csv.reader(file)
            data = list(customer_data)
            for row in data:
                if self.username in row and self.password in row:
                    self.dep = int(input("How much money do you want to deposit?: "))
                    balance = float(row[8])
                    self.balance = balance
                    self.balance += self.dep
                    row[8] = str(self.balance)
                    self.get_currentbalance()

                    break
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(data)
            file.truncate()

   
    def withdraw(self):

        with open('checking.csv', 'r+', newline='') as file:
            customer_data = csv.reader(file)
            data = list(customer_data)
            for row in data:
                if self.username in row and self.password in row:
                    balance = float(row[8])
                    self.balance = balance
                    self.drawout = int(input("How much money do you want to withdraw?: "))
                    if self.balance < self.drawout:
                        if self.balance > self.credit_limit:
                            choose = input("Your balance is less than your withdrawal which means that youre"
                                           "gonna be charged with an overdraft fee.\nDo you wish to proceed?: ").lower()
                            try:
                                if choose == "y":
                                    self.balance -= self.drawout
                                    self.balance -= self.overdraft_fee
                                    row[8] = str(self.balance)
                                    self.get_currentbalance()
                                elif choose == "n":
                                    print("Transaction canceled. Thank you!")
                                else:
                                    raise ValueError("Invalid input.")

                            except ValueError as error:
                                print(str(error))
                           


                    else:
                        balance = float(row[8])
                        self.balance = balance
                        self.balance -= self.drawout
                        self.balance -= self.overdraft_fee
                        row[8] = str(self.balance)
                        self.get_currentbalance()

                        break

     
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(data)
            file.truncate()

       

    def create(self):
        self.ins_customer.data()
        self.ins_customer.user_data.append(self.balance)
        with open("checking.csv", 'a+', newline='') as file:
            write = csv.writer(file)
            write.writerow(self.ins_customer.user_data)

class SavingAccount(Account,Currentbalance):
    def __init__(self,username,password, balance=0, interest_rate=0.05):
        super().__init__(balance)
        self.username = username
        self.password = password
        self.interest_rate = interest_rate
        self.ins_customer = Customer()
        self.account_name = "Saving"
        self.ins_customer.user_data.append(self.account_name)
        self.calculate_interest_rate()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ins_customer.user_data.append(timestamp)

    def get_currentbalance(self):
        return print(f'your current balance is:{self.balance}')

    def withdraw(self): # overriding withdraw method
        self.ins_customer.user_data.append(self.balance)
        with open('savings.csv', 'r+', newline='') as file:
            customer_data = csv.reader(file)
            data = list(customer_data)
            for row in data:
                if self.username in row and self.password in row:
                    balance = float(row[8])
                    self.balance=balance
                    self.drawout = int(input("How much money do you want to withdraw?: "))
                    self.balance -= self.drawout
                    row[8] = str(self.balance)
                    self.get_currentbalance()

                    break
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(data)
            file.truncate()


    def deposit(self):
        self.ins_customer.user_data.append(self.balance)
        with open('savings.csv', 'r+', newline='') as file:
            customer_data = csv.reader(file)
            data = list(customer_data)
            for row in data:
                if self.username in row and self.password in row:
                    balance = float(row[8])
                    self.balance = balance
                    self.dep = int(input("How much money do you want to deposit?: "))
                    self.balance = self.dep
                    row[8] = str(self.balance)
                    self.calculate_interest_rate()
                    self.get_currentbalance()
                    break

            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(data)
            file.truncate()

    def calculate_interest_rate(self):
        with open('savings.csv', 'r+', newline='') as file:
            customer_data = csv.reader(file)
            data = list(customer_data)
            for row in data:
                if self.username in row and self.password in row:
                    balance = float(row[8])
                    self.balance = balance
                    calculations = self.balance * self.interest_rate
                    self.balance += round(calculations)
                    row[8] = str(self.balance)
                    self.get_currentbalance()
                    self.get_interested_amount()
                    break
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(data)
            file.truncate()
    def get_interested_amount(self):
        return f"Your balance with monthly profit will be Rs {self.balance}"
    def create(self):
        self.ins_customer.data()
        self.ins_customer.user_data.append(self.balance)
        with open("savings.csv", 'a+',newline='') as sfile:
            write = csv.writer(sfile)
            write.writerow(self.ins_customer.user_data)

class LoanAccount(Account,Currentbalance):
    def __init__(self,username,password,balance=0,interest_rate=0.05, loan_duration = 12,principal=0 ):
        super().__init__(balance)
        self.password = password
        self.username = username
        self.interest_rate = interest_rate
        self.loan_duration = loan_duration
        self.principal =principal
        self.ins_customer = Customer()
        self.account_name = "Loan"
        self.ins_customer.user_data.append(self.account_name)
        self.ins_customer.user_data.append(self.principal)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ins_customer.user_data.append(timestamp)

    def get_currentbalance(self):
        return print(f"your current balance is:{self.balance}")

    def option(self):
        

        choice = input("do you want to pay installment?:").lower()
        if choice == "y":
            self.installment()
        elif choice =="n":
            with open('loan.csv', 'r+', newline="") as file:
                customer_data = csv.reader(file)
                data = list(customer_data)
                for row in data:
                    if self.username in row and self.password in row:
                        # principal = float(row[1])
                        # self.principal = principal
                        self.principal = int(input("how much money do you want to borrow?:"))
                        row[1] = str(self.principal)
                        break
                file.seek(0)
                writer = csv.writer(file)
                writer.writerows(data)
                file.truncate()
            self.calculate()

    def calculate(self):
        with open('loan.csv', 'r+',newline="") as file:
            customer_data = csv.reader(file)
            data = list(customer_data)
            for row in data:
                if self.username in row and self.password in row:
                    principal = float(row[1])
                    balance = float(row[9])
                    self.balance = balance
                    self.principal = principal
                    monthly_interest = (self.principal / self.loan_duration) + (
                            self.interest_rate / self.loan_duration) * self.principal
                    self.balance -= monthly_interest
                    row[9] = str(self.balance)
                    self.get_currentbalance()
                    break
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(data)
            file.truncate()

    def installment(self):
        try:
            with open('loan.csv', 'r+', newline="") as file:
                customer_data = csv.reader(file)
                data = list(customer_data)
                for row in data:
                    if self.username in row and self.password in row:
                        balance = float(row[9])
                        self.balance = balance
                        installment_amount = int(input("How much money do you want to pay? "))
                        self.balance += installment_amount
                        print("Payment successful!")
                        row[9] = str(self.balance)
                        self.get_currentbalance()
                        b = float(row[9])
                        p = float(row[1])
                        if b == p:
                            print("LOAN PAID")
                        elif b > p:
                            b -= p
                            print(f"LOAN PAID!.you paid more than the principal amount. your current balance is:{b}")
                            row[9] = str(b)
                        break

                else:
                    print("Customer not found.")

                file.seek(0)
                writer = csv.writer(file)
                writer.writerows(data)
                file.truncate()
        except ValueError:
            print("Invalid input for installment amount.")

    def create(self):
        self.ins_customer.data()
        self.ins_customer.user_data.append(self.balance)
        with open("loan.csv", 'a+',newline='') as lfile:
            write = csv.writer(lfile)
            write.writerow(self.ins_customer.user_data)

class Customer:
    user_data = []
    def data(self):
        username= str(input("Enter your username:"))
        self.user_data.append(username)
        password = str(input("Enter your password:"))
        self.user_data.append(password)
        Fname = str(input("Enter your first name:"))
        self.user_data.append(Fname)
        Lname = str(input("Enter your last name:"))
        self.user_data.append(Lname)
        address = str(input("Enter your address:"))
        self.user_data.append(address)
        acc_no = random.randrange(1000000000, 9999999999)
        string = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        c = str(acc_no) + random.choice(string)
        print(f'Account no: {c}')
        a = str(c)
        self.user_data.append(f"{a}")

class Report:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def saving(self):
        with open('savings.csv', 'r') as file:
            lines = csv.reader(file)
            for line in lines:
                if self.username in line and self.password in line:
                    print(f"User found with username: {self.username}")
                    print(f"User data: {line}")
                    break


    def checking(self):
        with open('checking.csv', 'r') as file:
            lines = csv.reader(file)
            for line in lines:
                if self.username in line and self.password in line:
                    print(f"User found with username: {self.username}")
                    print(f"User data: {line}")
                    break

    def loan(self):
        with open('loan.csv', 'r') as file:
            lines = csv.reader(file)
            for line in lines:
                if self.username in line and self.password in line:
                    print(f"User found with username: {self.username}")
                    print(f"User data: {line}")
                    break

class Transfer(Account):
    def __init__(self,money,balance=0):
        super().__init__(balance)
        self.money = money
        self.balance = balance
        self.ins_customer = Customer()

            # rows = list(csv.reader(file))
            # for row in rows:
            #     if account in row:
            #
            #         balance = float(row[9])
            #         self.balance = balance
            #         self.balance += self.money
            #         row[9] = str(self.balance)
            #         break
            #
            # file.seek(0)
            # writer = csv.writer(file)
            # writer.writerows(rows)
            # file.truncate()
    def saving(self):
        account = input("ENTER THE ACCOUNT NO. OF RECIPIENT")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ins_customer.user_data.append(timestamp)
        with open('savings.csv', 'r+', newline='') as file:
            lines = list(csv.reader(file))
            for line in lines:
                if account in line :
                    balance = float(line[8])
                    self.balance = balance
                    self.balance += self.money
                    line[8] = str(self.balance)
                    break
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(lines)
            file.truncate()

    def checking(self):
        account = input("ENTER THE ACCOUNT NO. OF RECIPIENT")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ins_customer.user_data.append(timestamp)
        with open('checking.csv', 'r+', newline='') as file:
            lines = list(csv.reader(file))
            for line in lines:
                if account in line:
                    balance = float(line[8])
                    self.balance = balance
                    self.balance += self.money
                    line[8] = str(self.balance)
                    break

            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(lines)
            file.truncate()

    def loan(self):
        account = input("ENTER THE ACCOUNT NO. OF RECIPIENT")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ins_customer.user_data.append(timestamp)
        with open('loan.csv', 'r+', newline='') as file:
            lines = list(csv.reader(file))
            for line in lines:
                if account in line:
                    balance = float(line[9])
                    self.balance = balance
                    self.balance += self.money
                    line[9] = str(self.balance)
                    break
            file.seek(0)
            writer = csv.writer(file)
            writer.writerows(lines)
            file.truncate()

class Interface:

    @staticmethod
    def menu():
        print("1.Withdraw amount")
        print("2.Deposit amount")
        print("3.view transaction history")
        print("4.Transfer Funds")

    def Accfunc(self):
        print("1.checking account")
        print("2.savings account")
        print("3.loan account")
        login = int(input("which account do you want to log in to?:"))
        if login == 1:
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            with open('checking.csv', 'r') as file:
                lines = csv.reader(file)
                check = False
                for line in lines:
                    if username in line and password in line:
                        check = True
                        break
            if check:
                Interface.menu()
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    c = CheckingAccount(username,password)
                    c.withdraw()
                elif choice == 2:
                    d = CheckingAccount(username,password)
                    d.deposit()
                elif choice == 3:
                    r = Report(username,password)
                    r.checking()
                else:
                    money = float(input("Enter amount to transfer"))
                    where = input("where do you want to transfer money?:").title()
                    if where == "Saving":
                        t = Transfer(money)
                        t.saving()
                    elif where == "Checking":
                        t = Transfer(money)
                        t.checking()
                    else:
                        t = Transfer(money)
                        t.loan()

                    with open('checking.csv', 'r+', newline='') as file:
                        lines = list(csv.reader(file))
                        for line in lines:
                            if username in line and password in line:
                                balance = float(line[8])
                                balance -= money
                                line[8] = str(balance)

                        file.seek(0)
                        writer = csv.writer(file)
                        writer.writerows(lines)
                        file.truncate()


        elif login == 2:
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            with open('savings.csv', 'r') as file:
                lines = csv.reader(file)
                check = False
                for line in lines:
                    if username in line and password in line:
                        check = True
                        break
            if check:
                Interface.menu()
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    withdraws = SavingAccount(username,password)
                    withdraws.withdraw()
                elif choice == 2:
                    deposits = SavingAccount(username,password)
                    deposits.deposit()
                elif choice == 3:
                    r = Report(username,password)
                    r.saving()
                else:
                    money = float(input("Enter amount to transfer"))
                    where = input("where do you want to transfer money?:").title()
                    if where == "Saving":
                        t = Transfer(money)
                        t.saving()
                    elif where == "Checking":
                        t = Transfer(money)
                        t.checking()
                    else:
                        t = Transfer(money)
                        t.loan()

                    with open('savings.csv', 'r+', newline='') as file:
                        lines = csv.reader(file)
                        for line in lines:
                            if username in line and password in line:
                                balance = float(line[8])
                                balance -= money
                                line[8] = str(balance)

                                break

                        file.seek(0)
                        writer = csv.writer(file)
                        writer.writerows(lines)
                        file.truncate()



        elif login == 3:
            username = input('Enter your username: ')
            password = input('Enter your password: ')
            with open('loan.csv', 'r') as file:
                lines = csv.reader(file)
                check = False
                for line in lines:
                    if username in line and password in line:
                        check = True
                        break
            if check:
                Interface.menu()
                choice = int(input("Enter your choice:"))
                if choice == 1:
                    print("invalid")
                elif choice == 2:
                    l = LoanAccount(username,password)
                    l.option()
                elif choice == 3:
                    r = Report(username,password)
                    r.loan()
                else:
                    print("can't transfer money from loan account")


###########################################################################################################

# with open("checking.csv", 'w', newline='') as file:
#     fieldnames = ["Account type","time","username","password","first name","last name","address","Account no.","balance"]
#     writer = csv.writer(file)
#     writer.writerow(fieldnames)
#     pass

# with open("savings.csv",'w', newline='')as file:
#     fieldnames = ["Account type","time", "username", "password", "first name", "last name", "address",
#                   "Account no.","balance"]
#     writer2 = csv.writer(file)
#     writer2.writerow(fieldnames)
#     pass

# with open("loan.csv",'w', newline='') as file:
#     fieldnames = ["Account type","time","principal amount", "username", "password", "first name", "last name", "address",
#                   "Account no.","balance"]
#     writer3 = csv.writer(file)
#     writer3.writerow(fieldnames)
#     pass

########################################################################################################

print("*******************")
print("ONLINE BANKING")
print("*******************")

def main():
    a = str(input("Are you a customer?:")).lower()
    if a == "y" :
        ask = input("do you want to create new account?:").lower()
        if ask == "y":
            print("1.checking account")
            print("2.savings account")
            print("3.loan account")
            new = int(input("which account do you want to log in to?:"))
            if new == 1:
                c = CheckingAccount(None, None, 0, 0, 0)
                c.create()
            elif new == 2:
                s = SavingAccount(None, None, 0, 0)
                s.create()
            elif new == 3:
                l = LoanAccount(0, 0, 0)
                l.create()
            else:
                print("invalid input")

        elif ask == "n":
            i = Interface()
            i.Accfunc()

    elif a == "n":
        print("WELCOME")
        p = "admin01"
        password = input("Enter password:")
        if password == p:
            def transaction():
                print("1.print report of a particular user")
                print("2.print report of all customers")
                choice = int(input("Enter your choice:"))
                if choice == 1:
                    acc_type = input("account type of the user:").title()
                    username = input("Enter username:")
                    password = input("Enter password:")
                    if acc_type == "Saving":
                        with open('savings.csv', 'r') as file:
                            lines = list(csv.reader(file))
                            for line in lines:
                                if username in line and password in line:
                                    print(line)
                                    break
                    elif acc_type == "Checking":
                        with open('checking.csv', 'r') as file:
                            lines = list(csv.reader(file))
                            for line in lines:
                                if username in line and password in line:
                                    print(line)
                                    break
                    else:
                        with open('loan.csv', 'r') as file:
                            lines = list(csv.reader(file))
                            for line in lines:
                                if username in line and password in line:
                                    print(line)
                                    break
                elif choice == 2:
                    account = input("Enter the Account type you want to view:").title()
                    if account == "Saving":
                        with open('savings.csv', 'r') as file:
                            lines = list(csv.reader(file))
                            for line in lines:
                                print(line)


                    elif account == "Checking":
                        with open('checking.csv', 'r') as file:
                            lines = list(csv.reader(file))
                            for line in lines:
                                print(line)


                    elif account == "Loan":
                        with open('loan.csv', 'r') as file:
                            lines = list(csv.reader(file))
                            for line in lines:
                                print(line)


            transaction()


        else:
            print("invalid input ")
main()

