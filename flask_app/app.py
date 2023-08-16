from google.auth.credentials import AnonymousCredentials
from google.cloud import storage
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
load_dotenv()



# python 讀取環境變數參考文件:https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5
# 仍然無法讀取，使用 python-dotenv 輔助讀取


app = Flask(__name__)

# 資料庫 URI 資訊
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_SCHEMA = os.getenv("DB_SCHEMA")
DB_TABLENAME = os.getenv("DB_TABLENAME")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_SCHEMA}'
db = SQLAlchemy(app)

class File(db.Model):
    global DB_TABLENAME
    __tablename__ = f"{DB_TABLENAME}" # 在這裡做指定的動作
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), index=True)
    file_url = db.Column(db.String(255))

def store_file_in_gcs(file):
    print("establishing client...")
    if (os.getenv("IS_DEVELOPMENT")):
        client = storage.Client(credentials=AnonymousCredentials(), project=os.getenv("GCP_PROJECT"))
    else:
        client = storage.Client(project=os.getenv("GCP_PROJECT"))
    print("client established.")

    # 取得 Bucket
    print("getting bucket '{}'".format(os.getenv("GCS_BUCKET_NAME")))
    bucket = client.get_bucket(os.getenv("GCS_BUCKET_NAME"))
    print("'{}' get.")

    # 存檔案到 bucket
    print("Saving file to gcs...")
    blob = bucket.blob(file.filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )
    print("file saved.")

    # 取 url 回傳
    url = blob.public_url

    return url

def store_in_db(file_name, url):
    # 存檔名、Public url 到 DB
    file = File(file_name=file_name, file_url=url)
    db.session.add(file)
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_name = file.filename
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
