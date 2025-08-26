from db import get_connection

def create_user(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
    if cursor.fetchone():
        conn.close()
        return None  # User already exists
    
    cursor.execute("INSERT INTO Users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    conn.close()
    return True


def get_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users")
    result = cursor.fetchall()
    conn.close()
    return result

def create_category(name, type_):
    conn = get_connection()
    cursor = conn.cursor()

    # Check if category already exists
    cursor.execute("SELECT category_id FROM Categories WHERE category_name = %s", (name,))
    if cursor.fetchone():
        conn.close()
        return None  # Category already exists

    cursor.execute(
        "INSERT INTO Categories (category_name, type) VALUES (%s, %s)",
        (name, type_)
    )
    conn.commit()
    conn.close()
    return True


def create_transaction(user_id, category_id, amount, description=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Transactions (user_id, category_id, amount, description) VALUES (%s, %s, %s, %s)",
        (user_id, category_id, amount, description),
    )
    conn.commit()
    conn.close()