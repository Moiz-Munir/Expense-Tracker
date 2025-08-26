from .db import get_connection

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

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

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

def get_all_categories():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Categories")
    categories = cursor.fetchall()
    conn.close()
    return categories


def create_transaction(user_id, category_id, amount, description=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Transactions (user_id, category_id, amount, description) VALUES (%s, %s, %s, %s)",
        (user_id, category_id, amount, description),
    )
    conn.commit()
    conn.close()

def get_transactions_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.transaction_id, c.category_name, c.type, t.amount, t.transaction_date, t.description
        FROM Transactions t
        JOIN Categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s
        ORDER BY t.transaction_date DESC
    """, (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_transactions_by_user_filtered(user_id, start_date=None, end_date=None, category_id=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT t.transaction_id, c.category_name, c.type, t.amount, t.transaction_date, t.description
        FROM Transactions t
        JOIN Categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s
    """
    params = [user_id]

    if start_date:
        query += " AND t.transaction_date >= %s"
        params.append(start_date)
    if end_date:
        query += " AND t.transaction_date <= %s"
        params.append(end_date)
    if category_id:
        query += " AND t.category_id = %s"
        params.append(category_id)

    query += " ORDER BY t.transaction_date DESC"
    cursor.execute(query, tuple(params))
    transactions = cursor.fetchall()
    conn.close()
    return transactions


def get_total_by_type(user_id, type_):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(t.amount) 
        FROM Transactions t
        JOIN Categories c ON t.category_id = c.category_id
        WHERE t.user_id = %s AND c.type = %s
    """, (user_id, type_))
    total = cursor.fetchone()[0]
    conn.close()
    return total if total else 0

def user_exists(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE user_id=%s", (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def category_exists(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Categories WHERE category_id=%s", (category_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
