from google.auth.credentials import AnonymousCredentials
from google.cloud import storage

import os

"""
無環境變數的 handle 沒有寫
有時間要補上
"""



# 指定 gcs-emulator host
os.environ["STORAGE_EMULATOR_HOST"] = os.getenv("STORAGE_EMULATOR_HOST")


client = storage.Client(
    credentials=AnonymousCredentials(),
    project="test",
)

# get bucket
bucket = client.get_bucket(os.getenv("GCS_BUCKET_NAME"))

# list all blobs and delete them
blobs = bucket.list_blobs()
for blob in blobs:
    blob.delete()

# delete bucket
bucket.delete()

