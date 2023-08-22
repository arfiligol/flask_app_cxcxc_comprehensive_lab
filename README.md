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

# Lab 2.1 - Cloud Run with Firestore (Emulator First)
## 設置 Firestore Emulator
1. 運行 Firebase Emulator
```
firebase emulators:start --only firestore
```