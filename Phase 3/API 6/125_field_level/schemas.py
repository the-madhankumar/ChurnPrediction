from pydantic import BaseModel, Field
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

class ChurnPredictionRequest(BaseModel):
    #125 - field validator for tenure
    tenure: int = Field(ge=0, le=100)
    monthly_charges: float
    contract_type: str
    service_count: int

#126 - Error Response
class ErrorResponse(BaseModel):
    detail: str
    status_code: int