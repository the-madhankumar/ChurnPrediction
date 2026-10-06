from fastapi import APIRouter, Depends
from schemas import CreateCustomer, UpdateCustomer, UNSET
from models import Customers
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create", tags=["Create"])
def create_customer(data: CreateCustomer, db: Session = Depends(get_db)):
    new_user = Customers(
        telecom_partner=data.telecom_partner,
        gender=data.gender,
        age=data.age,
        state=data.state,
        city=data.city,
        pincode=data.pincode,
        date_of_registration=data.date_of_registration,
        num_dependents=data.num_dependents,
        estimated_salary=data.estimated_salary,
        calls_made=data.calls_made,
        sms_sent=data.sms_sent,
        data_used=data.data_used,
        churn=data.churn
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Record Inserted Successfully",
        "data": new_user
    }

@router.get("/read", tags=["Read"])
def get_customers(db: Session = Depends(get_db)):
    records = db.query(Customers).all()

    if not records:
        return {
            "error": "No Records Found"
        }

    return records

@router.get("/read/{customer_id}", tags=["Read"])
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    record = db.get(Customers, customer_id)

    if not record:
        return {
            "error": "No Records Found"
        }
    
    return record

@router.put("/update", tags=["Update"])
def update_data(data: UpdateCustomer, db: Session = Depends(get_db)):
    record = db.get(Customers, data.customer_id)

    if data.telecom_partner is not UNSET:
        record.telecom_partner = data.telecom_partner

    if data.gender is not UNSET:
        record.gender = data.gender

    if data.age is not UNSET:
        record.age = data.age

    if data.state is not UNSET:
        record.state = data.state

    if data.city is not UNSET:
        record.city = data.city

    if data.pincode is not UNSET:
        record.pincode = data.pincode

    if data.date_of_registration is not UNSET:
        record.date_of_registration = data.date_of_registration

    if data.num_dependents is not UNSET:
        record.num_dependents = data.num_dependents

    if data.estimated_salary is not UNSET:
        record.estimated_salary = data.estimated_salary

    if data.calls_made is not UNSET:
        record.calls_made = data.calls_made

    if data.sms_sent is not UNSET:
        record.sms_sent = data.sms_sent

    if data.data_used is not UNSET:
        record.data_used = data.data_used

    if data.churn is not UNSET:
        record.churn = data.churn

    db.commit()
    db.refresh(record)

    return record

@router.delete("/delete", tags=["Delete"])
def delete_all(db: Session = Depends(get_db)):
    db.query(Customers).delete()
    db.commit()

    return {
        "message": "All Records Deleted"
    }

@router.delete("/delete/{customer_id}", tags=["Delete"])
def delete_by_id(customer_id: int, db: Session = Depends(get_db)):
    record = db.get(Customers, customer_id)

    if not record:
        return {
            "error": "User Not Found"
        }

    db.delete(record)

    return {
        "message": f"Customer ID: {customer_id} deleted from database successfully"
    }