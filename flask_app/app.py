"""
Flask 應用程式：上傳文件到 Google Cloud Storage

流程：
1. 載入必要的模組和函式庫。
2. 從 .env 文件中讀取環境變數。
3. 設定 Flask 應用和資料庫連接。
4. 定義資料庫模型。
5. 定義功能：將文件存儲到 Google Cloud Storage 和資料庫。
6. 定義 Flask 路由，處理文件上傳。
7. 啟動 Flask 應用。

"""


# 導入必要的函式庫和模組
# 從 .env 文件中載入環境變數
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
from google.cloud import storage
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


app = Flask(__name__)

# 設定資料庫連接
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_SCHEMA = os.getenv("DB_SCHEMA")
DB_TABLENAME = os.getenv("DB_TABLENAME")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_SCHEMA}'
db = SQLAlchemy(app)

# 定義資料庫模型
class File(db.Model):
    __tablename__ = os.getenv("DB_TABLENAME")
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), index=True)
    file_url = db.Column(db.String(255))

# 函數：將文件存儲到 Google Cloud Storage
def store_file_in_gcs(file):
    # 建立客戶端連接
    print("建立客戶端連接...")
    if (os.getenv("STORAGE_EMULATOR_HOST")):
        print("使用 AnonymousCredentials.")
        client = storage.Client(credentials=AnonymousCredentials(), project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    else:
        print("使用 real GCP user Account.")
        client = storage.Client()
    print("客戶端連接已建立。")

    # 取得存儲桶
    print("取得存儲桶 '{}'...".format(os.getenv("GCS_BUCKET_NAME")))
    bucket = client.get_bucket(os.getenv("GCS_BUCKET_NAME"))
    print("'{}' 已取得。".format(bucket))

    # 將文件保存到存儲桶
    print("將文件保存到 GCS...")
    blob = bucket.blob(file.filename)
    blob.upload_from_string(
        file.read(),
        content_type=file.content_type
    )
    print("文件已保存。")

    # 返回文件的公共 URL
    url = blob.public_url
    return url

# 函數：將文件資訊存儲到資料庫
def store_in_db(file_name, url):
    print("將文件存儲資訊保存到資料庫...")
    file = File(file_name=file_name, file_url=url)
    db.session.add(file)
    db.session.commit()
    print("資訊已保存。")

# Flask 路由：處理文件上傳
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
    <title>上傳新文件</title>
    <h1>上傳新文件</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=上傳>
    </form>
    '''

# 啟動 Flask 應用
if __name__ == '__main__':
    app.run(host=os.getenv("FLASK_RUN_HOST", "0.0.0.0"), port=int(os.getenv("FLASK_RUN_PORT", 8082)), debug=bool(os.getenv("FLASK_DEBUG", True)))
