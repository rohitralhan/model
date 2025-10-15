import s3fs
import os
from botocore.config import Config

# Create an S3FileSystem object
# If you have AWS credentials configured (e.g., via environment variables or ~/.aws/credentials),
# s3fs will automatically use them. Otherwise, you might need to pass credentials explicitly.
fs = s3fs.S3FileSystem(
	key="14AOD5215XEMZS3WLJPZ",
	secret="9ipn0d3oc0h98_LPiY2XYS_v8uKCFP4A6476OAAE",
    	client_kwargs={"endpoint_url": "https://10.0.18.5:8443/", "verify": False} #, config_kwargs={"signature_version": "s3v4", "s3": {"payload_signing_enabled": False}}, # adjust region if needed
	)

# Specify the S3 bucket and an optional path within the bucket
bucket_name = "redhat-bucket1"
path_in_bucket = "" # Optional: to list files within a specific folder
#local_dir ="./model-files"


#for root, _, files in os.walk(local_dir):
#    for filename in files:
#        local_path = os.path.join(root, filename)

#        # Preserve folder structure in bucket
#        relative_path = os.path.relpath(local_path, local_dir)
#        remote_path = f"{bucket_name}" #f"{remote_prefix}/{relative_path}"

#        print(f"Uploading {local_path} -> {remote_path}")

        # Upload file
#        fs.put(local_path, remote_path)


# List files and directories at the specified path
# The `detail=True` argument returns a list of dictionaries with more information
# about each object (e.g., size, last modified time).
# The `recursive=True` argument lists all objects in subdirectories as well.
files_and_folders = fs.ls(f"s3://{bucket_name}/{path_in_bucket}", detail=True)


# Print the list of files and folders
for item in files_and_folders:
    print(item)
