import os
import boto3
from botocore.client import Config
import warnings

warnings.filterwarnings("ignore")

## NetAPP S3
##URL - https://klsvmetl101:8443/redhat-bucket1
## Access Key - 14AOD5215XEMZS3WLJPZ
##Secret Key - 9ipn0d3oc0h98_LPiY2XYS_v8uKCFP4A6476OAAE

# MinIO server configuration
#MINIO_ENDPOINT =  "https://10.0.18.5:8443"
#ACCESS_KEY = "14AOD5215XEMZS3WLJPZ"
#SECRET_KEY = "9ipn0d3oc0h98_LPiY2XYS_v8uKCFP4A6476OAAE"
#BUCKET_NAME = "redhat-bucket1"
#PREFIX = "llama323b"

MINIO_ENDPOINT = "https://minio-api-minio.apps.etlai.lab.t-mobile.com"
ACCESS_KEY = "minio"
SECRET_KEY = "minio123"
BUCKET_NAME = "models"
#PREFIX = "phi35-mini-instruct"  # S3 path prefix inside bucket
#LOCAL_MODELS_DIR = "./models/phi35-mini-instruct"  # folder containing model files

#LOCAL_MODELS_DIR=["~/models/mistral7Binstructv03","~/models/mistralLargeInstruct2407","~/models/mistralNemoInstructFP82407","~/models/phi35MoEinstruct","~/models/phi4reasoning"]
LOCAL_MODELS_DIR=["~/models/mistralLargeInstruct2407"]
# Create S3 client
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name="us-east-1",  # MinIO defaults to this
    verify=False,
)


for lmd in LOCAL_MODELS_DIR:
 PREFIX = os.path.basename(lmd)
 #response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=PREFIX, MaxKeys=1)
 #if "Contents" not in response:
 # s3.put_object(Bucket=BUCKET_NAME, Key=PREFIX)
 # Walk through local models directory and upload files
 for root, _, files in os.walk(os.path.expanduser(lmd)): #LOCAL_MODELS_DIR):
   for filename in files:
        local_path = os.path.join(root, filename)

        # Compute S3 key with prefix, preserving relative folder structure
        relative_path = os.path.relpath(local_path, os.path.expanduser(lmd)) #LOCAL_MODELS_DIR)
        s3_key = f"{PREFIX}/{relative_path}"
#        print(relative_path)
        print(f"Uploading {local_path} -> s3://{BUCKET_NAME}/{s3_key}")
#        print(local_path)
#        print(BUCKET_NAME)
#        print(s3_key)
        s3.upload_file(local_path, BUCKET_NAME, s3_key)
        #break
   #break
