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

def upload_user_data(user_data: dict):
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{user_data['ip']}_{timestamp}.json"
    
    s3_client.put_object(
        Bucket=BUCKET,
        Key=filename,
        Body=json.dumps(user_data),
        ContentType="application/json"
    )
