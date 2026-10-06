from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey


class Customers(Base):
    __tablename__ = "customers"

    customer_id = Column(String(20), primary_key=True)
    gender = Column(String(20))
    partner = Column(Boolean)
    dependents = Column(Boolean)
    senior_citizen = Column(Boolean)


class FactCustomerAccount(Base):
    __tablename__ = "fact_customer_account"

    customer_id = Column(
        String(20),
        ForeignKey("customers.customer_id"),
        primary_key=True
    )
    contract_key = Column(
        Integer,
        ForeignKey("dim_contract.contract_key")
    )
    payment_key = Column(Integer)
    tenure = Column(Integer)
    monthly_charges = Column(DECIMAL(10, 2))
    total_charges = Column(DECIMAL(10, 2))
    churn = Column(Boolean)


class DimContract(Base):
    __tablename__ = "dim_contract"

    contract_key = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    contract_type = Column(String(30), unique=True)

class Services(Base):
    __tablename__ = "services"

    customer_id = Column(
        String(20),
        ForeignKey("customers.customer_id"),
        primary_key=True
    )

    phone_service = Column(String(10))
    multiple_lines = Column(String(20))
    internet_service = Column(String(20))
    online_security = Column(String(20))
    online_backup = Column(String(20))
    device_protection = Column(String(20))
    tech_support = Column(String(20))
    streaming_tv = Column(String(20))
    streaming_movies = Column(String(20))

class HighRisk(Base):
    __tablename__ = "v_high_risk_customers"

    customer_id = Column(String(20), primary_key=True)
    tenure = Column(Integer)
    contract_type = Column(String(30))
    monthly_charges = Column(DECIMAL(10, 2))
    risk_reason = Column(String(67))