from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
import os
from dotenv import load_dotenv
load_dotenv()

"""
用來創建 gcs-emulator 的 bucket，請勿實際用於雲端
"""



# 指定 gcs-emulator host
gcs_emulator_host = "http://{}:{}".format(os.getenv("STORAGE_EMULATOR_HOST"), os.getenv("STORAGE_EMULATOR_PORT"))
os.environ["STORAGE_EMULATOR_HOST"] = gcs_emulator_host


print("establishing client...")
client = storage.Client(
    credentials=AnonymousCredentials(),
    project=os.getenv("GCP_PROJECT"),
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
    print("Error: {}".format(err.message))



