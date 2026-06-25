# FastAPI app initialization & CORS setup
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# Import your database components and models
from app.db.session import engine, Base, SessionLocal
from app.db import models
# Import your new schemas from client.py
from app.schemas.client import LeadCreate, LeadResponse
# Celetty import
from app.tasks.celery_app import test_task
# Fast API Excel imports
from fastapi.responses import FileResponse
from app.services.excel_gen import generate_leads_excel
from app.db.session import get_db

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
    # Convert Pydantic schema to SQLAlchemy model
    db_lead = models.Lead(**lead.model_dump())
    # Save to database
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead) # Fetches the new ID and created_at timestamp
    return db_lead

@app.get("/leads", response_model=list[LeadResponse])
def get_all_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Retrieve leads from the database
    leads = db.query(models.Lead).offset(skip).limit(limit).all()
    return leads

@app.get("/test-celery/{name}")
def test_celery_worker(name: str):
    test_task.delay(name) # Passes over to Redis
    return {"message": f"Task sent to Redis for {name}! Check your Celery Docker logs."}

@app.get("/test-excel")
def test_download_excel(db: Session = Depends(get_db)):
    # Trigger the function we just wrote to build the Excel file
    file_path = generate_leads_excel(db)
    # Send that file out of Docker and into your web browser!
    return FileResponse(
        path=file_path, 
        filename="Bulkhead_Test_Report.xlsx", 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )