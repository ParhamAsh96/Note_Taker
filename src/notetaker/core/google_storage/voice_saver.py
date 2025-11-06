import os
from google.cloud import storage
from google.api_core.exceptions import NotFound, Conflict

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "src/notetaker/core/google_storage/storage_API.json"

PROJECT_ID = "notetaker-477400"
BUCKET_NAME = "voice-data-bucket-12345"
LOCATION = "EU"

storage_client = storage.Client(project=PROJECT_ID)

def get_or_create_bucket(name, location):
    try:
        bucket = storage_client.get_bucket(name)
        print(f"Bucket already exists. Location: {bucket.location}")
        return bucket
    
    except NotFound:
        pass


    try:
        bucket = storage_client.create_bucket(name, location=location)
        print(f"Created bucket: {bucket.name} in {bucket.location}")
        return bucket
    
    except Conflict:
        bucket = storage_client.get_bucket(name)
        print(f"Bucket exists after conflict. Location: {bucket.location}")
        return bucket

bucket = get_or_create_bucket(BUCKET_NAME, LOCATION)


def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
   
    except Exception as e:
        print(f"Upload failed: {e}")
        return False
    
file_path = r"src/notetaker/core/data/output.wav"
upload_to_bucket("lecture_voice", file_path, bucket)