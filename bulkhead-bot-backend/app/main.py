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
    LeadCreate, LeadResponse, 
    ClientSettingsCreate, ClientSettingsResponse
)

# Services & Tasks
from app.services.excel_gen import generate_leads_excel
from app.services.nlp_parser import normalize_timeline_to_months
from app.tasks.celery_app import test_task, process_and_email_report


# Initialize database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bulkhead Bot Backend", version="1.0.0")

# Handle CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Opens a database session for a request, then safely closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "database_connected": "Phase 2 Active!"}

@app.post("/leads", response_model=LeadResponse)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    # Convert the incoming Pydantic schema into a Python dictionary
    lead_data = lead.model_dump()
    
    # If the user provided a timeline, run it through the NLP parser
    if lead.timeline:
        parsed_months = normalize_timeline_to_months(lead.timeline)
        lead_data["timeline_parsed"] = parsed_months
        
    # Pass the updated dictionary to the database model
    db_lead = models.Lead(**lead_data)
    
    # Save to database
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

# Company endpoints
@app.post("/companies", response_model=CompanyResponse)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = models.Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)  
    return db_company

@app.get("/companies", response_model=list[CompanyResponse])
def get_all_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = db.query(models.Company).offset(skip).limit(limit).all()
    return companies

@app.get("/companies/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.delete("/companies/{company_id}", response_model=CompanyResponse)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(company)
    db.commit()
    return company

# Client Settings endpoints
@app.post("/client-settings", response_model=ClientSettingsResponse)
def create_client_settings(settings: ClientSettingsCreate, db: Session = Depends(get_db)):
    db_settings = models.ClientSettings(**settings.model_dump())
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings

@app.get("/client-settings", response_model=list[ClientSettingsResponse])
def get_all_client_settings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ClientSettings).offset(skip).limit(limit).all()

@app.get("/client-settings/company/{company_id}", response_model=ClientSettingsResponse)
def get_settings_by_company_id(company_id: int, db: Session = Depends(get_db)):
    settings = db.query(models.ClientSettings).filter(models.ClientSettings.company_id == company_id).first()
    if not settings:
        raise HTTPException(status_code=404, detail=f"No settings found for company ID {company_id}")
    return settings