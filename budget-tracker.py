import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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

    def save_transactions(self):
        with open(DATA_FILE, 'w') as f:
            json.dump([t.__dict__ for t in self.transactions], f)

    def load_transactions(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                transactions_data = json.load(f)
                self.transactions = [Transaction(**t_data) for t_data in transactions_data]

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def show_add_transaction(frame, is_income):
    clear_frame(frame)
    
    title = "Add Income" if is_income else "Add Expense"
    ttk.Label(frame, text=title, font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    ttk.Label(frame, text="Amount:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    amount_entry = ttk.Entry(frame)
    amount_entry.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)

    ttk.Label(frame, text="Category:").grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
    category_entry = ttk.Entry(frame)
    category_entry.grid(row=2, column=1, padx=10, pady=10, sticky=tk.EW)

    def submit():
        try:
            amount = float(amount_entry.get())
            category = category_entry.get()
            if not category:
                messagebox.showerror("Error", "Category cannot be empty.")
                return
            budget_tracker.add_transaction(amount, category, is_income)
            messagebox.showinfo("Success", f"{title} added successfully.")
            clear_frame(frame)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered.")

    ttk.Button(frame, text="Submit", command=submit).grid(row=3, column=0, columnspan=2, pady=20)

def show_transactions(frame):
    clear_frame(frame)
    
    ttk.Label(frame, text="Transactions", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)
    
    transactions = "\n".join(f"{i+1}. {t}" for i, t in enumerate(budget_tracker.transactions))
    text = transactions if transactions else "No transactions available."
    ttk.Label(frame, text=text).grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NW)

def show_budget(frame):
    clear_frame(frame)
    
    ttk.Label(frame, text="Budget", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)
    
    budget = budget_tracker.calculate_budget()
    ttk.Label(frame, text=f"Remaining Budget: Rs.{budget:.2f}").grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NW)

def show_expenses_analysis(frame):
    clear_frame(frame)
    
    ttk.Label(frame, text="Expense Analysis", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=10)
    
    expense_summary = budget_tracker.analyze_expenses()
    if expense_summary:
        analysis = "\n".join(f"{category}: Rs.{total:.2f}" for category, total in expense_summary.items())
        ttk.Label(frame, text=analysis).grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NW)
    else:
        ttk.Label(frame, text="No expenses recorded.").grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=tk.NW)

def main():
    global budget_tracker
    budget_tracker = BudgetTracker()

    root = tk.Tk()
    root.title("Budget Tracker")
    root.geometry("600x400")
    root.minsize(600, 400)

    # Style
    style = ttk.Style()
    style.configure("TButton", padding=10, relief="flat", background="#ccc")
    style.configure("TFrame", padding=20)
    style.configure("TLabel", padding=10)

    # Main Frame
    main_frame = ttk.Frame(root, padding="20 20 20 20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Title Label
    title_label = ttk.Label(main_frame, text="Budget Tracker", font=("Helvetica", 16))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Buttons Frame
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)

    # Content Frame
    content_frame = ttk.Frame(main_frame, borderwidth=1, relief="solid")
    content_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(1, weight=1)

    # Buttons
    ttk.Button(buttons_frame, text="Add Income", command=lambda: show_add_transaction(content_frame, True)).grid(row=0, column=0, sticky=tk.W+tk.E, pady=10)
    ttk.Button(buttons_frame, text="Add Expense", command=lambda: show_add_transaction(content_frame, False)).grid(row=1, column=0, sticky=tk.W+tk.E, pady=10)
    ttk.Button(buttons_frame, text="View Transactions", command=lambda: show_transactions(content_frame)).grid(row=2, column=0, sticky=tk.W+tk.E, pady=10)
    ttk.Button(buttons_frame, text="View Budget", command=lambda: show_budget(content_frame)).grid(row=3, column=0, sticky=tk.W+tk.E, pady=10)
    ttk.Button(buttons_frame, text="Analyze Expenses", command=lambda: show_expenses_analysis(content_frame)).grid(row=4, column=0, sticky=tk.W+tk.E, pady=10)
    ttk.Button(buttons_frame, text="Exit", command=root.quit).grid(row=5, column=0, sticky=tk.W+tk.E, pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()

