import pandas as pd
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pandas as pd

user = "root"
password = "root"
host = "localhost"
port = 3306
database = "customer_intelligence_labs"

url = URL.create(
    drivername="mysql+pymysql",
    username=user,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_engine(url=url)

existing_customers = pd.read_sql(
    """
    SELECT
        customer_id,
        gender,
        partner,
        dependents,
        senior_citizen
    FROM customers
    """,
    con=engine
)

existing_ids = set(existing_customers["customer_id"])

df = pd.read_csv(r"D:\Training Project\Project 1\dataset\telco_customer.csv")

for _, row in df.iterrows():
    customer_id = row["customerID"]

    existing = existing_customers[
        existing_customers["customer_id"] == customer_id
    ]

    if customer_id not in existing_ids:
        print(customer_id, "New -> Insert")
    else:
        existing_row = existing.iloc[0]

        partner = True if row["Partner"] == "Yes" else False
        dependents = True if row["Dependents"] == "Yes" else False
        senior_citizen = True if row["SeniorCitizen"] == 1 else False

        if (
            row["gender"] == existing_row["gender"]
            and partner == bool(existing_row["partner"])
            and dependents == bool(existing_row["dependents"])
            and senior_citizen == bool(existing_row["senior_citizen"])
        ):
            print(customer_id, "SKIP")
        else:
            print(customer_id, "UPDATE")