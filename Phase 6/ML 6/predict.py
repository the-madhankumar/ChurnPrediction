import joblib
import pandas as pd

# 263. LOAD BEST MODEL AT MODULE LEVEL
model = joblib.load("../../models/logistic_churn.pkl")


FEATURE_COLUMNS = list(model.feature_names_in_)

# 264. PREPROCESS INPUT
def preprocess_input(
    tenure,
    monthly_charges,
    contract_type,
    service_count
):

    data = {
        "tenure": float(tenure),
        "monthly_charges": float(monthly_charges),

        "total_charges": float(monthly_charges) * float(tenure),

        "service_count": int(service_count),

        "high_charge_flag": 0,

        "is_long_term_customer": (
            1 if float(tenure) >= 24 else 0
        ),

        "auto_pay_flag": 0,

        "has_streaming_bundle": 0,

        "contract_Month-to-month": 0,
        "contract_One year": 0,
        "contract_Two year": 0,

        "internet_service_DSL": 0,
        "internet_service_Fiber optic": 1,
        "internet_service_No": 0
    }

    if contract_type == "Month-to-month":

        data["contract_Month-to-month"] = 1

    elif contract_type == "One year":

        data["contract_One year"] = 1

    elif contract_type == "Two year":

        data["contract_Two year"] = 1

    else:

        raise ValueError(
            "contract_type must be "
            "'Month-to-month', 'One year', or 'Two year'"
        )

    df = pd.DataFrame([data])

    df = df.reindex(
        columns=FEATURE_COLUMNS,
        fill_value=0
    )


    return df

# 265–266. PREDICT CHURN
def predict_churn(
    tenure,
    monthly_charges,
    contract_type,
    service_count
):
    """
    Return churn probability, prediction and confidence.
    """

    input_df = preprocess_input(
        tenure,
        monthly_charges,
        contract_type,
        service_count
    )

    prediction = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]

    churn_index = list(model.classes_).index(1)

    risk_score = float(
        probabilities[churn_index]
    )

    if prediction == 1:
        prediction_text = "Likely to churn"
    else:
        prediction_text = "Unlikely to churn"

    confidence = float(
        max(probabilities)
    )

    return {
        "risk_score": risk_score,
        "prediction": prediction_text,
        "confidence": confidence
    }