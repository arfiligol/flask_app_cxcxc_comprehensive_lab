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


print("establishing client...")
client = storage.Client(
    credentials=AnonymousCredentials(),
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
)
print("client established.")

# get bucket
try:
    print("Getting bucket '{}'...".format(os.getenv("GCS_BUCKET_NAME")))
    bucket = client.get_bucket(os.getenv("GCS_BUCKET_NAME"))
    print("Bucket: '{}'".format(bucket))

    # list all blobs and delete them
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()

    # delete bucket
    bucket.delete()
    print("Bucket '{}' deleted".format(os.getenv("GCS_BUCKET_NAME")))

except Exception as err:
    print("Error: {}".format(err))



