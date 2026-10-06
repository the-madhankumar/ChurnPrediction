from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Customers, FactCustomerAccount, DimContract, Services
from schemas import CustomerResponse


router = APIRouter()

@router.get("/churn/summary")
def get_churn_summary():
    pass

@router.get("/customer/{customer_id}",  response_model=CustomerResponse)
def get_customer_by_id(
    customer_id: str,
    db: AsyncSession = Depends(get_db)
):
    query = (
        select(
            Customers.customer_id,
            FactCustomerAccount.tenure,
            DimContract.contract_type,
            Services.internet_service,
            FactCustomerAccount.monthly_charges,
            FactCustomerAccount.churn,
        )
        .join(
            FactCustomerAccount,
            Customers.customer_id == FactCustomerAccount.customer_id
        )
        .join(
            DimContract,
            FactCustomerAccount.contract_key == DimContract.contract_key
        )
        .join(
            Services,
            Customers.customer_id == Services.customer_id
        )
        .where(Customers.customer_id == customer_id)
    )

    result = db.execute(query)

    record = result.mappings().first()

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return record