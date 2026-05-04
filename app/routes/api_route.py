from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.appraisalCat_service import (
    activate_criteria,
    add_criteria,
    deactivate_criteria,
    delete_criteria,
    get_all_criteria,
)
from app.services.faculty_crit_score_service import (
    calculate_total_score,
    get_faculty_score,
    initialize_faculty_scores,
    update_faculty_score,
)
from app.services.faculty_service import (
    create_faculty,
    delete_faculty,
    get_all_faculty,
    get_faculty,
)

router = APIRouter(prefix="/api", tags=["api"])


class FacultyPayload(BaseModel):
    name: str
    department: str
    designation: str
    contact: str = ""
    qualifications: str = ""
    experience: int = Field(default=0, ge=0)
    doj: str
    categories: List[str] = []


class CriteriaPayload(BaseModel):
    category: str
    name: str
    weight: float = Field(ge=0)


class ScorePayload(BaseModel):
    criteria: List[str] = []


@router.get("/faculty")
async def list_faculty():
    return await get_all_faculty()


@router.post("/faculty", status_code=201)
async def create_faculty_api(payload: FacultyPayload):
    faculty_id = await create_faculty(payload.model_dump())
    faculty = await get_faculty(faculty_id)
    return faculty


@router.delete("/faculty/{faculty_id}")
async def delete_faculty_api(faculty_id: str):
    faculty = await get_faculty(faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    await delete_faculty(faculty_id)
    return {"deleted": True}


@router.get("/criteria")
async def list_criteria():
    return await get_all_criteria()


@router.post("/criteria", status_code=201)
async def create_criteria_api(payload: CriteriaPayload):
    criteria_id = await add_criteria(payload.model_dump())
    criteria = await get_all_criteria()
    return next((item for item in criteria if item["id"] == criteria_id), None)


@router.patch("/criteria/{criteria_id}/status")
async def update_criteria_status(criteria_id: str, is_active: bool):
    if is_active:
        await activate_criteria(criteria_id)
    else:
        await deactivate_criteria(criteria_id)

    return {"id": criteria_id, "is_active": is_active}


@router.delete("/criteria/{criteria_id}")
async def delete_criteria_api(criteria_id: str):
    await delete_criteria(criteria_id)
    return {"deleted": True}


@router.get("/scores")
async def list_scores():
    await initialize_faculty_scores()
    faculty_list = await get_all_faculty()
    criteria_list = await get_all_criteria()

    faculty_with_scores = []
    for faculty in faculty_list:
        score_data = await get_faculty_score(faculty["id"])
        total_score = await calculate_total_score(faculty["id"])
        faculty_with_scores.append(
            {
                **faculty,
                "selected_criteria": score_data.get("criterion_name", [])
                if score_data
                else [],
                "total_score": total_score,
            }
        )

    return {"scores": faculty_with_scores, "criteria": criteria_list}


@router.put("/scores/{faculty_id}")
async def update_score_api(faculty_id: str, payload: ScorePayload):
    faculty = await get_faculty(faculty_id)
    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    await update_faculty_score(faculty_id, payload.criteria)
    return {
        "faculty_id": faculty_id,
        "selected_criteria": payload.criteria,
        "total_score": await calculate_total_score(faculty_id),
    }
