import os
from celery import Celery
from app.db.session import SessionLocal
from app.services.excel_gen import generate_leads_excel
from app.services.email_sender import send_leads_report_email

# Securely pull the Redis URL from the environment
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "bulkhead_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
)

# Now lets test connection
@celery_app.task(name="test_celery_connection")
def test_task(name: str):
    message = f"Success! Celery is processing a background task for {name}"
    print(message)  # This will print inside your Celery Docker terminal logs
    return message

@celery_app.task(name="process_and_email_report")
def process_and_email_report(recipient_email: str):
    """
    Background job that opens the database, generates the Excel file,
    emails it to the provided address, and closes the database connection safely.
    """
    # Manually open a database session for the worker
    db = SessionLocal()
    try:
        print(f"Worker started: Generating Excel report for {recipient_email}...")
        
        # Generate the Excel sheet
        excel_path = generate_leads_excel(db)
        
        # Email the sheet
        print(f"Excel generated at {excel_path}. Sending email...")
        send_leads_report_email(recipient_email, excel_path)
        
        return f"Report successfully processed and sent to {recipient_email}"
    
    except Exception as e:
        print(f"Error in background task: {e}")
        return str(e)
    
    finally:
        # ALWAYS close the database connection so the app doesn't crash!
        db.close()