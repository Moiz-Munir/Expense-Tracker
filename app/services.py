from . import models

def add_new_user(name, email):
    result = models.create_user(name, email)
    if result:
        return f"User {name} created!"
    else:
        return f"User with email {email} already exists."

def add_new_transaction(user_id, category_id, amount, description=None):
    models.create_transaction(user_id, category_id, amount, description)
    return f"Transaction of {amount} added!"

def find_user(email):
    user = models.get_user_by_email(email)
    if user:
        return f"User found: {user['name']} (ID: {user['user_id']})"
    else:
        return f"No user with email {email}."
    
def list_categories():
    categories = models.get_all_categories()
    return categories  # Can format or print nicely in CLI later

def add_new_category(name, type_):
    result = models.create_category(name, type_)
    if result:
        print(f"Category '{name}' added!")
    else:
        print(f"Category '{name}' already exists.")


def list_user_transactions(user_id):
    transactions = models.get_transactions_by_user(user_id)
    if not transactions:
        return "No transactions found."
    return transactions

def list_user_transactions_filtered(user_id, start_date=None, end_date=None, category_id=None):
    transactions = models.get_transactions_by_user_filtered(user_id, start_date, end_date, category_id)
    if not transactions:
        return "No transactions found."
    return transactions

def get_user_summary(user_id):
    income = models.get_total_by_type(user_id, 'income')
    expenses = models.get_total_by_type(user_id, 'expense')
    balance = income - expenses
    return {
        "income": income,
        "expenses": expenses,
        "balance": balance
    }

def add_new_transaction(user_id, category_id, amount, description):
    # Validate user
    if not models.user_exists(user_id):
        return f"Error: User ID {user_id} does not exist."
    
    # Validate category
    if not models.category_exists(category_id):
        return f"Error: Category ID {category_id} does not exist."
    
    # Validate amount
    if amount <= 0:
        return "Error: Transaction amount must be positive."
    
    # Everything is valid, create transaction
    return models.create_transaction(user_id, category_id, amount, description)
