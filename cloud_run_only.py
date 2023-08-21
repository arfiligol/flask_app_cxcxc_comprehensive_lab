from flask import Flask, jsonify
import time
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    # 模擬一些計算工作
    total = 0
    for i in range(10000):
        total += i

    # 模擬一些 I/O 等待
    time.sleep(0.01)

    # 回傳 users.json 的內容
    with open("users.json", "r") as file:
        data = json.load(file)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=(os.getenv("PORT"), 8080))
