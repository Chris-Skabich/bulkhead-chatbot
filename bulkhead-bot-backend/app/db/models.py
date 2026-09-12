# DB schemas (Client settings, Leads)
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.sql import func
from app.db.session import Base
from datetime import datetime

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
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True) # Google OAuth Login Email
    api_key = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    report_email = Column(String, nullable=True) # Where lead notifications are sent
    urgency_threshold = Column(Float, default=3.0) # Months
    is_active = Column(Boolean, default=True) # Widget Kill Switch