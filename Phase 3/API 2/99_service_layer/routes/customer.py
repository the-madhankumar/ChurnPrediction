from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Customers, FactCustomerAccount, DimContract, Services
from schemas import CustomerResponse


router = APIRouter()

@router.get("/churn/summary")
async def get_churn_summary(db: AsyncSession = Depends(get_db)):
    total_customers = db.query(
        func.count(Customers.customer_id)
    ).scalar()

    total_churned = db.query(
        func.count(Customers.customer_id)
    ).join(
        FactCustomerAccount,
        Customers.customer_id == FactCustomerAccount.customer_id
    ).filter(
        FactCustomerAccount.churn == 1
    ).scalar()

    churn_rate = total_churned / total_customers


    churn_rate_by_contract_type = dict(
        db.query(
            DimContract.contract_type,
            ((
                func.sum(FactCustomerAccount.churn.cast(Integer))
                / func.count(FactCustomerAccount.customer_id)
            ) * 100).label("churn_rate")
        ).join(
            DimContract,
            DimContract.contract_key == FactCustomerAccount.contract_key
        ).group_by(
            DimContract.contract_type
        ).all()
    )

    churn_rate_by_internet_service = dict(
        db.query(
            Services.internet_service,
            ((
                func.sum(FactCustomerAccount.churn.cast(Integer))
                / func.count(FactCustomerAccount.customer_id)
            ) * 100).label("churn_rate")
        ).join(
            Services,
            Services.customer_id == FactCustomerAccount.customer_id
        ).group_by(
            Services.internet_service
        ).all()
    )

    return {
        "total_customers": float(total_customers),
        "total_churned": float(total_churned),
        "churn_rate": round(churn_rate * 100, 2),
        "contract_type": [
            {
                f"{contract_type}": churn_rate
            }
            for contract_type, churn_rate in churn_rate_by_contract_type.items()
        ],
        "internet_servie": [
            {
                f"{internet_service}" : churn_rate
            }
            for internet_service, churn_rate in churn_rate_by_internet_service.items()
        ]
    }

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