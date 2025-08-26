import argparse
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import services


# Add project root to sys.path so Python can find 'app'
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

    # Transaction commands
    parser.add_argument("--add-transaction", nargs=4, metavar=("USER_ID", "CATEGORY_ID", "AMOUNT", "DESCRIPTION"), help="Add a transaction")
    parser.add_argument("--list-transactions", metavar="USER_ID", help="List all transactions for a user")

    # Summary
    parser.add_argument("--summary", metavar="USER_ID", help="Get income, expenses, balance for a user")

    # Filtered Transactions
    parser.add_argument("--start-date", metavar="YYYY-MM-DD", help="Filter transactions start date")
    parser.add_argument("--end-date", metavar="YYYY-MM-DD", help="Filter transactions end date")
    parser.add_argument("--category-id", metavar="CATEGORY_ID", help="Filter transactions by category")


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

    # Transactions
    if args.add_transaction:
        user_id, category_id, amount, description = args.add_transaction
        print(services.add_new_transaction(int(user_id), int(category_id), float(amount), description))

    if args.list_transactions:
        user_id = int(args.list_transactions)
        transactions = services.list_user_transactions(user_id)
        for t in transactions:
            print(f"{t['transaction_date']}: {t['category_name']} ({t['type']}) - {t['amount']} | {t['description']}")

    # Summary
    if args.summary:
        user_id = int(args.summary)
        summary = services.get_user_summary(user_id)
        print(f"Income: {summary['income']}, Expenses: {summary['expenses']}, Balance: {summary['balance']}")

    if args.list_transactions:
        user_id = int(args.list_transactions)
        transactions = services.list_user_transactions_filtered(
            user_id,
            start_date=args.start_date,
            end_date=args.end_date,
            category_id=int(args.category_id) if args.category_id else None
        )
        for t in transactions:
            print(f"{t['transaction_date']}: {t['category_name']} ({t['type']}) - {t['amount']} | {t['description']}")

if __name__ == "__main__":
    main()
