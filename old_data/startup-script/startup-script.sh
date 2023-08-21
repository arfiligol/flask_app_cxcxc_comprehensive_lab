
#!/bin/bash

# 更新系統套件列表
sudo apt-get update

# 安裝 Docker
sudo apt-get install -y docker.io

# 啟動 Docker 服務
sudo systemctl start docker
sudo systemctl enable docker

# 拉取 Docker 映像
sudo docker pull arfiligol/cxcxc-comprehensive-lab-app1-web
# 從 Metadata 伺服器讀取環境變數
METADATA_SERVER="http://metadata.google.internal/computeMetadata/v1/instance/attributes"

get_metadata_value() {
    curl -s -H "Metadata-Flavor: Google" "${METADATA_SERVER}/$1"
}

# 運行 Docker 容器並傳遞環境變數
sudo docker run -d --network=host \
-e IS_DEVELOPMENT="$(get_metadata_value IS_DEVELOPMENT)" \
-e DB_USERNAME="$(get_metadata_value DB_USERNAME)" \
-e DB_PASSWORD="$(get_metadata_value DB_PASSWORD)" \
-e DB_HOST="$(get_metadata_value DB_HOST)" \
-e DB_SCHEMA="$(get_metadata_value DB_SCHEMA)" \
-e GCS_BUCKET_NAME="$(get_metadata_value GCS_BUCKET_NAME)" \
-e FLASK_RUN_HOST="$(get_metadata_value FLASK_RUN_HOST)" \
-e FLASK_RUN_PORT="$(get_metadata_value FLASK_RUN_PORT)" \
-e FLASK_DEBUG="$(get_metadata_value FLASK_DEBUG)" \
arfiligol/cxcxc-comprehensive-lab-app1-web:1.0.0

# 下載 cloud-sql-proxy 
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy 

# 設置執行權限 
chmod +x cloud_sql_proxy 

# 從中繼資料讀取 INSTANCE_CONNECTION_NAME
INSTANCE_CONNECTION_NAME=$(get_metadata_value INSTANCE_CONNECTION_NAME) 

# 執行 cloud-sql-proxy 
./cloud_sql_proxy -instances=${INSTANCE_CONNECTION_NAME}=tcp:3306 --enable_iam_login &

# 安裝 stress 工具
sudo apt-get install -y stress

# 進行燒機動作
stress --cpu 1 --vm 1 --vm-bytes 1G --timeout 600s &

