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
4. Push Artifact Registry
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
