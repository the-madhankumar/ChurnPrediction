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

    cleaned_df.to_sql(
        "cleaned_customers",
        con = engine,
        if_exists = "replace",
        index = False
    )

    return cleaned_df

def build_curated_tables(cleaned_df, engine):
    dim_contract_data = (
        cleaned_df[["contract"]]
        .dropna()
        .drop_duplicates()
        .rename(columns={"contract": "contract_type"})
    )

    dim_contract_data.to_sql(
        "dim_contract",
        con=engine,
        if_exists="append",
        index=False
    )

    dim_payment_data = (
        cleaned_df[["payment_method"]]
        .dropna()
        .drop_duplicates()
    )

    dim_payment_data.to_sql(
        "dim_payment",
        con=engine,
        if_exists="append",
        index=False
    )

    contract_lookup = pd.read_sql(
        "SELECT contract_key, contract_type FROM dim_contract",
        con=engine
    )

    payment_lookup = pd.read_sql(
        "SELECT payment_key, payment_method FROM dim_payment",
        con=engine
    )

    fact_df = cleaned_df.merge(
        contract_lookup,
        left_on="contract",
        right_on="contract_type",
        how="left"
    )

    fact_df = fact_df.merge(
        payment_lookup,
        on="payment_method",
        how="left"
    )

    fact_data = fact_df[
        [
            "customer_id",
            "contract_key",
            "payment_key",
            "tenure",
            "monthly_charges",
            "total_charges",
            "churn"
        ]
    ]

    fact_data.to_sql(
        "fact_customer_account",
        con=engine,
        if_exists="append",
        index=False
    )

    print("dim_contract:", len(dim_contract_data))
    print("dim_payment:", len(dim_payment_data))
    print("customers: ", len(fact_data))
    print("fact_customer_account:", len(fact_data))

def quality_report(cleaned_df):

    assert cleaned_df["customer_id"].isnull().sum() == 0, \
        "FAIL: NULL values found in customer_id"

    print("PASS: No NULL values in customer_id")

    assert cleaned_df["monthly_charges"].isnull().sum() == 0, \
        "FAIL: NULL values found in monthly_charges"

    print("PASS: No NULL values in monthly_charges")

    assert sorted(cleaned_df["churn"].unique()) == [0, 1], \
        "FAIL: churn values are not 0 and 1"

    print("PASS: churn values are 0 and 1")

if __name__ == "__main__":
    cleaned_df = clean_staging("stg_customer_raw", engine=engine)
    build_curated_tables(cleaned_df, engine = engine)
    quality_report(cleaned_df)