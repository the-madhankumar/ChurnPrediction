from sqlalchemy import text
import sys

sys.path.append("../../Phase 1/CP2/")

from customer_cleaner import CustomerCleaner
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

def clean_staging(database_name, engine):
    df = pd.read_sql(f"SELECT * FROM {database_name}", con = engine)
    cleaner = CustomerCleaner(data_frame=df)
    cleaned_df = cleaner.clean()

    return cleaned_df

def upsert_customers(cleaned_df, engine):

    existing_df = pd.read_sql(
        """
        SELECT customer_id, gender, partner, dependents, senior_citizen
        FROM customers
        """,
        con=engine
    )

    existing_customers = {
        row["customer_id"]: row
        for _, row in existing_df.iterrows()
    }

    rows_inserted = 0
    rows_updated = 0
    rows_unchanged = 0

    query = text("""
        INSERT INTO customers
        (customer_id, gender, partner, dependents, senior_citizen)
        VALUES
        (:customer_id, :gender, :partner, :dependents, :senior_citizen)

        ON DUPLICATE KEY UPDATE
            gender = VALUES(gender),
            partner = VALUES(partner),
            dependents = VALUES(dependents),
            senior_citizen = VALUES(senior_citizen)
    """)

    with engine.begin() as conn:

        for _, row in cleaned_df.iterrows():

            customer_id = row["customer_id"]

            new_values = {
                "customer_id": customer_id,
                "gender": row["gender"],
                "partner": row["partner"],
                "dependents": row["dependents"],
                "senior_citizen": row["senior_citizen"]
            }

            if customer_id not in existing_customers:

                conn.execute(query, new_values)

                rows_inserted += 1
                print(customer_id, "-> INSERT")

            else:
                existing = existing_customers[customer_id]

                changed = (
                    row["gender"] != existing["gender"]
                    or row["partner"] != existing["partner"]
                    or row["dependents"] != existing["dependents"]
                    or row["senior_citizen"] != existing["senior_citizen"]
                )

                if changed:

                    conn.execute(query, new_values)

                    rows_updated += 1
                    print(customer_id, "-> UPDATE")

                else:

                    rows_unchanged += 1
                    print(customer_id, "-> SKIP")

    print("\nSummary")
    print("Inserted:", rows_inserted)
    print("Updated:", rows_updated)
    print("Unchanged:", rows_unchanged)

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO pipeline_run_log
                (file_name, rows_inserted, rows_updated, rows_unchanged)
                VALUES
                (:file_name, :rows_inserted, :rows_updated, :rows_unchanged)
            """),
            {
                "file_name": "telco_customer.csv",
                "rows_inserted": rows_inserted,
                "rows_updated": rows_updated,
                "rows_unchanged": rows_unchanged
            }
        )

cleaned_df = clean_staging("stg_customer_raw", engine)

upsert_customers(cleaned_df, engine)