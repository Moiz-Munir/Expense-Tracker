import argparse
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import services


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")

    # User commands
    parser.add_argument("--add-user", nargs=2, metavar=("NAME", "EMAIL"), help="Add a new user")
    parser.add_argument("--find-user", metavar="EMAIL", help="Find a user by email")

    # Category commands
    parser.add_argument("--list-categories", action="store_true", help="List all categories")
    parser.add_argument("--add-category", nargs=2, metavar=("NAME", "TYPE"), help="Add a new category")

    # Expense commands
    parser.add_argument("--add-expense", nargs=4, metavar=("USER_ID", "CATEGORY_ID", "AMOUNT", "DESCRIPTION"), help="Add an expense")
    parser.add_argument("--list-expenses", metavar="USER_ID", help="List all expenses for a user")

    # New expense commands
    parser.add_argument("--delete-expense", metavar="EXPENSE_ID", help="Delete an expense by ID")
    parser.add_argument("--update-expense", nargs=4, metavar=("EXPENSE_ID", "CATEGORY_ID", "AMOUNT", "DESCRIPTION"), help="Update an expense")
    parser.add_argument("--export-expenses", nargs=2, metavar=("USER_ID", "FILENAME"), help="Export expenses to CSV")
    parser.add_argument("--category-summary", metavar="USER_ID", help="Summary of expenses by category")

    # Summary
    parser.add_argument("--summary", metavar="USER_ID", help="Get income, expenses, balance for a user")

    # Filters
    parser.add_argument("--start-date", metavar="YYYY-MM-DD", help="Filter expenses start date")
    parser.add_argument("--end-date", metavar="YYYY-MM-DD", help="Filter expenses end date")
    parser.add_argument("--category-id", metavar="CATEGORY_ID", help="Filter expenses by category")

    args = parser.parse_args()

    # Users
    if args.add_user:
        name, email = args.add_user
        print(services.add_new_user(name, email))

    if args.find_user:
        print(services.find_user(args.find_user))

    # Categories
    if args.list_categories:
        categories = services.list_categories()
        for c in categories:
            print(f"{c['category_id']}: {c['category_name']} ({c['type']})")

    if args.add_category:
        name, type_ = args.add_category
        services.add_new_category(name, type_)

    # Expenses
    if args.add_expense:
        user_id, category_id, amount, description = args.add_expense
        print(services.add_new_expense(int(user_id), int(category_id), float(amount), description))

    if args.list_expenses:
        user_id = int(args.list_expenses)
        expenses = services.list_user_expenses_filtered(
            user_id,
            start_date=args.start_date,
            end_date=args.end_date,
            category_id=int(args.category_id) if args.category_id else None
        )
        for t in expenses:
            print(f"{t['expense_id']} | {t['expense_date']}: {t['category_name']} ({t['type']}) - {t['amount']} | {t['description']}")

    if args.delete_expense:
        print(services.delete_expense(int(args.delete_expense)))

    if args.update_expense:
        expense_id, category_id, amount, description = args.update_expense
        print(services.update_expense(int(expense_id), int(category_id), float(amount), description))

    if args.export_expenses:
        user_id, filename = args.export_expenses
        print(services.export_expenses_to_csv(int(user_id), filename))

    if args.category_summary:
        summary = services.get_category_summary(int(args.category_summary))
        for cat, total in summary.items():
            print(f"{cat}: {total}")

    # Summary
    if args.summary:
        user_id = int(args.summary)
        summary = services.get_user_summary(user_id)
        print(f"Income: {summary['income']}, Expenses: {summary['expenses']}, Balance: {summary['balance']}")


if __name__ == "__main__":
    main()
