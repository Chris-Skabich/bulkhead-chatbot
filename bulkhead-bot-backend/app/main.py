# FastAPI app initialization & CORS setup
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# Import your database components and models
from app.db.session import engine, Base, SessionLocal
from app.db import models
# Import your new schemas from client.py
from app.schemas.client import LeadCreate, LeadResponse

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

# Dependency: Opens a database session for a request, then safely closes it
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