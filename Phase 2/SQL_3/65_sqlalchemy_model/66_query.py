from database import get_db
from schema import Customer


db = get_db()

try:
    customer = db.get(Customer, "7590-VHVEG")

    if customer:
        print("Customer Details")
        print("-" * 30)
        print(f"Customer ID     : {customer.customer_id}")
        print(f"Gender          : {customer.gender}")
        print(f"Senior Citizen  : {customer.senior_citizen}")
    else:
        print("Customer not found.")

finally:
    db.close()

# (venv) PS D:\Training Project\Project 1\Phase 2\SQL_3\65_sqlalchemy_model> python .\66_query.py
# Customer Details
# ------------------------------
# Customer ID     : 7590-VHVEG
# Gender          : Female
# Senior Citizen  : 0