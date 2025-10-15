import os
import boto3
from botocore.client import Config

MINIO_ENDPOINT = "https://minio-api-minio.apps.etlai.lab.t-mobile.com"
ACCESS_KEY = "minio"
SECRET_KEY = "minio123"
BUCKET_NAME = "models"

LOCAL_MODELS_DIR=["~/models/mistral7Binstructv03","~/models/mistralLargeInstruct2407","~/models/mistralNemoInstructFP82407","~/models/phi35MoEinstruct","~/models/phi4reasoning"]

# Create S3 client
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="us-east-1",  # MinIO defaults to this
    verify=False,
)


#s3.put_object(Bucket=BUCKET_NAME, Key="mistralLargeInstruct2407/")

s3.upload_file("../models/mistralLargeInstruct2407/README.md",BUCKET_NAME, "mistralLargeInstruct2407/README.md")

