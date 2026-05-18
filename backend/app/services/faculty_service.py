from app.config.database import faculty_collection, criteria_collection
from bson import ObjectId

def faculty_helper(f):
    return{
        "id" : str(f["_id"]),
        "name" : f["name"],
        "department" : f["department"],
        "designation" : f["designation"],
        "contact" : f["contact"],
        "qualifications" : f["qualifications"],
        "experience" : f["experience"],
        "doj" : f["doj"],
        "categories": f.get("categories",[])
    }
async def create_faculty(data : dict):
    res = await faculty_collection.insert_one(data)
    return str(res.inserted_id)

async def get_all_faculty():
    fac = []
    async for f in faculty_collection.find():
        fac.append(faculty_helper(f))
    return fac

async def get_faculty(id : str):
    fac = await faculty_collection.find_one({"_id":ObjectId(id)})
    if fac:
        return faculty_helper(fac)

async def update_faculty(id:str,data:dict):
    await faculty_collection.update_one({"_id":ObjectId(id)},{"$set":data})
    return True

async def delete_faculty(id:str):
    await faculty_collection.delete_one({"_id":ObjectId(id)})
    return True


