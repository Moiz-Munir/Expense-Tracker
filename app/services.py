import models

def add_new_user(name, email):
    result = models.create_user(name, email)
    if result:
        return f"User {name} created!"
    else:
        return f"User with email {email} already exists."


def add_new_transaction(user_id, category_id, amount, description=None):
    models.create_transaction(user_id, category_id, amount, description)
    return f"Transaction of {amount} added!"
