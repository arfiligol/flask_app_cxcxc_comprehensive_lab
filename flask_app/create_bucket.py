from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
import os
from dotenv import load_dotenv
load_dotenv()


# 指定 gcs-emulator host
gcs_emulator_host = "{}:{}".format(os.getenv("STORAGE_EMULATOR_HOST"), os.getenv("STORAGE_EMULATOR_PORT"))
os.environ["STORAGE_EMULATOR_HOST"] = gcs_emulator_host

print("establish client...")
project = os.getenv("GCP_PROJECT")
client = storage.Client(
    credentials=AnonymousCredentials(),
    project=project,
)

try:
# create bucket
    print("creating bucket '{}'...".format(os.getenv("GCS_BUCKET_NAME")))
    bucket = client.create_bucket(os.getenv("GCS_BUCKET_NAME"))
    print("'{}' created.".format(bucket))
except Exception as err:
    print("Error: {}".format(err.message))