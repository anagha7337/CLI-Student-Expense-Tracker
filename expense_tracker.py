from datetime import datetime

class ExpenseTracker:

    def __init__(self):
        self.expenses = [
            {
                "date" : datetime.strptime("01/05/2026", "%d/%m/%Y"),
                "amount" : 120.0,
                "category" : "Food"
            },
            {
                "date" : datetime.strptime("08/05/2026", "%d/%m/%Y"),
                "amount" : 50.0,
                "category" : "Travel"
            },
            {
                "date" : datetime.strptime("13/05/2026", "%d/%m/%Y"),
                "amount" : 199.0,
                "category" : "Recharge"
            },
            {
                "date" : datetime.strptime("22/05/2026", "%d/%m/%Y"),
                "amount" : 750.0,
                "category" : "Clothes"
            }
        ]
        self.mbudget = None

    
    def input_values(self):
        while(True):
            date_input = input("Enter date (DD/MM/YYYY) : ")
            try:
                stored_date = datetime.strptime(date_input, "%d/%m/%Y")
                break
            except ValueError:
                print("Invalid format! Please try again using DD/MM/YYYY.")

        while True:
            try:
                amount = float(input("Enter amount : ₹"))
                if amount<=0:
                    print("Amount must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Invalid amount.\n")

        category = input("Enter category : ").title()
        return stored_date, amount, category



    def add_expense(self):
        stored_date, amount, category = self.input_values()
        expense = {
            "date" : stored_date,
            "amount" : amount,
            "category" : category
        }

        self.expenses.append(expense)

        print("Expense added successfully.")

        if self.mbudget is not None:
            current_month = datetime.now().month
            current_year = datetime.now().year
            monthly_spent = self.total_spent_month(current_month, current_year)
            if(monthly_spent>self.mbudget):
                print("\nTotal money spent this month has exceeded the monthly budget!")

    

    def delete_expense(self):
        if not self.expenses:
            print("No expenses available.")
            return
        
        while True:
            try:
                i = int(input("Enter entry no. of expense to be deleted : "))

                if 1<=i<=len(self.expenses):
                    del self.expenses[i-1]
                    print("Expense deleted successfully.\n")
                    break
                else:
                    print("Entry no. does not exist.")

            except ValueError:
                print("Invalid entry no.\n")

    

    def edit_expense(self):
        if not self.expenses:
            print("No expenses available.")
            return
        
        while True:
            try:
                i = int(input("Enter entry no. of expense to be edited : "))

                if 1<=i<=len(self.expenses):
                    stored_date, amount, category = self.input_values()

                    expense = {
                        "date" : stored_date,
                        "amount" : amount,
                        "category" : category
                    }

                    self.expenses[i-1] = expense

                    print("Expense edited successfully.\n")
                    break
                else:
                    print("Entry no. does not exist.")
            except ValueError:
                print("Invalid entry no.\n")
        
        
        
    def total_spent_month(self, month, year):
        total_amt = 0
        for expense in self.expenses:
            if (expense["date"].year==year) and (expense["date"].month==month):
                total_amt += expense["amount"]
        return total_amt



    def view_expenses(self):
        print(f"{'No.':<6}{'Date':<15}{'Amount':<15}{'Category'}")
        print("-" * 50)

        for i, expense in enumerate(self.expenses, start=1):
            print(
                f"{i:<6}"
                f"{expense['date'].strftime('%d/%m/%Y'):<15}"
                f"₹{expense['amount']:<14.2f}"
                f"{expense['category']}"
            )



    def total_spent(self):
        total_amt = 0
        for expense in self.expenses:
            total_amt += expense["amount"]
        print("Total amount spent : ₹", total_amt)



    def highest_category(self):
        if not self.expenses:
            print("No expenses available.")
            return
        
        category_spendings = {}

        for expense in self.expenses:
            category_spendings[expense["category"]] = category_spendings.get(expense["category"], 0) + expense["amount"]

        total_spent = sum(category_spendings.values())

        print("\nCATEGORY-WISE SPENDING")
        print("-" * 50)

        for category, amount in category_spendings.items():
            percentage = (amount / total_spent) * 100

            print(
                f"{category:<15}"
                f"₹{amount:<10.2f}"
                f"{percentage:.2f}%"
            )

        highest_spendings = []
        highest = 0

        for category, spending in category_spendings.items():
            if spending>highest:
                highest = spending
                highest_spendings.clear()
                highest_spendings.append(category)
            elif spending==highest:
                highest_spendings.append(category)
        
        if len(highest_spendings)==1:
            print("\nHIGHEST SPENDING CATEGORY : ", highest_spendings[0])
            print("Total money spent on ", highest_spendings[0], " : ₹", category_spendings[highest_spendings[0]])
        else:
            print("HIGHEST SPENDING CATEGORIES : ")
            for category in highest_spendings:
                print(category)
            print("\nTotal money spent on each category :")
            for category in highest_spendings:
                print(category, " : ₹", category_spendings[category])



    def search_by_category(self):
        category = input("Enter category : ").title()

        matches = [
            expense
            for expense in self.expenses
            if expense['category'] == category
        ]

        if not matches:
            print("No expenses found for this category.")
            return
        
        print(f"{'No.':<6}{'Date':<15}{'Amount':<15}{'Category'}")
        print("-" * 50)

        for i, expense in enumerate(self.expenses, start=1):
            if expense['category']==category:
                print(
                    f"{i:<6}"
                    f"{expense['date'].strftime('%d/%m/%Y'):<15}"
                    f"₹{expense['amount']:<14.2f}"
                    f"{expense['category']}"
                )


    def set_monthly_budget(self):
        while True:
            try:
                self.mbudget = float(input("Enter monthly budget for the ongoing month : ₹"))
                if self.mbudget < 0 :
                    print("Monthly budget must be greater than or equal to 0.")
                    continue
                print("Monthly budget set successfully.")
                break
            except ValueError:
                print("Invalid amount.\n")


    
    def monthly_report(self):
        if not self.expenses:
            print("No expenses available.")
            return

        monthly_data = {}

        for expense in self.expenses:
            key = (expense["date"].year, expense["date"].month)

            if key not in monthly_data:
                monthly_data[key] = []

            monthly_data[key].append(expense)

        highest_month = None
        highest_amount = 0

        print("\nMONTHLY REPORT")
        print("=" * 50)

        for key, expenses in sorted(monthly_data.items()):

            year, month = key

            print(f"\n{datetime(year, month, 1).strftime('%B %Y')}")
            print("-" * 30)

            total = 0

            for expense in expenses:
                print(
                    expense['date'].strftime("%d/%m/%Y"),
                    f"₹{expense['amount']}",
                    expense['category']
                )

                total += expense["amount"]

            average = total / len(expenses)

            print(f"\nTotal Spending : ₹{total}")
            print(f"Average Expense: ₹{average:.2f}")

            if total > highest_amount:
                highest_amount = total
                highest_month = key

        print("\n" + "=" * 50)

        year, month = highest_month

        print(
            f"\nHighest Spending Month : "
            f"{datetime(year, month, 1).strftime('%B %Y')}"
        )

        print(f"Amount Spent : ₹{highest_amount}")



    def dashboard(self):
        if not self.expenses:
            print("No expenses available.")
            return

        total_expenses = len(self.expenses)

        total_spent = sum(
            expense["amount"]
            for expense in self.expenses
        )

        avg_expense = total_spent / total_expenses

        highest_expense = max(
            self.expenses,
            key=lambda expense: expense["amount"]
        )

        category_spendings = {}

        for expense in self.expenses:
            category_spendings[expense["category"]] = (
                category_spendings.get(expense["category"], 0)
                + expense["amount"]
            )

        highest_category_amount = max(
            category_spendings.values()
        )

        highest_categories = [
            category
            for category, amount in category_spendings.items()
            if amount == highest_category_amount
        ]

        print("\nDASHBOARD")
        print("-" * 40)

        print("Total Expenses :", total_expenses)
        print("Total Amount Spent : ₹", total_spent)
        print("Average Expense : ₹", round(avg_expense, 2))

        print(
            "\nHighest Single Expense : ₹",
            highest_expense["amount"]
        )
        print(
            "Category :",
            highest_expense["category"]
        )
        print(
            "Date :",
            highest_expense["date"].strftime("%d/%m/%Y")
        )

        print("\nHighest Spending Category/Categories:")

        for category in highest_categories:
            print(
                f"{category} : ₹{highest_category_amount}"
            )

        if self.mbudget is not None:
            current_month = datetime.now().month
            current_year = datetime.now().year

            monthly_spent = self.total_spent_month(
                current_month,
                current_year
            )

            remaining = self.mbudget - monthly_spent

            print("\nMonthly Budget : ₹", self.mbudget)

            if remaining < 0:
                print(
                    "Monthly budget is already spent."
                )
                print(
                    f"Exceeded by ₹{-remaining:.2f}"
                )
            else:
                print(
                    f"Remaining Budget : ₹{remaining:.2f}"
                )



