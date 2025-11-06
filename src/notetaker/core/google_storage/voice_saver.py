import os
from google.cloud import storage
from google.api_core.exceptions import NotFound, Conflict

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "src/notetaker/core/google_storage/storage_API.json"

PROJECT_ID = "notetaker-477400"
BUCKET_NAME = "voice-data-bucket-12345"
LOCATION = "EU"

client = storage.Client(project=PROJECT_ID)

def get_or_create_bucket(name: str, location: str):
    try:
        bucket = client.get_bucket(name)
        print(f"Bucket already exists. Location: {bucket.location}")
        return bucket
    except NotFound:
        pass

    try:
        bucket = client.create_bucket(name, location=location)
        print(f"Created bucket: {bucket.name} in {bucket.location}")
        return bucket
    except Conflict:
        # Very rare race condition / retry case
        bucket = client.get_bucket(name)
        print(f"Bucket exists after conflict. Location: {bucket.location}")
        return bucket

bucket = get_or_create_bucket(BUCKET_NAME, LOCATION)

