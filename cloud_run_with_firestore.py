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
    print("Emulating some calculation work...")
    total = 0
    for i in range(10000):
        total += i

    # 模擬一些 I/O 等待
    print("Emualting some waiting job...")
    time.sleep(0.01)

    # 讀取 users.json 的內容
    print("reading user.json")
    with open("./users.json") as jsonFile:
        data = json.load(jsonFile)

    # 寫入 users.json 到 db
    print("Importing/Updating data to firestore db...")
    for item in data:
        print("Insert/Update {}!".format(str(item["id"])))
        db.collection("users").document(str(item["id"])).set(item)

    # 回傳寫入的資料
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv("PORT", 8081)))