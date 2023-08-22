# Lab 1 - Cloud Run Only
## Cloud Run Serivce 部屬
### Create Docker Image
1. 透過 Cloud Shell Link 建置環境
2. 複製 users.json 到當前目錄
```
cp /tmp/users.json ./users.json
```
3. Build Docker Image
```
docker build -t cloud-run-demo-ili .
```
### Push to Artifact Registry
4. 先在 Cloud shell 設置 docker 客戶端，讓 docker 客戶端正確的認證 google cloud 服務
```
gcloud auth configure-docker asia-east1-docker.pkg.dev
```
5. 前往 Artifact Registry 創建 Repository
6. 回到 Cloud Shell，對 image 貼標
```
docker tag cloud-run-demo-<YOUR_NAME> asia-east1-docker.pkg.dev/<PROJECT_ID>/<ARTIFACT_REGISTRY>/cloud-run-demo-<YOUR_NAME>:1.0.0
```
7. Push Image 到 Artifact Registry
```
docker push asia-east1-docker.pkg.dev/<PROJECT_ID>/<ARTIFACT_REGISTRY>/cloud-run-demo-<YOUR_NAME>:1.0.0
```

### 透過 Artifact Registry 部屬 Cloud Run Service
1. 前往 Cloud Run
2. 點即「新增服務」
3. 選擇 push 到 Artifact Registry 的 Image
4. 選擇地區
5. 選擇 Unauthorized
6. 建立

# Lab 2 - Cloud Run with Firestore
## 2-1 先嘗試 Firestore Emulator
### 啟動 Firestore Emulator
1. 運行 Firebase Emulator
```
firebase emulators:start --only firestore
```
### 運行 flask app 操作 Firestore
1. 開 new Terminal，進入 git repo 資料夾
```
cd cloudshell_open/flask_app_cxcxc_comprehensive_lab/
```
2. 安裝必要套件 
```
pip3 install -r requirements.txt
```
3. (optional) 從 /tmp 複製 users.json 到當前資料夾
```
cp /tmp/users.json ./users.json
```
4. 執行 flask app
```
python3 cloud_run_with_firestore.py
```
5. 透過 cloud shell preview 功能閱覽，確定有回傳 users.json 內容

## 2-2 部屬 Flask App 到 Cloud Run 並存取 Firestore
### Build and Push Image
1. 修改 .env 的內容 -> 註解掉所有環境變數
2. 修改 Dockerfile 的內容
```
CMD ["python3", "cloud_run_only.py"] --> CMD ["python3", "cloud_run_with_firestore.py"]
```
3. Build Docker Image
```
docker build -t cloud-run-with-firestore-demo-<YOUR_NAME> .
```
4. Tag Docker Image
```
docker tag cloud-run-with-firestore-demo-<YOUR_NAME> asia-east1-docker.pkg.dev/<PROJECT_ID>/cloud-run-demo-<YOUR_NAME>/cloud-run-with-firestore-demo-<YOUR_NAME>:1.0.0
```
5. (optional) 先在 Cloud shell 設置 docker 客戶端，讓 docker 客戶端正確的認證 google cloud 服務
```
gcloud auth configure-docker asia-east1-docker.pkg.dev
```
6. Push Image
```
docker push asia-east1-docker.pkg.dev/<YOUR_PROJECT_ID>/cloud-run-demo-<YOUR_NAME>/cloud-run-with-firestore-demo-<YOUR_NAME>:1.0.0
```

### 部屬 Cloud Run Service
1. 前往