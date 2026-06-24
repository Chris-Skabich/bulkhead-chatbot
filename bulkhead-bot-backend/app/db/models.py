# DB schemas (Client settings, Leads)
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.session import Base

# Here we are simply setting up a table for leads
# This is what Dylan L. initially suggested should be part of a lead 
class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    # Necessary info
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    # Optional porject specifics
    project_type = Column(String, nullable=True) # Can be Bulkhead, Dock, Boat Lift
    linear_feet = Column(Integer, nullable=True)
    timeline = Column(String, nullable=True)
    # A text box for notes that is once again optional
    notes = Column(Text, nullable=True)
    # Automatically stamps the exact date and time the lead was saved
    created_at = Column(DateTime(timezone=True), server_default=func.now())