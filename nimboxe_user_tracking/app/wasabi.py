import csv
import io
import os
import boto3
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

s3_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("WASABI_S3_ENDPOINT"),
    aws_access_key_id=os.getenv("WASABI_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("WASABI_SECRET_KEY"),
    region_name=os.getenv("WASABI_REGION")
)
 
BUCKET = os.getenv("WASABI_BUCKET")


def update_csv_with_user(user_data: dict, csv_filename: str = "usuarios.csv"):
    from datetime import datetime
    unique_fields = ["ip", "city", "region", "country"]
    now_str = datetime.utcnow().isoformat()
    try:
        response = s3_client.get_object(Bucket=BUCKET, Key=csv_filename)
        csv_bytes = response["Body"].read()
        csv_str = csv_bytes.decode("utf-8")
        reader = list(csv.DictReader(io.StringIO(csv_str)))
        print(f"[DEBUG] CSV descargado, filas existentes: {len(reader)}")
    except s3_client.exceptions.NoSuchKey:
        reader = []
        print("[DEBUG] No existe el archivo CSV, se creará uno nuevo.")

    # Buscar si el usuario ya existe
    updated = False
    for row in reader:
        if all(str(row.get(field, "")) == str(user_data.get(field, "")) for field in unique_fields):
            # Actualiza contador y fecha
            visitas = int(row.get("visitas", 1)) + 1
            row["visitas"] = str(visitas)
            row["ultima_visita"] = now_str
            updated = True
            print(f"[DEBUG] Usuario ya existe, contador actualizado a {visitas}")
            break

    if not updated:
        # Nueva fila
        new_row = {k: v for k, v in user_data.items() if isinstance(v, (str, int, float))}
        new_row["visitas"] = "1"
        new_row["ultima_visita"] = now_str
        reader.append(new_row)
        print("[DEBUG] Usuario nuevo agregado al CSV.")

    # Escribe el CSV en memoria
    output = io.StringIO()
    # Asegura que los campos estén completos
    all_fieldnames = set()
    for row in reader:
        all_fieldnames.update(row.keys())
    fieldnames = list(all_fieldnames)
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reader)
    csv_data = output.getvalue()

    s3_client.put_object(
        Bucket=BUCKET,
        Key=csv_filename,
        Body=csv_data.encode("utf-8"),
        ContentType="text/csv"
    )
    print("[DEBUG] CSV actualizado y subido a Wasabi.")
