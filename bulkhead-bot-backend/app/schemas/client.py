# Validating admin settings
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base properties shared across all lead interactions (same as in db/models.py)
class LeadBase(BaseModel):
    name: str
    phone: str
    project_type: Optional[str] = None
    linear_feet: Optional[int] = None
    timeline: Optional[str] = None
    notes: Optional[str] = None
# Schema for creating a lead (what the user sends via API)
class LeadCreate(LeadBase):
    pass
# Schema for reading a lead (what the API sends back, including DB-generated fields)
class LeadResponse(LeadBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True  # Tells Pydantic to read data from SQLAlchemy models

# Base Properties shared across schemas
class CompanyBase(BaseModel):
    name: str
    email: Optional[str] = None
    api_key: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

#Schema for Post requests
class CompanyCreate(CompanyBase):
    pass

#schema for API responses (returning a company)
class CompanyResponse(CompanyBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Tells Pydantic to read data from SQLAlchemy models
