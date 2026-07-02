# Logic to convert DB leads to Excel rows
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from sqlalchemy.orm import Session
from app.db import models

def generate_leads_excel(db: Session) -> str:
    """
    Queries the database for all leads, builds a styled Excel spreadsheet,
    and returns the file path where the report is saved.
    """
    # Fetch all leads from the db
    leads = db.query(models.Lead).order_by(models.Lead.created_at.desc()).all()
    
    # Create a new Excel Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Bulkhead Project Leads"
    
    # Show gridlines explicitly
    ws.views.sheetView[0].showGridLines = True
    
    # Define styles for a professional corporate look
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid") # Navy Blue
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    
    # Write headers
    headers = ["ID", "Name", "Phone", "Project Type", "Linear Feet", "Timeline", "Notes", "Date Created"]
    ws.append(headers)
    
    # Format header row
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
    
    # Populate data rows
    for lead in leads:
        # Format the timestamp nicely for the Excel sheet
        formatted_date = lead.created_at.strftime("%Y-%m-%d %H:%M") if lead.created_at else "N/A"
        
        row = [
            lead.id,
            lead.name,
            lead.phone,
            getattr(lead, 'project_type', 'N/A'),  # Pulls project_type from your new schema
            lead.linear_feet if lead.linear_feet is not None else "N/A",
            getattr(lead, 'timeline', 'N/A'),      # Pulls timeline from your new schema
            lead.notes if lead.notes else "",
            formatted_date
        ]
        ws.append(row)
    
    # Auto-adjust column widths so data doesn't get truncated with "###"
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = col[0].column_letter
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)
        
    # Save the file to a temporary directory inside the container
    output_dir = "/tmp/reports"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"leads_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = os.path.join(output_dir, filename)
    
    wb.save(file_path)
    return file_path