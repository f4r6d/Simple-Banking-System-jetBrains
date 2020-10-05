import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
conn.commit()

level = 1
def print_menu(level):
    if level == 1:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
    elif level == 2:
        print()
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")

class CreditCard:
    MII = 4
    BIN = 400000
    checksum = None
    balance = 0
    
    def __init__(self):
        self.account_id = random.randrange(0, 999999999)
        self.password = random.randrange(1000, 9999)
        self.card_number = self.BIN * 10000000000 + self.account_id * 10 + self.luhn_digit()
        cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)", (self.card_number, str(self.card_number), self.password, 0))
        
   
    
    def luhn_digit(self):
        digits = list(str(self.BIN * 1000000000 + self.account_id))
        step_one = [int(x) for x in digits]
        for i in range(len(step_one)):
            if i % 2 == 0:
                step_one[i] *= 2  # odd digits * 2
        step_two = [x - 9 if x > 9 else x for x in step_one]  # subtract 9 to numbers over 9
        sum_digits = sum(step_two)  # sum all digits
        if sum_digits % 10 == 0:
            return 0
        else:
            return 10 - (sum_digits % 10)
        
def luhn(cardnum):
    digits = list(str(cardnum))
    step_one = [int(x) for x in digits]
    for i in range(len(step_one)):
        if i % 2 == 0:
            step_one[i] *= 2  # odd digits * 2
    step_two = [x - 9 if x > 9 else x for x in step_one]  # subtract 9 to numbers over 9
    sum_digits = sum(step_two)  # sum all digits
    return sum_digits % 10 == 0
    
def login(card_number, pin):
    cur.execute("SELECT id, pin FROM card;")
    data = cur.fetchall()
    if (card_number, str(pin)) in data:
        print()
        print("You have successfully logged in!")
        global level
        level = 2
    else:
        print()
        print("Wrong card number or PIN!")
        print()

def card_exist(number):
        num_query ="SELECT id FROM card WHERE id={};".format(number)
        cur.execute(num_query)
        if cur.fetchall():
            return True
        
def bal_f(card):
    bal_query = "SELECT balance FROM card WHERE id={};".format(card)
    cur.execute(bal_query)
    balan = cur.fetchall()[0][0]
    return balan
    
def update_balance(new_bal, card_id):
    update_query = "UPDATE card SET balance={} WHERE id={};".format(new_bal, card_id)
    cur.execute(update_query)
    conn.commit()

while level == 1:
    print_menu(1)
    main_option = int(input())
    if main_option == 1:
        new_card = CreditCard()
        conn.commit()
        print()
        print("Your card has been created")
        print("Your card number:")
        print(new_card.card_number)
        print("Your card PIN:")
        print(new_card.password)
        print()
    elif main_option == 2:
        print()
        my_card_number = int(input("Enter your card number:"))
        my_pin = int(input("Enter your PIN:"))
        login(my_card_number, my_pin)
        while level == 2:
            print_menu(2)
            card_option = int(input())
            if card_option == 1:
                bals = bal_f(my_card_number)
                print(f'Balance: {bals}')
            elif card_option == 2:
                print()
                balls = bal_f(my_card_number)
                income = int(input("Enter income:"))
                new_bal = balls + income
                update_balance(new_bal, my_card_number)
                print("Income was added!")
            elif card_option == 3:
                print()
                print("Transfer")
                dest_card = int(input("Enter card number:"))
                if luhn(dest_card):
                    if card_exist(dest_card):
                        if dest_card != my_card_number:
                            amount = int(input("Enter how much money you want to transfer:"))
                            money = bal_f(my_card_number)
                            if amount < money:
                                update_balance(money - amount, my_card_number)
                                dest_money =bal_f(dest_card)
                                update_balance(dest_money + amount, dest_card)
                                print("Success!")
                            else:
                                print("Not enough money!")
                        else:
                            print("You can't transfer money to the same account!")
                    else:
                        print("Such a card does not exist.")
                else:
                    print("Probably you made a mistake in the card number. Please try again!")
                
            elif card_option == 4:
                del_query = "DELETE FROM card WHERE id={}".format(my_card_number)
                cur.execute(del_query)
                conn.commit()
                print()
                print("The account has been closed!")
                print()
                level = 1
            elif card_option == 5:
                print()
                print("You have successfully logged out!")
                print()
                level = 1                
            elif card_option == 0:
                level = 0
                print()
                print("Bye!")            
    elif main_option == 0:
        level = 0
        print()
        print("Bye!")
