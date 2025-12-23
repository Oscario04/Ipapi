from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["nimboxe"]

async def test():
    print(await db.list_collection_names())

import asyncio
asyncio.run(test())
