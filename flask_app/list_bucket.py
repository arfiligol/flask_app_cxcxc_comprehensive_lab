from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
import os
from dotenv import load_dotenv
load_dotenv()


# 指定 gcs-emulator host
if (os.getenv("STORAGE_EMULATOR_HOST")):
    print("Using gcs-emulator")


client = storage.Client(
    credentials=AnonymousCredentials(),
    project=os.getenv("GCP_PROJECT"),
)

try:
    # List the Buckets
    for bucket in client.list_buckets():
        print(f"Bucket: {bucket.name}\n")

        # List the Blobs in each Bucket
        for blob in bucket.list_blobs():
            print(f"Blob: {blob.name}")
except Exception as err:
    print("Error: {}".format(err.message))