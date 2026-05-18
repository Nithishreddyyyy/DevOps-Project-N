from app.config.database import criteria_collection
from bson import ObjectId

def criteria_helper(c):
    return{
        "id" : str(c["_id"]),
        "category" : c["category"],
        "name" : c["name"],
        "weight" : c["weight"],
        "is_active" : c["is_active"]
    }

async def add_criteria(data : dict):
    res = await criteria_collection.insert_one({**data, "is_active" : True})
    return str(res.inserted_id)

async def get_all_criteria ():
    cri = []
    async for c in criteria_collection.find():
        cri.append(criteria_helper(c))
    return cri  

async def update_criteria(id : str , data : dict):
    await criteria_collection.update_one({"_id":ObjectId},{"$set":data})
    return True

async def deactivate_criteria(id: str):
    await criteria_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": {"is_active": False}}
    )
    return True

async def activate_criteria(id: str):
    await criteria_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": {"is_active": True}}
    )
    return True

async def delete_criteria(id: str):
    await criteria_collection.delete_one({"_id": ObjectId(id)})
    return True

