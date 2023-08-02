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


"""
流程：
取得檔名
上傳檔案到 storage，回傳 檔案 url
將檔名、檔案 url 存到 cloud sql 去

"""

app = Flask(__name__)

# 資料庫 URI 資訊
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_SCHEMA = os.getenv("DB_SCHEMA")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_SCHEMA}'
db = SQLAlchemy(app)


# database model -> 有特別指定 table name（可件手動流程文件內的 table name）
class File(db.Model):
    global DB_SCHEMA
    __tablename__ = f"{DB_SCHEMA}"
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), index=True)
    file_url = db.Column(db.String(255))

def store_file_in_gcs(file):
    client = storage.Client()

    # 取得 bucket
    bucket = client.get_bucket(os.getenv("GCS_BUCKET_NAME")) 

    # 存檔案
    blob = bucket.blob(file.filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )

    # 取 url 回傳
    url = blob.public_url

    return url

def store_in_db(file_name, url):
    # 存檔名、檔案 url
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
