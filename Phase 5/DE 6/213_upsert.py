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

            conn.execute(query, {
                "customer_id": row["customer_id"],
                "gender": row["gender"],
                "partner": row["partner"],
                "dependents": row["dependents"],
                "senior_citizen": row["senior_citizen"]
            })

cleaned_df = clean_staging("stg_customer_raw", engine)

upsert_customers(cleaned_df, engine)