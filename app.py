from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
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

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
