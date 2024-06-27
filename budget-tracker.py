import json
import os

DATA_FILE = 'transactions.json'

class Transaction:
    def __init__(self, amount, category, is_income):
        self.amount = amount
        self.category = category
        self.is_income = is_income

    def __repr__(self):
        type_ = "Income" if self.is_income else "Expense"
        return f"{type_}: {self.category} - Rs.{self.amount:.2f}"

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.load_transactions()

    def add_transaction(self, amount, category, is_income):
        transaction = Transaction(amount, category, is_income)
        self.transactions.append(transaction)
        self.save_transactions()

    def calculate_budget(self):
        total_income = sum(t.amount for t in self.transactions if t.is_income)
        total_expense = sum(t.amount for t in self.transactions if not t.is_income)
        return total_income - total_expense

    def analyze_expenses(self):
        expense_summary = {}
        for t in self.transactions:
            if not t.is_income:
                if t.category not in expense_summary:
                    expense_summary[t.category] = 0
                expense_summary[t.category] += t.amount
        return expense_summary

    def display_transactions(self):
        if not self.transactions:
            print("No transactions available.")
        for i, transaction in enumerate(self.transactions):
            print(f"{i+1}. {transaction}")

    def save_transactions(self):
        with open(DATA_FILE, 'w') as f:
            json.dump([t.__dict__ for t in self.transactions], f)

    def load_transactions(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                transactions_data = json.load(f)
                self.transactions = [Transaction(**t_data) for t_data in transactions_data]

def main():
    budget_tracker = BudgetTracker()

    while True:
        print("\nBudget Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. View Budget")
        print("5. Analyze Expenses")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            amount = float(input("Enter income amount: "))
            category = input("Enter income category: ")
            budget_tracker.add_transaction(amount, category, True)
        elif choice == '2':
            amount = float(input("Enter expense amount: "))
            category = input("Enter expense category: ")
            budget_tracker.add_transaction(amount, category, False)
        elif choice == '3':
            budget_tracker.display_transactions()
        elif choice == '4':
            budget = budget_tracker.calculate_budget()
            print(f"Remaining Budget: Rs.{budget:.2f}")
        elif choice == '5':
            expense_summary = budget_tracker.analyze_expenses()
            print("Expense Analysis:")
            for category, total in expense_summary.items():
                print(f"{category}: Rs.{total:.2f}")
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
