from dotenv import load_dotenv
load_dotenv()
import os
if (os.getenv("GOOGLE_APPLICATION_CREDENTIALS")):
    print("Use real credential.")
    from google.oauth2.service_account import Credentials
else:
    print("Use AnonymousCredential.")
    from google.auth.credentials import AnonymousCredentials
from google.cloud import storage



# 指定 gcs-emulator host
if (os.getenv("STORAGE_EMULATOR_HOST")):
    print("Using gcs-emulator")
    print("Using AnonymousCredential.")
    client = storage.Client(
        credentials=AnonymousCredentials(),
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    )
else:
    print("Using Real Cloud Storage.")
    print("Using Real account credential.")
    client = storage.Client()

try:
    # List the Buckets
    for bucket in client.list_buckets():
        print(f"Bucket: {bucket.name}\n")

        # List the Blobs in each Bucket
        for blob in bucket.list_blobs():
            print(f"Blob: {blob.name}")
except Exception as err:
    print("Error: {}".format(err))