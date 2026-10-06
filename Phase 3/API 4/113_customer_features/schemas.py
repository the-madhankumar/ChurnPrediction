from pydantic import BaseModel
from decimal import Decimal

class CustomerResponse(BaseModel):
    customer_id: str
    tenure: int
    contract_type: str
    internet_service: str
    monthly_charges: Decimal
    churn: bool

#115 - Return all engineered features: service_count, tenure_bucket, high_charge_flag, is_long_term_customer, has_streaming_bundle, auto_pay_flag, monthly_charges, total_charges  BY Response Model
#117 - Define a Pydantic CustomerFeatures response model 
class CustomerFeatures(BaseModel):
    service_count: int
    high_charge_flag: bool
    is_long_term_customer: bool
    auto_pay_flag: bool
    tenure_bucket: str
    has_streaming_bundle: bool