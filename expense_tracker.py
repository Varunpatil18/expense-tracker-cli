import json
import os
from datetime import datetime


class Expense:
    """Represents a single spending transaction."""

    def __init__(self, amount: float, category: str, description: str, date: str = None):
        self.amount = float(amount)
        self.category = category.strip().title()
        self.description = description.strip()
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self) -> dict:
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data.get("date"),
        )


class ExpenseTracker:
    """Manages collection of expenses, file persistence, and summaries."""

    def __init__(self, storage_file: str = "expenses.json"):
        self.storage_file = storage_file
        self.expenses = []
        self.load_data()

    def add_expense(self, amount: float, category: str, description: str):
        if amount <= 0:
            print("[-] Amount must be greater than zero.")
            return

        expense = Expense(amount, category, description)
        self.expenses.append(expense)
        self.save_data()
        print(f"[+] Successfully logged: Rs. {amount:.2f} under '{expense.category}'")

    def calculate_total(self) -> float:
        return sum(exp.amount for exp in self.expenses)

    def view_all(self):
        if not self.expenses:
            print("[-] No expenses recorded yet.")
            return

        print("\n" + "=" * 65)
        print(f"{'ID':<4} | {'Date':<17} | {'Category':<12} | {'Amount (Rs)':<11} | Description")
        print("-" * 65)
        for idx, exp in enumerate(self.expenses, 1):
            print(f"{idx:<4} | {exp.date:<17} | {exp.category:<12} | {exp.amount:<11.2f} | {exp.description}")
        print("=" * 65)
        print(f"Total Expenditure: Rs. {self.calculate_total():.2f}\n")

    def category_summary(self):
        if not self.expenses:
            print("[-] No expense data to summarize.")
            return

        summary = {}
        for exp in self.expenses:
            summary[exp.category] = summary.get(exp.category, 0.0) + exp.amount

        print("\n--- Spending Breakdown by Category ---")
        for category, total in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            print(f"* {category:<15}: Rs. {total:.2f}")
        print("-" * 38)
        print(f"Total Spent    : Rs. {self.calculate_total():.2f}\n")

    def delete_expense(self, index: int):
        if 1 <= index <= len(self.expenses):
            removed = self.expenses.pop(index - 1)
            self.save_data()
            print(f"[+] Removed Rs. {removed.amount:.2f} ('{removed.description}')")
        else:
            print("[-] Invalid index. Please check the list numbers.")

    def save_data(self):
        try:
            with open(self.storage_file, "w") as f:
                json_data = [exp.to_dict() for exp in self.expenses]
                json.dump(json_data, f, indent=4)
        except OSError as e:
            print(f"[-] Error writing to disk: {e}")

    def load_data(self):
        if not os.path.exists(self.storage_file):
            return

        try:
            with open(self.storage_file, "r") as f:
                data = json.load(f)
                self.expenses = [Expense.from_dict(item) for item in data]
        except (json.JSONDecodeError, OSError):
            print("[!] Warning: Could not decode existing records. Starting fresh.")
            self.expenses = []


def get_float_input(prompt: str) -> float:
 while True:
        raw_val = input(prompt).strip()
        try:
            val = float(raw_val)
            if val <= 0:
                print("[-] Enter a positive amount.")
                continue
            return val
        except ValueError:
            print("[-] Invalid input. Please enter a valid numerical amount.")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\n==============================")
        print("   PERSONAL EXPENSE TRACKER   ")
        print("==============================")
        print("1. Add New Expense")
        print("2. View All Transactions")
        print("3. View Category Summary")
        print("4. Delete an Entry")
        print("5. Exit")
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            amount = get_float_input("Enter amount (Rs): ")
            category = input("Enter category (e.g., Food, Travel, Books): ").strip()
            desc = input("Short note/description: ").strip()
            tracker.add_expense(amount, category, desc)

        elif choice == "2":
            tracker.view_all()

        elif choice == "3":
            tracker.category_summary()

        elif choice == "4":
            tracker.view_all()
            if tracker.expenses:
                try:
                    target_id = int(input("Enter transaction ID to remove: ").strip())
                    tracker.delete_expense(target_id)
                except ValueError:
                    print("[-] Please enter a valid numeric ID.")

        elif choice == "5":
            print("\nAll data safely saved to expenses.json. Goodbye!")
            break

        else:
            print("[-] Invalid choice. Enter a number between 1 and 5.")


if __name__ == "__main__":
    main()