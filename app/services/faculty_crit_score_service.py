from app.config.database import faculty_collection, criteria_collection, scores_collection
from bson import ObjectId

def faculty_crit_score_helper(fcs):
    return {
        "id": str(fcs["_id"]),
        "faculty_id": fcs["faculty_id"],
        "criterion_name": fcs["criterion_name"],
        "score": fcs["score"]
    }

async def create_faculty_crit_score(data: dict):
    """Create a new faculty criterion score record"""
    res = await scores_collection.insert_one(data)
    return str(res.inserted_id)

async def get_all_faculty_scores():
    """Get all faculty criterion scores"""
    scores = []
    async for score in scores_collection.find():
        scores.append(faculty_crit_score_helper(score))
    return scores

async def get_faculty_score(faculty_id: str):
    """Get criterion scores for a specific faculty"""
    score = await scores_collection.find_one({"faculty_id": faculty_id})
    if score:
        return faculty_crit_score_helper(score)
    return None

async def calculate_total_score(faculty_id: str):
    """Calculate total appraisal score using criterion weights"""
    score_doc = await scores_collection.find_one({"faculty_id": faculty_id})
    if not score_doc:
        return 0

    criterion_names = score_doc.get("criterion_name", [])
    total_score = 0

    for criterion_name in criterion_names:
        criterion = await criteria_collection.find_one({"name": criterion_name, "is_active": True})
        if criterion:
            total_score += criterion.get("weight", 0)

    return total_score

async def initialize_faculty_scores():
    """Initialize scores for all faculty with empty criteria list"""
    # Get all faculty
    faculty_list = []
    async for faculty in faculty_collection.find():
        faculty_list.append(faculty)

    # Create score records for each faculty
    for faculty in faculty_list:
        existing = await scores_collection.find_one({"faculty_id": str(faculty["_id"])})
        if not existing:
            await create_faculty_crit_score({
                "faculty_id": str(faculty["_id"]),
                "criterion_name": [],
                "score": 0.0
            })

async def update_faculty_score(faculty_id: str, criterion_name: list):
    """Update the selected criteria for a faculty and auto-calculate score"""
    await scores_collection.update_one(
        {"faculty_id": faculty_id},
        {"$set": {"criterion_name": criterion_name, "score": 0.0}},
        upsert=True
    )
    return True
