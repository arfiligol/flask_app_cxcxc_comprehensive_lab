# 使用 codercom/code-server 作為基礎映像檔
FROM linuxserver/code-server:4.16.1

# 安裝 gcloud-sdk
# 安裝必要的套件
RUN apt update && apt install -y curl gnupg2
# 添加 Google Cloud SDK 存儲庫
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
# 添加 Google Cloud 公鑰
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
# 更新存儲庫並安裝 google-cloud-sdk
RUN apt update -y
RUN apt install google-cloud-sdk -y
# 安裝 python 和 pip
RUN apt update && apt install -y python3 python3-pip

