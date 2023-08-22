FROM ubuntu:22.04

# 設置工作目錄
WORKDIR /app

# 安裝 python 和 pip
RUN apt-get update && apt-get install -y python3 python3-pip

# 複製當前目錄的所有文件到容器的 /app 目錄
COPY . /app

# 安裝所需的 python 庫
RUN pip3 install -r requirements.txt

# 啟動 Flask 應用程序
CMD ["python3", "cloud_run_only.py"]