tracker = ExpenseTracker()

while True:
    print("\n\n\n-----------EXPENSE TRACKER INTERFACE-----------\n")
    print("1  -  Add an expense")
    print("2  -  Delete an expense")
    print("3  -  Edit an expense")
    print("4  -  View expenses")
    print("5  -  See total amount spent")
    print("6  -  See which category has the highest spending")
    print("7  -  Search expenses by category")
    print("8  -  Set monthly budget")
    print("9  -  View monthly spending report")
    print("10 -  View complete Dashboard")
    print("11 -  Exit")
    
    while True:
        try:
            option = int(input("\n\nChoose an option : "))
            break
        except ValueError:
            print("Invalid input.")
            
    print("\n\n")

    match option:
        case 1:
            tracker.add_expense()
        case 2:
            tracker.delete_expense()
        case 3:
            tracker.edit_expense()
        case 4:
            tracker.view_expenses()
        case 5:
            tracker.total_spent()
        case 6:
            tracker.highest_category()
        case 7:
            tracker.search_by_category()
        case 8:
            tracker.set_monthly_budget()
        case 9:
            tracker.monthly_report()
        case 10:
            tracker.dashboard()
        case 11:
            print("Exiting the program...\n\n")
            break
        case _:
<<<<<<< HEAD
            print("Invalid option. Please try again")
=======
            print("Invalid option. Please try again")
>>>>>>> 8d35a591b4bccd48c746d1baf9dbd23c10d63fef
