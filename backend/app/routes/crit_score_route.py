from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO

from app.services.faculty_crit_score_service import (
    get_faculty_score,
    calculate_total_score,
    update_faculty_score,
    initialize_faculty_scores
)
from app.services.faculty_service import get_all_faculty, get_faculty
from app.services.appraisalCat_service import get_all_criteria

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def scores_page(request: Request):
    await initialize_faculty_scores()
    faculty_list = await get_all_faculty()
    criteria_list = await get_all_criteria()
    
    faculty_with_scores = []
    for faculty in faculty_list:
        score_data = await get_faculty_score(faculty["id"])
        total_score = await calculate_total_score(faculty["id"])
        faculty_with_scores.append({
            **faculty,
            "selected_criteria": score_data.get("criterion_name", []) if score_data else [],
            "total_score": total_score
        })
    
    return templates.TemplateResponse("scores.html", {
        "request": request,
        "scores": faculty_with_scores,
        "all_criteria": criteria_list
    })

@router.post("/update/{faculty_id}")
async def update_score(
    faculty_id: str,
    criteria: list = Form(default=[])
):
    await update_faculty_score(faculty_id, criteria)
    return RedirectResponse("/scores/", status_code=303)

@router.get("/pdf/all")
async def generate_all_pdf():
    all_faculty = await get_all_faculty()
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []
    
    # Title
    title_style = styles['Title']
    title = Paragraph("Complete Faculty Appraisal Report", title_style)
    story.append(title)
    story.append(Spacer(1, 12))
    
    # College Name
    college_style = styles['Heading2']
    college = Paragraph("Ramaiah Institute of Technology", college_style)
    story.append(college)
    story.append(Spacer(1, 12))
    
    # Department
    dept_style = styles['Heading3']
    dept = Paragraph("Department of Information Science and Engineering", dept_style)
    story.append(dept)
    story.append(Spacer(1, 24))
    
    # Report Date
    from datetime import datetime
    report_date = Paragraph(f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    story.append(report_date)
    story.append(Spacer(1, 24))
    
    for faculty in all_faculty:
        # Faculty Section Header
        faculty_header = Paragraph(f"<b>Faculty: {faculty['name']}</b>", styles['Heading4'])
        story.append(faculty_header)
        story.append(Spacer(1, 6))
        
        # Faculty Details
        normal_style = styles['Normal']
        story.append(Paragraph(f"<b>Department:</b> {faculty['department']}", normal_style))
        story.append(Paragraph(f"<b>Designation:</b> {faculty['designation']}", normal_style))
        story.append(Paragraph(f"<b>Contact:</b> {faculty['contact']}", normal_style))
        story.append(Paragraph(f"<b>Qualifications:</b> {faculty['qualifications']}", normal_style))
        story.append(Paragraph(f"<b>Experience:</b> {faculty['experience']} years", normal_style))
        story.append(Paragraph(f"<b>Date of Joining:</b> {faculty['doj']}", normal_style))
        
        # Appraisal Details
        score_data = await get_faculty_score(faculty['id'])
        total_score = await calculate_total_score(faculty['id'])
        criteria_list = score_data.get("criterion_name", []) if score_data else []
        
        story.append(Paragraph(f"<b>Selected Criteria:</b> {', '.join(criteria_list) if criteria_list else 'None'}", normal_style))
        story.append(Paragraph(f"<b>Total Appraisal Score:</b> {total_score:.2f}", normal_style))
        
        # Separator
        story.append(Spacer(1, 12))
        story.append(Paragraph("-" * 50, styles['Normal']))
        story.append(Spacer(1, 12))
    
    doc.build(story)
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=all_faculty_appraisal.pdf"}
    )
@router.get("/pdf/{faculty_id}")
async def generate_faculty_pdf(faculty_id: str):
    from fastapi import HTTPException
    faculty = await get_faculty(faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []
    
    # Title
    title_style = styles['Title']
    title = Paragraph("Faculty Appraisal Report", title_style)
    story.append(title)
    story.append(Spacer(1, 12))
    
    # College Name
    college_style = styles['Heading2']
    college = Paragraph("Ramaiah Institute of Technology", college_style)
    story.append(college)
    story.append(Spacer(1, 12))
    
    # Department
    dept_style = styles['Heading3']
    dept = Paragraph("Department of Information Science and Engineering", dept_style)
    story.append(dept)
    story.append(Spacer(1, 24))
    
    # Report Date
    from datetime import datetime
    report_date = Paragraph(f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    story.append(report_date)
    story.append(Spacer(1, 24))
    
    # Faculty Section Header
    faculty_header = Paragraph(f"<b>Faculty: {faculty['name']}</b>", styles['Heading4'])
    story.append(faculty_header)
    story.append(Spacer(1, 6))
    
    # Faculty Details
    normal_style = styles['Normal']
    story.append(Paragraph(f"<b>Department:</b> {faculty['department']}", normal_style))
    story.append(Paragraph(f"<b>Designation:</b> {faculty['designation']}", normal_style))
    story.append(Paragraph(f"<b>Contact:</b> {faculty['contact']}", normal_style))
    story.append(Paragraph(f"<b>Qualifications:</b> {faculty['qualifications']}", normal_style))
    story.append(Paragraph(f"<b>Experience:</b> {faculty['experience']} years", normal_style))
    story.append(Paragraph(f"<b>Date of Joining:</b> {faculty['doj']}", normal_style))
    
    # Appraisal Details
    score_data = await get_faculty_score(faculty['id'])
    total_score = await calculate_total_score(faculty['id'])
    criteria_list = score_data.get("criterion_name", []) if score_data else []
    
    story.append(Paragraph(f"<b>Selected Criteria:</b> {', '.join(criteria_list) if criteria_list else 'None'}", normal_style))
    story.append(Paragraph(f"<b>Total Appraisal Score:</b> {total_score:.2f}", normal_style))
    
    doc.build(story)
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={faculty['name']}_appraisal.pdf"}
    )
