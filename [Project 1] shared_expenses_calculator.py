global people
people = {}  # Dictionary that stores the amount each person should receive or pay.

def welcome_message():
    print("Welcome to the Debt Settlement Program!")
    print("This program helps you track expenses among a group of people and calculates how much each person owes or is owed.")

def calc_loan(n, amount, participated):
    if participated:
        loan = amount - amount/n
    else:
        loan = amount
    return loan

def count_participants(list):
    return len(list)

def register_purchase(purchase):
    n = count_participants(purchase['participants'])
    loan = calc_loan(n, purchase['amount'], purchase['payer'] in purchase['participants'])
    for name in purchase['participants']:
        if name != purchase['payer']:
            people[name] += purchase['amount']/n
    people[purchase['payer']] -= loan
    return people

def register_people():
    while True:
        try:
            num_people = int(input("How many people will participate? "))
            break
        except ValueError:
            print("Please enter a valid number.")

    for i in range(num_people):
        name = input(f"Enter the name of person {i + 1}: ")
        people[name] = 0

def register_purchases():
    num_purchases = 1
    while True:
        participants = input(f"Enter the participants of purchase {num_purchases} separated by commas: ").split(", ")

        while True:
            try:
                amount = float(input(f"Enter the amount of purchase {num_purchases}: "))
                break
            except ValueError:
                print("Please enter a valid numeric value.")

        payer = input(f"Who paid for purchase {num_purchases}? ")
        purchase = {'participants': participants, 'amount': amount, 'payer': payer}
        register_purchase(purchase)

        more_purchases = input("Do you want to register another purchase? (y/n): ")
        if more_purchases.lower() != 'y':
            break
        num_purchases += 1

def show_balances():
    print("\nFinal balances:")
    for person, balance in people.items():
        print(f"{person}: {balance:.2f}")

def calculate_transactions():
    creditors = [(person, balance) for person, balance in people.items() if balance < 0]
    debtors = [(person, balance) for person, balance in people.items() if balance > 0]

    transactions = []

    while creditors and debtors:
        creditor, amount_to_receive = creditors.pop(0)
        debtor, amount_to_pay = debtors.pop(0)

        transaction_amount = min(abs(amount_to_receive), amount_to_pay)
        transactions.append(f"{debtor} must transfer {transaction_amount:.2f} to {creditor}")

        new_balance_creditor = amount_to_receive + transaction_amount
        new_balance_debtor = amount_to_pay - transaction_amount

        if new_balance_creditor < 0:
            creditors.append((creditor, new_balance_creditor))
        if new_balance_debtor > 0:
            debtors.append((debtor, new_balance_debtor))

    print("\nNecessary transactions to settle debts:")
    for transaction in transactions:
        print(transaction)

def exit_program():
    while True:
        exit_choice = input("\nDo you want to exit the program? (y/n): ")
        if exit_choice.lower() in ['y', 'n']:
            break
        print("Please enter 'y for yes or 'n' for no.")

# Executes the registration of people and purchases
welcome_message()
register_people()
register_purchases()
show_balances()
calculate_transactions()
exit_program()
