from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Init cors
CORS(app)

# User Model ===============================================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    token = db.Column(db.String(100))

    def __init__(self, username, password, token):
        self.username = username
        self.password = password
        self.token = token

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'token')

# Init Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Get all User
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)

# Create a User
@app.route('/user', methods=['POST'])
def add_user():
    username = request.json['username']
    password = request.json['password']
    new_user = User(username, password, "token")
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# Get by Username
@app.route('/user/<string:username>', methods=['GET'])
def get_user(username):
    user = User.query.filter_by(username=username).first()

    return user_schema.jsonify(user)

@app.route('/auth/<string:username>/<string:password>', methods=['GET'])
def auth(username, password):
    user = User.query.filter_by(username=username, password=password).first()

    return user_schema.jsonify(user)

# Barang Model =============================================== 
class Barang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(100), unique=True)
    nama = db.Column(db.String(100))
    lokasi = db.Column(db.String(100))
    username = db.Column(db.String(100))

    def __init__(self, kode, nama, lokasi, username):
        self.kode = kode
        self.nama = nama
        self.lokasi = lokasi
        self.username = username

# Barang Schema
class BarangSchema(ma.Schema):
    class Meta:
        fields = ('id', 'kode', 'nama', 'lokasi', 'username')

# Init Barang Schema
barang_schema = BarangSchema()
barangs_schema = BarangSchema(many=True)

# Get all Barang
@app.route('/barangs/<string:username>', methods=['GET'])
def get_barangs(username):
    all_barangs = Barang.query.filter_by(username=username)
    result = barangs_schema.dump(all_barangs)

    return jsonify(result)

# Create barang
@app.route('/barang', methods=['POST'])
def add_barang():
    kode = request.json['kode']
    nama = request.json['nama']
    lokasi = request.json['lokasi']
    username = request.json['username']
    new_barang = Barang(kode, nama, lokasi, username)
    db.session.add(new_barang)
    db.session.commit()

    return barang_schema.jsonify(new_barang)

# Delete barang
@app.route('/barang/<id>', methods=['DELETE'])
def delete_barang(id):
    barang = Barang.query.get(id)
    db.session.delete(barang)
    db.session.commit()

    return barang_schema.jsonify(barang)

# Edit Barang
@app.route('/barang/<id>', methods=['PUT'])
def update_barang(id):
    barang = Barang.query.get(id)

    kode = request.json['kode']
    nama = request.json['nama']
    lokasi = request.json['lokasi']
    username = request.json['username']

    barang.kode = kode
    barang.nama = nama
    barang.lokasi = lokasi
    barang.username = username
    
    db.session.commit()

    return barang_schema.jsonify(barang)

# Information Model ===================================================
class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, unique=True)
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    store_name = db.Column(db.String(100))
    store_category = db.Column(db.String(100))
    store_address = db.Column(db.String(100))
    url_photo = db.Column(db.String(300))

    def __init__(self, username, nama, email, phone, store_name, store_category, store_address, url_photo):
        self.username = username
        self.nama = nama
        self.email = email
        self.phone = phone
        self.store_name = store_name
        self.store_category = store_category
        self.store_address = store_address
        self.url_photo = url_photo

# Information Schema
class InformationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'nama', 'email', 'phone', 'store_name', 'store_category', 'store_address', 'url_photo')

# Init Information Schema
information_schema = InformationSchema()
informations_schema = InformationSchema(many=True)

@app.route('/informations', methods=['GET'])
def get_informations():
    all_informations = Information.query.all()
    result = informations_schema.dump(all_informations)

    return jsonify(result)

# Get Information By User 
@app.route('/information/<string:username>', methods=['GET'])
def get_information(username):
    information = Information.query.filter_by(username=username).first()
    return information_schema.jsonify(information)

# Create Information
@app.route('/information', methods=['POST'])
def add_information():
    username = request.json['username']
    nama = request.json['nama']
    email = request.json['email']
    phone = request.json['phone']
    store_name = request.json['store_name']
    store_category = request.json['store_category']
    store_address = request.json['store_address']
    url_photo = request.json['url_photo']
    new_information = Information(username, nama, email, phone, store_name, store_category, store_address, url_photo)
    db.session.add(new_information)
    db.session.commit()

    return information_schema.jsonify(new_information)

# Delete Information
@app.route('/information/<id>', methods=['DELETE'])
def delete_information(id):
    information = Information.query.get(id)
    db.session.delete(information)
    db.session.commit()

    return information_schema.jsonify(information)

# Edit Information
@app.route('/information/<id>', methods=['PUT'])
def update_information(id):
    information = Information.query.get(id)

    nama = request.json['nama']
    email = request.json['email']
    phone = request.json['phone']
    store_name = request.json['store_name']
    store_category = request.json['store_category']
    store_address = request.json['store_address']
    url_photo = request.json['url_photo']

    information.nama = nama
    information.email = email
    information.phone = phone
    information.store_name = store_name
    information.store_category = store_category
    information.store_address = store_address
    information.url_photo = url_photo

    db.session.commit()

    return information_schema.jsonify(information)


# Detail Barang Model
class DetailBarang(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_barang = db.Column(db.Integer)
    tanggal = db.Column(db.DateTime)
    quantity = db.Column(db.Integer)

    def __init__(self, id_barang, tanggal, quantity):
        self.id_barang = id_barang
        self.tanggal = tanggal
        self.quantity = quantity


# Detail Barang Schema
class DetailBarangSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_barang', 'tanggal', 'quantity')

# Init Detail Barang Schema
detail_barang_schema = DetailBarangSchema()
many_detail_barang_schema = DetailBarangSchema(many=True)

# Get All Detail Barang by id_barang
@app.route('/detail-barang/<id_barang>', methods=['GET'])
def get_all_detail_barang(id_barang):
    all_detail_barang = DetailBarang.query.filter_by(id_barang=id_barang)
    result = many_detail_barang_schema.dump(all_detail_barang)

    return jsonify(result)


# Create Detail Barang
@app.route('/detail-barang', methods=['POST'])
def add_detail_barang():
    id_barang = request.json['id_barang']
    tanggal = datetime.fromisoformat(request.json['tanggal'])
    quantity = request.json['quantity']

    new_detail_barang = DetailBarang(id_barang, tanggal, quantity)
    db.session.add(new_detail_barang)
    db.session.commit()
    
    return detail_barang_schema.jsonify(new_detail_barang)

# Delete Detail Barang
@app.route('/detail-barang/<id>', methods=['DELETE'])
def delete_detail_barang(id):
    detail_barang = DetailBarang.query.get(id)
    db.session.delete(detail_barang)
    db.session.commit()

    return detail_barang_schema.jsonify(detail_barang)

# Edit Barang
@app.route('/detail-barang/<id>', methods=['PUT'])
def edit_detail_barang(id):
    detail_barang = DetailBarang.query.get(id)
    
    detail_barang.id_barang = request.json['id_barang']
    detail_barang.tanggal = datetime.fromisoformat(request.json['tanggal'])
    detail_barang.quantity = request.json['quantity']

    db.session.commit()

    return detail_barang_schema.jsonify(detail_barang)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
