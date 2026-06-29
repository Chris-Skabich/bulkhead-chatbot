# Native SMTP & Webhook notification logic
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Docker networks Mailpit by its service name. Mailpit receives emails on port 1025.
SMTP_SERVER = os.getenv("SMTP_SERVER", "mailpit")
SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
SENDER_EMAIL = "bot@bulkhead-app.local" # This can be completely fake for Mailpit

def send_leads_report_email(recipient_email: str, excel_file_path: str):
    """
    Constructs an email with the Excel report attached and sends it via Mailpit.
    """
    subject = "Daily Bulkhead Leads Report"
    body = "Hello Team,\n\nPlease find the latest bulkhead project leads attached to this email.\n\nBest,\nAutomated Bot"
    
    # Build the Email Envelope
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the Body Text
    msg.attach(MIMEText(body, 'plain'))

    # Attach the Excel File
    if excel_file_path and os.path.exists(excel_file_path):
        with open(excel_file_path, "rb") as attachment:
            # Create the attachment payload
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            
        # Encode it in base64 so it can travel safely over email protocols
        encoders.encode_base64(part)
        
        # Give it a filename in the email
        filename = os.path.basename(excel_file_path)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={filename}'
        )
        msg.attach(part)
    else:
        print(f"Warning: Could not find attachment at {excel_file_path}")

    # Connect to the SMTP Server (Mailpit) and Send
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            # No login required for Mailpit! Just send it.
            server.send_message(msg)
        print(f"Successfully routed email to {recipient_email} via Mailpit.")
    except Exception as e:
        print(f"Failed to send email: {e}")