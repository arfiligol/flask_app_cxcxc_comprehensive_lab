from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

"""
無環境變數的 handle 沒有寫
有時間要補上
"""


if (os.getenv("IS_DEVELOPMENT")):
    # 指定 gcs-emulator host
    os.environ["STORAGE_EMULATOR_HOST"] = os.getenv("STORAGE_EMULATOR_HOST") # 改成從環境變數讀取，而不是寫死

app = Flask(__name__)

# 資料庫 URI 資訊
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_SHCEMA = os.getenv("DB_SCHEMA")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_SCHEMA}'
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), index=True)
    file_url = db.Column(db.String(255))

def store_file_in_gcs(file):
    if (os.getenv("IS_DEVELOPMENT")):
        client = storage.Client(credentials=AnonymousCredentials(), project="cxcxc-comprehensive-lab")
    else:
        client = storage.Client()
    bucket = client.get_bucket(os.getenv("GCS_BUCKET_NAME"))

    blob = bucket.blob(file.filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )

    url = blob.public_url

    return url

def store_in_db(file_name, url):
    file = File(file_name=file_name, file_url=url)
    db.session.add(file)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_name = file.filename
            print(file_name)
            url = store_file_in_gcs(file)
            store_in_db(file_name, url)

            return redirect(url_for('upload_file', file_name=file_name))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(host=os.getenv("FLASK_RUN_HOST", "0.0.0.0"), port=int(os.getenv("FLASK_RUN_PORT", 8082)), debug=bool(os.getenv("FLASK_DEBUG", True)))
