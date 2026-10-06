from pydantic import BaseModel
from decimal import Decimal

class CustomerResponse(BaseModel):
    customer_id: str
    tenure: int
    contract_type: str
    internet_service: str
    monthly_charges: Decimal
    churn: bool

class CustomerFeatures(BaseModel):
    service_count: int
    high_charge_flag: bool
    is_long_term_customer: bool
    auto_pay_flag: bool
    tenure_bucket: str
    has_streaming_bundle: bool

#119 - Churn prediction request
class ChurnPredictionRequest(BaseModel):
    tenure: int
    monthly_charges: float
    contract_type: str
    service_count: int