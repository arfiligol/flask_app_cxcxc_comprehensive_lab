from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, exc
from sqlalchemy.orm import relationship
import json
import os
from dotenv import load_dotenv
load_dotenv()

# 建立 Flask App
app = Flask(__name__)

# 設定資料庫連接
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_SCHEMA = os.getenv("DB_SCHEMA")
DB_TABLENAME = os.getenv("DB_TABLENAME")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_SCHEMA}'
db = SQLAlchemy(app)

# 定義資料庫模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100), nullable=False)
    address = db.relationship('Address', backref='user', uselist=False)
    company = db.relationship('Company', backref='user', uselist=False)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(100), nullable=False)
    suite = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    geo = db.relationship('Geo', backref='address', uselist=False)

class Geo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.String(50), nullable=False)
    lng = db.Column(db.String(50), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    catchPhrase = db.Column(db.String(150), nullable=False)
    bs = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# 從 users.json 讀取並寫入資料庫
def insert_data_from_json():
    try:
        with open('users.json', 'r') as file:
            usersData = json.load(file)

        exist_user = []
        for data in usersData:
            if (User.query.get(data['id'])):
                exist_user.append(User.query.get(data['id']).name)
                continue
            print("Handling User: {}".format(data['name']))
            print()
            print("Debug: Phone number: {}".format(data['phone']))
            print()
            # User Table
            print("Creating user object...")
            user = User(
                id=data['id'],
                name=data['name'],
                username=data['username'],
                email=data['email'],
                phone=data['phone'],
                website=data['website'],
            )

            # Address Table
            print("Creating address object...")
            addressData = data['address']
            address = Address(
                id=data['id'],
                street=addressData['street'],
                suite=addressData['suite'],
                city=addressData['city'],
                zipcode=addressData['zipcode'],
                user_id=data['id']
            )

            # Geo Table
            print("Creating geo object...")
            geoData = addressData['geo']
            geo = Geo(
                id=data['id'],
                lat=geoData['lat'],
                lng=geoData['lng'],
                address_id=data['id']
            )

            # Company Table
            print("Creating company object...")
            companyData = data['company']
            company = Company(
                id=data['id'],
                name=companyData['name'],
                catchPhrase=companyData['catchPhrase'],
                bs=companyData['bs'],
                user_id=data['id']
            )
            
            print("Add user '{}' to db session!".format(data['name']))
            db.session.add(user)
            db.session.add(address)
            db.session.add(geo)
            db.session.add(company)

        print("Try insert data to db...")
        db.session.commit()
        print("Successful!")
        return {"message": "Successful import/update data!", "exist_user": exist_user}
    except Exception as err:
        print(err)
        return err
    


@app.route('/', methods=['GET'])
def import_users():
    result = insert_data_from_json()
    return jsonify({"message": str(result)}), 200

if __name__ == '__main__':
    with app.app_context():
        print("初始化 Table")
        db.create_all()  # 創建所有未存在的表格
    app.run(host=os.getenv("FLASK_RUN_HOST", "0.0.0.0"), port=os.getenv("PORT", 8080), debug=os.getenv("FLASK_RUN_DEBUG", True))