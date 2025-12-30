def serialize_datetimes(obj):
    if isinstance(obj, dict):
        return {k: serialize_datetimes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetimes(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj
from fastapi import FastAPI
from Ipapi.nimboxe_user_tracking.app.models.user import UserVisit
from Ipapi.nimboxe_user_tracking.app.db.mongodb import collection
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from Ipapi.nimboxe_user_tracking.app.wasabi import update_csv_with_user
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Permite cualquier origen, o reemplaza con tu dominio
    allow_methods=["*"],   # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],   # Permite cualquier header
)
# Montar carpeta static

static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/all-users")
async def get_all_users():
    print("[DEBUG] Iniciando consulta de usuarios en MongoDB...")
    users = []
    async for doc in collection.find():
        print(f"[DEBUG] Documento encontrado: {doc}")
        doc["_id"] = str(doc["_id"])
        users.append(doc)
        try:
            serializable_doc = serialize_datetimes(doc)
            print(f"[DEBUG] Subiendo usuario a Wasabi: {serializable_doc}")
            update_csv_with_user(serializable_doc)
            print("[DEBUG] Subida exitosa a Wasabi")
        except Exception as e:
            print(f"[ERROR] Fallo al subir a Wasabi: {e}")
    print(f"[DEBUG] Total usuarios encontrados: {len(users)}")
    return users


@app.post("/track")
async def track_user(user: UserVisit):
    user_dict = user.dict()
    print("Datos que llegan al backend:", user_dict)
    try:
        # Subir a Wasabi como CSV único
        update_csv_with_user(user_dict)
        print("[DEBUG] Usuario procesado en CSV de Wasabi")
        return {"message": "Usuario trackeado y CSV actualizado"}
    except Exception as e:
        print("Error subiendo a Wasabi:", e)
        return {"error": str(e)}, 500
