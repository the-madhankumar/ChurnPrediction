import json

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

# 219. QUALITY CHECK FUNCTIONS
def check_null_rate(df, col, threshold):
    null_rate = df[col].isnull().mean() * 100

    return {
        "check_name": f"null_rate_{col}",
        "status": "PASS" if null_rate <= threshold else "FAIL",
        "value_found": round(null_rate, 2),
        "threshold": threshold
    }


def check_value_range(df, col, min_value=None, max_value=None):
    min_found = df[col].min()
    max_found = df[col].max()

    passed = True

    if min_value is not None and min_found < min_value:
        passed = False

    if max_value is not None and max_found > max_value:
        passed = False

    return {
        "check_name": f"value_range_{col}",
        "status": "PASS" if passed else "FAIL",
        "value_found": {
            "min": min_found,
            "max": max_found
        },
        "threshold": {
            "min": min_value,
            "max": max_value
        }
    }


def check_allowed_values(df, col, allowed_set):
    found_values = set(df[col].dropna().unique())

    invalid_values = found_values - set(allowed_set)

    return {
        "check_name": f"allowed_values_{col}",
        "status": "PASS" if len(invalid_values) == 0 else "FAIL",
        "value_found": list(found_values),
        "threshold": list(allowed_set)
    }


def check_row_count(df, expected_min):
    row_count = len(df)

    return {
        "check_name": "row_count",
        "status": "PASS" if row_count >= expected_min else "FAIL",
        "value_found": row_count,
        "threshold": expected_min
    }


def check_no_duplicates(df, key_col):
    duplicate_count = df[key_col].duplicated().sum()

    return {
        "check_name": f"no_duplicates_{key_col}",
        "status": "PASS" if duplicate_count == 0 else "FAIL",
        "value_found": duplicate_count,
        "threshold": 0
    }


def check_churn_distribution(df):
    # Adjust the column name if your dataset uses a different name
    churn_rate = (
        df["churn"]
        .value_counts(normalize=True)
        .get("Yes", 0) * 100
    )

    return {
        "check_name": "churn_distribution",
        "status": "PASS",
        "value_found": round(churn_rate, 2),
        "threshold": "Informational"
    }


def run_quality_checks(df):

    results = []

    # 220. Null rate checks
    results.append(
        check_null_rate(df, "monthly_charges", 0)
    )

    results.append(
        check_null_rate(df, "tenure", 0)
    )

    # 221. Value range checks
    results.append(
        check_value_range(df, "tenure", 0, 100)
    )

    results.append(
        check_value_range(df, "monthly_charges", 0, None)
    )

    # 222. Allowed values check
    results.append(
        check_allowed_values(
            df,
            "contract",
            {
                "Month-to-month",
                "One year",
                "Two year"
            }
        )
    )

    # 223. Row count check
    results.append(
        check_row_count(df, 7000)
    )

    # 224. Duplicate check
    results.append(
        check_no_duplicates(df, "customer_id")
    )

    # 219. Churn distribution check
    results.append(
        check_churn_distribution(df)
    )

    return results

def save_quality_report(results, file_name="quality_report.json"):

    with open(file_name, "w") as file:
        json.dump(results, file, indent=4, default=str)


def validate_quality(results):

    critical_failures = []

    for result in results:

        if result["status"] == "FAIL":
            critical_failures.append(result["check_name"])

    if critical_failures:

        raise Exception(
            "CRITICAL DATA QUALITY CHECK FAILED: "
            + ", ".join(critical_failures)
        )

# 219 - 227. RUN DATA QUALITY CHECKS
cleaned_df = clean_staging("stg_customer_raw", engine)

# Run all quality checks
quality_results = run_quality_checks(cleaned_df)

# 225. Create quality_report.json
save_quality_report(quality_results)

# Print results
for result in quality_results:
    print(
        result["check_name"],
        "->",
        result["status"],
        "| Value:",
        result["value_found"],
        "| Threshold:",
        result["threshold"]
    )

# 226. Stop pipeline if critical check fails
validate_quality(quality_results)

print("\nAll critical quality checks passed.")