from pydantic import BaseModel

class FacultyCriterionScore(BaseModel):
    faculty_id: str
    criterion_name: str
    score: float