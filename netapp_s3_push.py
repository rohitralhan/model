
import os
import boto3
from botocore.config import Config
import logging
logging.basicConfig(level=logging.DEBUG)

# NetApp S3 details
endpoint_url = "https://10.0.18.5:8443"   # replace with your endpoint
access_key   = ""
secret_key   = ""
bucket_name  = "redhat-bucket1"

# Directory to upload
local_dir = "./model-files"
remote_prefix = "llama323b"

# boto3 client with UNSIGNED-PAYLOAD
s3 = boto3.client(
    "s3",
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    verify=False,   # disable SSL verification for self-signed cert
    config=Config(
         request_checksum_calculation="when_required",
         response_checksum_validation="when_required",
         signature_version="s3v4",
         s3={"payload_signing_enabled": False}  # <-- forces UNSIGNED-PAYLOAD
    )
)

test_file_path = "./model-files/README.md"
remote_key_test = "llama323b/README.md"
with open(test_file_path, 'rb') as data:
    s3.put_object(
        Bucket=bucket_name,
        Key=remote_key_test,
        Body=data
    )
print("#######################################################################")
print(bucket_name, " ", remote_key_test, " " , data)
print("#######################################################################")
# Walk local directory and upload
for root, _, files in os.walk(local_dir):
    for filename in files:
        local_path = os.path.join(root, filename)

        # preserve folder structure
        relative_path = os.path.relpath(local_path, local_dir)
        remote_key = f"{remote_prefix}/{relative_path}"

        print(f"Uploading {local_path} -> s3://{bucket_name}/{remote_key}")
        print(local_path)
        print(bucket_name)
        print(remote_key)
        s3.upload_file(local_path, bucket_name, remote_key)
