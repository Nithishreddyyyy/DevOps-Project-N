from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.appraisalCat_service import (
    add_criteria, get_all_criteria, update_criteria, deactivate_criteria, activate_criteria, delete_criteria
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def criteria_page(request: Request):
    data = await get_all_criteria()
    return templates.TemplateResponse("criteria.html", {"request": request, "criteria": data})

@router.post("/create")
async def create_criteria(
    category: str = Form(...),
    name: str = Form(...),
    weight: float = Form(...)
):
    await add_criteria({"category": category, "name": name, "weight": weight})
    return RedirectResponse("/criteria/", status_code=303)

@router.get("/deactivate/{id}")
async def deactivate(id: str):
    await deactivate_criteria(id)
    return RedirectResponse("/criteria/", status_code=303)

@router.get("/activate/{id}")
async def activate(id: str):
    await activate_criteria(id)
    return RedirectResponse("/criteria/", status_code=303)

@router.get("/delete/{id}")
async def delete(id: str):
    await delete_criteria(id)
    return RedirectResponse("/criteria/", status_code=303)
