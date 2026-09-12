# FastAPI app initialization & CORS setup
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

# Database components and models
from app.db.session import engine, SessionLocal
from app.db import models

# Schemas
from app.schemas.client import (
    CompanyCreate, CompanyResponse, 
    LeadCreate, LeadResponse
)

# Services & Tasks
from app.services.excel_gen import generate_leads_excel
from app.services.nlp_parser import normalize_timeline_to_months
from app.tasks.celery_app import test_task, process_and_email_report

# Google OAuth
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

# Sign Up
import uuid

# Optional update for company settings
from typing import Optional

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

class TokenAuth(BaseModel):
    token: str

class SignupAuth(BaseModel):
    token: str
    company_name: str
    
class CompanySettingsUpdate(BaseModel):
    name: str
    report_email: str
    urgency_threshold: float
    is_active: bool
    phone: Optional[str] = None     
    address: Optional[str] = None  

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bulkhead Bot Backend", version="1.0.0")

# Handle CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Health & Testing Endpoints ---

@app.get("/health")
def health_check():
    return {"status": "healthy", "database_connected": "Phase 2 Active!"}

@app.get("/test-celery/{name}")
def test_celery_worker(name: str):
    test_task.delay(name) 
    return {"message": f"Task sent to Redis for {name}! Check your Celery Docker logs."}

@app.get("/test-excel")
def test_download_excel(company_id: int, db: Session = Depends(get_db)):
    file_path = generate_leads_excel(db, company_id=company_id)
    return FileResponse(
        path=file_path, 
        filename=f"company_{company_id}_leads.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.post("/trigger-report/{email}")
def trigger_email_report(email: str):
    process_and_email_report.delay(email)
    return {"message": f"Background job started! Check Mailpit for the email sent to {email}."}


# --- Auth Endpoints ---

@app.post("/auth/google")
def google_auth(data: TokenAuth, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(
            data.token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        user_email = idinfo['email']

        company = db.query(models.Company).filter(models.Company.email == user_email).first()
        if not company:
            raise HTTPException(status_code=404, detail="No company found for this email address.")
        
        return {
            "company_id": company.id, 
            "company_name": company.name, 
            "email": user_email
        }
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    
@app.post("/auth/signup")
def google_signup(data: SignupAuth, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(
            data.token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        user_email = idinfo['email']

        existing_company = db.query(models.Company).filter(models.Company.email == user_email).first()
        if existing_company:
            raise HTTPException(status_code=400, detail="An account with this email already exists. Please log in.")

        new_company = models.Company(
            name=data.company_name,
            email=user_email,
            api_key=f"sk_{uuid.uuid4().hex}",
            report_email=user_email,
            urgency_threshold=3.0,
            is_active=True
        )
        db.add(new_company)
        db.commit()
        db.refresh(new_company)

        return {
            "company_id": new_company.id, 
            "company_name": new_company.name, 
            "email": user_email
        }
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")


# --- Leads Endpoints ---

@app.post("/leads", response_model=LeadResponse)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    lead_data = lead.model_dump()
    if lead.timeline:
        parsed_months = normalize_timeline_to_months(lead.timeline)
        lead_data["timeline_parsed"] = parsed_months
        
    db_lead = models.Lead(**lead_data)
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@app.get("/leads/company/{company_id}", response_model=list[LeadResponse])
def get_company_leads(company_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leads = db.query(models.Lead).filter(models.Lead.company_id == company_id).offset(skip).limit(limit).all()
    if not leads:
        return [] 
    return leads


# --- Company & Settings Endpoints ---

@app.post("/companies", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = models.Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)  
    return db_company

@app.get("/companies")
def get_all_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Company).offset(skip).limit(limit).all()

@app.get("/companies/{company_id}")
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.put("/companies/{company_id}")
def update_company_settings(company_id: int, settings: CompanySettingsUpdate, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company.name = settings.name
    company.report_email = settings.report_email
    company.urgency_threshold = settings.urgency_threshold
    company.is_active = settings.is_active
    company.phone = settings.phone
    company.address = settings.address
    
    db.commit()
    return {"message": "Settings updated successfully"}

@app.delete("/companies/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    # Delete all leads associated with this company first
    db.query(models.Lead).filter(models.Lead.company_id == company_id).delete()
    # Now safely delete the company
    db.delete(company)
    db.commit()
    return {"message": "Company and all associated leads deleted successfully"}