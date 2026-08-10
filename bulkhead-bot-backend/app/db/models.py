# DB schemas (Client settings, Leads)
from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, ForeignKey, JSON, Float, Boolean
from sqlalchemy.sql import func
from app.db.session import Base

# Here we are simply setting up a table for leads
# This is what Dylan L. initially suggested should be part of a lead 
class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    # Necessary info
    name = Column(String, nullable=False)
    phone = Column(Text, nullable=True) # Removed "Phone"
    # Optional porject specifics
    project_type = Column(String, nullable=True) # Can be Bulkhead, Dock, Boat Lift
    linear_feet = Column(Integer, nullable=True)
    timeline = Column(String, nullable=True)
    timeline_parsed = Column(Float, nullable=True) # New lead column to measure urgency
    # A text box for notes that is once again optional
    notes = Column(Text, nullable=True)
    # Automatically stamps the exact date and time the lead was saved
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    # Mapping exact column names from your database screenshot
    email = Column(Text, nullable=True) # Removed "Email"
    api_key = Column(Text, nullable=True)
    phone = Column(Text, nullable=True) # Removed "Phone" and changed to Text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    address = Column(Text, nullable=True)

class client_settings(Base):
    __tablename__ = "client_settings"

    id = Column(BigInteger, primary_key=True, index=True)  # int8 in Supabase
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    api_key = Column(Text, nullable=True)
    company_name = Column(Text, nullable=True)
    report_email = Column(Text, nullable=True)
    business_hours = Column(JSON, nullable=True)  # jsonb column
    urgency_threshold = Column(Float, nullable=True)  # float4 column
    is_active = Column(Boolean, default=True)  # bool column
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)