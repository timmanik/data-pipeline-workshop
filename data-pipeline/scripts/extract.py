import boto3
from botocore.config import Config
from botocore import UNSIGNED
import os

def extract_noaa_gsod_data(year, month, output_dir='/data'):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    bucket_name = 'noaa-gsod-pds'
    prefix = f'{year}/{str(month).zfill(2)}'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # List objects in the bucket for the specified month
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    if 'Contents' not in response:
        print(f"No files found for {prefix}")
        return

    for obj in response['Contents']:
        key = obj['Key']
        local_path = os.path.join(output_dir, os.path.basename(key))
        
        # Download the file
        s3.download_file(bucket_name, key, local_path)
        print(f'Downloaded {key} to {local_path}')

if __name__ == '__main__':
    extract_noaa_gsod_data(2020, 1)