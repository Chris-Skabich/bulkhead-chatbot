# DB schemas (Client settings, Leads)
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
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
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

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

class ClientSettings(Base):
    __tablename__ = "client_settings" # Make sure this matches your Supabase table name exactly
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), unique=True)
    company_name = Column(String)
    api_key = Column(String)
    report_email = Column(String)
    # {"Monday": "9-5", "Tuesday": "9-5", "Weekend": "Closed"}
    business_hours = Column(JSON, default={}) 
    urgency_threshold = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Optional: Relationship back to Company (if your Company model expects it)
    # company = relationship("Company", back_populates="settings")