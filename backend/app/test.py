import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Your existing setup
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client["faculty_appraisal"]

# Note: The collections are defined but not used in the connection test itself.
faculty_collection = db["faculty"]
criteria_collection = db["criteria"]
documents_collection = db["documents_metadata"]
scores_collection = db["scores"]

# --- Test Function ---
async def test_mongo_connection():
    """
    Checks the connection to MongoDB by sending an 'isMaster'/'ping' 
    command to the database administration.
    """
    print(f"Attempting to connect to MongoDB at: {MONGO_URI}")
    try:
        # Use a non-database-specific command like 'ping' on the admin database.
        # This will raise a ServerSelectionTimeoutError if the connection fails.
        await client.admin.command('ping') 
        
        print("✅ MongoDB connection successful!")
        # Optional: You can also print the server version or status info
        # info = await client.server_info()
        # print(f"Server Info: {info['version']}")
        
        return True
    
    except Exception as e:
        print(f"❌ MongoDB connection failed. Error: {e}")
        return False
    finally:
        # It's good practice to close the client if you open it just for a check.
        # In a FastAPI app, you'd typically leave it open, but for a standalone test, close it.
        # client.close() 
        pass

# --- Execution Block ---
# Run the asynchronous function
if __name__ == "__main__":
    # Get the event loop and run the test
    asyncio.run(test_mongo_connection())
    
    # You can also use client.close() here if you're not using it in FastAPI's shutdown event
    # client.close()