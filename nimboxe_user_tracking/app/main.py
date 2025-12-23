from fastapi import FastAPI
from app.models.user import UserVisit
from app.db.mongodb import collection
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.wasabi import upload_user_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Permite cualquier origen, o reemplaza con tu dominio
    allow_methods=["*"],   # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],   # Permite cualquier header
)
# Montar carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/all-users")
async def get_all_users():
    users = []
    async for doc in collection.find():
        doc["_id"] = str(doc["_id"])  # convierte ObjectId a string para JSON
        users.append(doc)
    return users

@app.post("/track")
async def track_user(user: UserVisit):
    user_dict = user.dict()
    print("Datos que llegan al backend:", user_dict)  # <-- agrega esto
    try:
        upload_user_data(user_dict)
        return {"message": "Usuario trackeado"}
    except Exception as e:
        print("Error subiendo a Wasabi:", e)  # <-- imprime el error real
        return {"error": str(e)}, 500
