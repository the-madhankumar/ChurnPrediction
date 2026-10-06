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

def build_features(cleaned_df, engine):
    try:
        # df = pd.read_sql(
        #     "SELECT * FROM cleaned_customers",
        #     con=engine
        # )

        df = cleaned_df

        # Feature 1 - tenure_bucket

        bins = [0, 12, 24, 48, 72]
        labels = ["0-12", "13-24", "25-48", "49-72"]
        df["tenure_bucket"] = pd.cut(
            df["tenure"],
            bins=bins,
            labels=labels,
            include_lowest=True
        )

        # Feature 2 - high_change_flag

        median = df["monthly_charges"].median()
        def fill_high_charge(charge):
            return 1 if charge > median else 0

        df["high_charge_flag"] = df["monthly_charges"].apply(fill_high_charge)

        # Feature 3 - serivce_count

        def fill_service_count(row):
            service_columns = [
                "online_security",
                "online_backup",
                "device_protection",
                "tech_support",
                "streaming_tv",
                "streaming_movies"
            ]
            count = 0
            for cols in service_columns:
                count += 1 if row[cols] == "Yes" else 0
            return count

        df["service_count"] = df.apply(fill_service_count, axis=1)

        # Feature 4 - is_long_term_customer

        def fill_is_long_term_customer(tenure):
            return 1 if tenure >= 24 else 0

        df["is_long_term_customer"] = df["tenure"].apply(fill_is_long_term_customer)

        # Feature 5 - has_streaming_bundle

        def fill_has_streaming_bundle(row):
            return 1 if row["streaming_tv"] == "Yes" and row["streaming_movies"] == "Yes" else 0

        df["has_streaming_bundle"] = df[["streaming_tv", "streaming_movies"]].apply(fill_has_streaming_bundle, axis = 1)

        # Feature 6 - auto_pay_flag

        def fill_auto_pay_flag(value):
            return 1 if "automatic" in value else 0

        df["auto_pay_flag"] = df["payment_method"].apply(fill_auto_pay_flag)

        df = df[
                [
                    'customer_id',
                    'tenure',
                    'monthly_charges',
                    'contract',
                    'internet_service',
                    'total_charges',
                    'auto_pay_flag',
                    'has_streaming_bundle',
                    'is_long_term_customer',
                    'service_count',
                    'high_charge_flag',
                    'tenure_bucket',
                    'churn'
                ]
            ]
        return df
    
    except Exception as e:
        print("Error Occured:", e)

def validation(customer_ml_features, cleaned_df):

    if customer_ml_features.shape[0] == cleaned_df.shape[0]:
        print("PASS: Customer ML Features and Cleaned df row counts match")
    else:
        print("FAIL: Customer ML Features and Cleaned df row counts do not match")

    feature_columns = [
        "auto_pay_flag",
        "has_streaming_bundle",
        "is_long_term_customer",
        "service_count",
        "high_charge_flag",
        "tenure_bucket",'tenure', 'monthly_charges', 'total_charges'
    ]

    missing_columns = []

    for col in feature_columns:
        if col not in customer_ml_features.columns:
            missing_columns.append(col)

    if len(missing_columns) == 0:
        print("PASS: All 6 feature columns are present")
    else:
        print("FAIL: Missing columns:", missing_columns)

    for col in feature_columns:
        null_count = customer_ml_features[col].isnull().sum()

        if null_count == 0:
            print(f"PASS: {col} has no NULL values")
        else:
            print(f"FAIL: {col} has {null_count} NULL values")

if __name__ == "__main__":

    cleaned_df = clean_staging(
        "stg_customer_raw",
        engine=engine
    )

    print(cleaned_df.columns)

    customer_ml_features = build_features(
        cleaned_df,
        engine=engine
    )

    validation(
        customer_ml_features,
        cleaned_df
    )

    customer_ml_features.to_sql(
        "customer_ml_features_DE",
        con = engine,
        if_exists = "replace",
        index = False
    )