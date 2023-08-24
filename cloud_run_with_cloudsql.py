from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, exc
from sqlalchemy.orm import relationship, declarative_base
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
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    phone = Column(String)
    website = Column(String)

    address_id = Column(Integer, ForeignKey('address.id'))
    address = relationship("Address", back_populates="user")

    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship("Company", back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    street = Column(String)
    suite = Column(String)
    city = Column(String)
    zipcode = Column(String)

    geo_id = Column(Integer, ForeignKey('geo.id'))
    geo = relationship("Geo", back_populates="address")

    user = relationship("User", back_populates="address")


class Geo(Base):
    __tablename__ = "geo"

    id = Column(Integer, primary_key=True)
    lat = Column(String)
    lng = Column(String)

    address = relationship("Address", back_populates="geo")


class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    catchPhrase = Column(String)
    bs = Column(String)

    user = relationship("User", back_populates="company")

def load_users_from_file():
    with open('users.json', 'r') as file:
        users_data = json.load(file)
        return users_data

@app.route('/import_users', methods=['POST'])
def import_users():
    users_data = load_users_from_file()

    for data in users_data:
        user_id = data['id']
        user = User.query.get(user_id)

        if user:
            # 更新現有用戶資料
            for key, value in data.items():
                setattr(user, key, value)
        else:
            # 創建新用戶
            user = User(**data)
            db.session.add(user)

    try:
        db.session.commit()
        return jsonify({"message": "Users imported/updated successfully!"}), 200
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 創建所有未存在的表格
    app.run(debug=True)