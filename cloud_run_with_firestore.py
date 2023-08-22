import json
import os
from google.cloud import firestore
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
import time
import json
import os

app = Flask(__name__)

db = firestore.Client() # project 要與 firebase 運行時設定的一致，才可以在 UI 中正確的顯示 # 這邊都僅使用預設 (google-cloud-firestore-emulator)


@app.route('/')
def index():
    # 模擬一些計算工作
    total = 0
    for i in range(10000):
        total += i

    # 模擬一些 I/O 等待
    time.sleep(0.01)

    # 讀取 users.json 的內容
    with open("./users.json") as jsonFile:
        data = json.load(jsonFile)

    # 寫入 users.json 到 db
    for item in data:
        db.collection("users").add(item)

    # 回傳寫入的資料
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv("PORT", 8080)))



