from fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy import select, func, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Customers, FactCustomerAccount, DimContract, Services, HighRisk, CustomerMLFeatures
from schemas import CustomerResponse, CustomerFeatures, ChurnPredictionRequest

router = APIRouter()

@router.post("/predict-churn")
#120. Add POST /predict-churn 
async def predict_churn(inputData: ChurnPredictionRequest):

    #121. Return a stub response
    return {
        "customer_id": "N/A",
        "risk_score": 0.78,
        "prediction": "Likely to churn",
        #122. Add a "note" field making it clear this is a stub 
        "note": "stub - real model in ML4"
    }

@router.get("/customers/{customer_id}/features", response_model=CustomerFeatures)
async def get_customer_features(customer_id: str, db: AsyncSession = Depends(get_db)):
    record = db.get(CustomerMLFeatures, customer_id)

    if not record:
        raise HTTPException(status_code=404, detail="Customer not found")

    return record


@router.get("/customers/high-risk")
async def get_high_risk(limit: int = 50, min_tenure: int = 0, max_tenure: int = 100, db: AsyncSession = Depends(get_db)):

    records = db.query(HighRisk).filter(
        HighRisk.tenure >= min_tenure,
        HighRisk.tenure <= max_tenure
    ).limit(limit).all()

    return {
        "Records" : records
    }

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