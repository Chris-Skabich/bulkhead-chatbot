# FastAPI app initialization & CORS setup

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Bulkhead Bot Backend", version="1.0.0")

#Handle CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "database_connected": "Pending Phase 2"}