import boto3
s3 = boto3.resource('s3')
from pathlib import Path
import os
import zipfile
from shared.util import makeparents

bucket_uri = "ecommerce-parquet"
s3_file = "olist.zip"
local_path = "tempdata"


def download_default_s3(bucket_uri=bucket_uri, s3_file=s3_file, local_path=local_path):
    temp_path = f"tmp/{s3_file}"
    makeparents(local_path)
    makeparents(temp_path)
    
    s3.Bucket(bucket_uri).download_file(
        s3_file, temp_path
    )
   
    with zipfile.ZipFile(temp_path, 'r') as zip_ref:
        zip_ref.extractall(local_path)
    
    os.remove(temp_path)
    
if __name__ == "__main__":
    download_default_s3()

    