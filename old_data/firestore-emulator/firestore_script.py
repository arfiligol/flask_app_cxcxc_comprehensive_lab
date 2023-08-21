import json
import os
from google.cloud import firestore
from dotenv import load_dotenv
load_dotenv()


db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT")) # project 要與 firebase 運行時設定的一致，才可以在 UI 中正確的顯示 # 在 cloud shell 中運行，它會自動讀取 gcloud 的設定，無須額外做環境變數的設置


# # 創建一個新的文件
# doc_ref = db.collection('users').document('katelyn')
# doc_ref.set({
#     'first': 'katelyn',
#     'last': 'u',
#     'born': 1234
# })

# # 讀取所有文件
# docs_ref = db.collection('users')
# docs = docs_ref.stream()

# for doc in docs:
#     print(f'{doc.id} => {doc.to_dict()}')

with open("./users.json") as jsonFile:
    data = json.load(jsonFile)

for item in data:
    db.collection("users").add(item)