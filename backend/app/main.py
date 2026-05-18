from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routes.faculty_route import router as faculty_router
from app.routes.appraisalCat_route import router as criteria_router
from app.routes.crit_score_route import router as score_router
from app.routes.api_route import router as api_router
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    return{
        "message": "Hello world"
    }

app.include_router(faculty_router, prefix="/faculty")
app.include_router(criteria_router, prefix="/criteria")
app.include_router(score_router, prefix = "/scores")
app.include_router(api_router)
