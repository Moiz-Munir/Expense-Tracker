from db import get_connection
import services, models

conn = get_connection()
print("✅ Connected to:", conn.server_info)
conn.close()

print(services.add_new_user("Moiz", "moiz@email.com"))

models.create_category("Groceries", "Expense")
models.create_category("Salary", "Income")

print(services.add_new_transaction(1, 1, 25, "Weekly groceries"))
print(models.get_users())
