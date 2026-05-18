from fastapi import APIRouter, Request,Form
from fastapi.responses import HTMLResponse , RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List

from app.config.database import faculty_collection
from app.schema.faculty_schema import FacultyCreate
from app.services.faculty_service import (create_faculty,get_all_faculty,get_faculty,update_faculty,delete_faculty)

router = APIRouter()
templates = Jinja2Templates("app/templates")

@router.get('/',response_class=HTMLResponse)
async def faculty_page(request: Request):
    data = await get_all_faculty()
    return templates.TemplateResponse("faculty.html",{"request":request, "faculty":data})

@router.post("/create")
async def create_faculty_route(
    name: str = Form(...),
    department: str = Form(...),
    designation: str = Form(...),
    contact: str = Form(...),
    qualifications: str = Form(...),
    experience: int = Form(...),
    doj: str = Form(...),
    categories: List[str] = Form([])
):
    faculty_data = {
        "name": name,
        "department": department,
        "designation": designation,
        "contact": contact,
        "qualifications": qualifications,
        "experience": experience,
        "doj": doj,
        "categories":categories
    }
    await create_faculty(faculty_data)
    return RedirectResponse("/faculty/",status_code=303)

@router.get("/delete/{id}")
async def delete_faculty_route(id: str):
    await delete_faculty(id)
    return RedirectResponse("/faculty/",status_code=303)