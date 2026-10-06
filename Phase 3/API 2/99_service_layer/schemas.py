from pydantic import BaseModel
from decimal import Decimal

class CustomerResponse(BaseModel):
    customer_id: str
    tenure: int
    contract_type: str
    internet_service: str
    monthly_charges: Decimal
    churn: bool
