from pydantic import BaseModel, Field
from datetime import date
from enum import Enum

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class IndianState(str, Enum):
    # States
    ANDHRA_PRADESH = "Andhra Pradesh"
    ARUNACHAL_PRADESH = "Arunachal Pradesh"
    ASSAM = "Assam"
    BIHAR = "Bihar"
    CHHATTISGARH = "Chhattisgarh"
    GOA = "Goa"
    GUJARAT = "Gujarat"
    HARYANA = "Haryana"
    HIMACHAL_PRADESH = "Himachal Pradesh"
    JHARKHAND = "Jharkhand"
    KARNATAKA = "Karnataka"
    KERALA = "Kerala"
    MADHYA_PRADESH = "Madhya Pradesh"
    MAHARASHTRA = "Maharashtra"
    MANIPUR = "Manipur"
    MEGHALAYA = "Meghalaya"
    MIZORAM = "Mizoram"
    NAGALAND = "Nagaland"
    ODISHA = "Odisha"
    PUNJAB = "Punjab"
    RAJASTHAN = "Rajasthan"
    SIKKIM = "Sikkim"
    TAMIL_NADU = "Tamil Nadu"
    TELANGANA = "Telangana"
    TRIPURA = "Tripura"
    UTTAR_PRADESH = "Uttar Pradesh"
    UTTARAKHAND = "Uttarakhand"
    WEST_BENGAL = "West Bengal"

    # Union Territories
    ANDAMAN_AND_NICOBAR_ISLANDS = "Andaman and Nicobar Islands"
    CHANDIGARH = "Chandigarh"
    DADRA_AND_NAGAR_HAVELI_AND_DAMAN_AND_DIU = "Dadra and Nagar Haveli and Daman and Diu"
    DELHI = "Delhi"
    JAMMU_AND_KASHMIR = "Jammu and Kashmir"
    LADAKH = "Ladakh"
    LAKSHADWEEP = "Lakshadweep"
    PUDUCHERRY = "Puducherry"

class CreateCustomer(BaseModel):
    telecom_partner: str
    gender: Gender
    age: int
    state: IndianState
    city: str
    pincode: int = Field(
        ...,
        ge=100000,
        le=999999,
        description="6-digit Indian PIN code"
    )
    date_of_registration: date
    num_dependents: int
    estimated_salary: int
    calls_made: int
    sms_sent: int
    data_used: int
    churn: bool

class _Unset:
    pass

UNSET = _Unset()

class UpdateCustomer(BaseModel):
    customer_id: int
    telecom_partner: str | None = UNSET
    gender: Gender | None = UNSET
    age: int | None = Field(UNSET, ge=0, le=120)
    state: IndianState | None = UNSET
    city: str | None = UNSET
    pincode: int | None = Field(
        UNSET,
        ge=100000,
        le=999999,
        description="6-digit Indian PIN code"
    )
    date_of_registration: date | None = UNSET
    num_dependents: int | None = Field(UNSET, ge=0)
    estimated_salary: int | None = Field(UNSET, ge=0)
    calls_made: int | None = Field(UNSET, ge=0)
    sms_sent: int | None = Field(UNSET, ge=0)
    data_used: int | None = Field(UNSET, ge=0)
    churn: bool | None = UNSET