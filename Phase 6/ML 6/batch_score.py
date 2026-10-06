import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

from predict import predict_churn


# ============================================================
# 271–272. CONNECT TO DATABASE AND LOAD ALL CUSTOMERS
# ============================================================

engine = create_engine(
    "mysql+pymysql://root:root@localhost/customer_intelligence_labs"
)

df = pd.read_sql(
    "SELECT * FROM customer_ml_features_de",
    engine
)

print("Customers loaded:", len(df))


# ============================================================
# 273–274. APPLY MODEL TO EVERY CUSTOMER
# ============================================================

def score_customer(row):

    return predict_churn(
        tenure=row["tenure"],
        monthly_charges=row["monthly_charges"],
        contract_type=row["contract"],
        service_count=row["service_count"]
    )


results = df.apply(
    score_customer,
    axis=1,
    result_type="expand"
)


# Give the returned values proper column names
results.columns = [
    "risk_score",
    "prediction",
    "confidence"
]


# Add results to customer IDs
risk_table = pd.concat(
    [
        df[["customer_id"]],
        results
    ],
    axis=1
)


# ============================================================
# 275. ADD SCORING DATE
# ============================================================

risk_table["scoring_date"] = datetime.today().strftime(
    "%Y-%m-%d"
)


# ============================================================
# 276. SAVE TO SQL TABLE
# ============================================================

risk_table.to_sql(
    "customer_risk_table",
    engine,
    if_exists="replace",
    index=False
)

print("\nSaved to customer_risk_table")


# ============================================================
# 277. SUMMARY
# ============================================================

print("\nCHURN RISK SUMMARY")
print("=" * 50)

summary = risk_table["prediction"].value_counts()

print(summary)

likely = (risk_table["prediction"] == "Likely to churn").sum()
unlikely = (risk_table["prediction"] == "Unlikely to churn").sum()

total = len(risk_table)

churn_percentage = likely / total * 100

print(f"\nLikely to churn:   {likely}")
print(f"Unlikely to churn: {unlikely}")
print(f"Total customers:   {total}")
print(f"Predicted churn:   {churn_percentage:.2f}%")


# ============================================================
# 278. TOP 10 HIGHEST-RISK CUSTOMERS
# ============================================================

top10 = risk_table.sort_values(
    "risk_score",
    ascending=False
).head(10)

print("\nTOP 10 HIGHEST-RISK CUSTOMERS")
print("=" * 60)

print(
    top10[
        [
            "customer_id",
            "risk_score",
            "prediction",
            "confidence"
        ]
    ].to_string(index=False)
)