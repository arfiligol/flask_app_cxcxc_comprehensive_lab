# 使用 Node.js 基礎映像，因為 Firebase CLI 需要 Node.js
FROM node:16

# 安裝 Firebase CLI
RUN npm install -g firebase-tools

# 安裝 Python 和 pip
RUN apt-get update && apt-get install -y openjdk-11-jre python3 python3-pip

# 設定工作目錄
WORKDIR /usr/src/app

# 複製 Python 腳本到容器
COPY firestore_script.py .

# 啟動 Firestore Emulator
CMD firebase emulators:start --project ili-demo-test --only firestore
