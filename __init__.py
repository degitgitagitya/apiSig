from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime
from pandas import read_csv
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt
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
    satuan = db.Column(db.String(100))
    username = db.Column(db.String(100))
    harga = db.Column(db.Integer)

    def __init__(self, kode, nama, satuan, username, harga):
        self.kode = kode
        self.nama = nama
        self.satuan = satuan
        self.username = username
        self.harga = harga

# Barang Schema
class BarangSchema(ma.Schema):
    class Meta:
        fields = ('id', 'kode', 'nama', 'satuan', 'username', 'harga')

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
    satuan = request.json['satuan']
    username = request.json['username']
    harga = request.json['harga']
    new_barang = Barang(kode, nama, satuan, username, harga)
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
    satuan = request.json['satuan']
    username = request.json['username']
    harga = request.json['harga']

    barang.kode = kode
    barang.nama = nama
    barang.satuan = satuan
    barang.username = username
    barang.harga = harga
    
    db.session.commit()

    return barang_schema.jsonify(barang)

# Barang Batch Upload
@app.route('/barang/upload/<string:username>', methods=['POST'])
def upload_batch_barang(username):
    data = request.json['data']

    for i in data:
        new_barang = Barang(i['kode'], i['nama'], i['satuan'], username, i['harga'])
        db.session.add(new_barang)

    db.session.commit()

    all_barangs = Barang.query.filter_by(username=username)
    result = barangs_schema.dump(all_barangs)

    return jsonify(result)

# Delete All Barang
@app.route('/barang/delete-all/<string:username>', methods=['DELETE'])
def delete_all_barang(username):
    all_barang = Barang.query.filter_by(username=username)

    for i in all_barang:
        db.session.delete(i)

    db.session.commit()

    all_barangs = Barang.query.filter_by(username=username)
    result = barangs_schema.dump(all_barangs)

    return jsonify(result)

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
    cycle = db.Column(db.Integer)

    def __init__(self, username, nama, email, phone, store_name, store_category, store_address, url_photo, cycle):
        self.username = username
        self.nama = nama
        self.email = email
        self.phone = phone
        self.store_name = store_name
        self.store_category = store_category
        self.store_address = store_address
        self.url_photo = url_photo
        self.cycle = cycle

# Information Schema
class InformationSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'nama', 'email', 'phone', 'store_name', 'store_category', 'store_address', 'url_photo', 'cycle')

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
    cycle = request.json['cycle']
    new_information = Information(username, nama, email, phone, store_name, store_category, store_address, url_photo, cycle)
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
@app.route('/information/<string:username>', methods=['PUT'])
def update_information(username):
    information = Information.query.filter_by(username=username).first()

    nama = request.json['nama']
    email = request.json['email']
    phone = request.json['phone']
    store_name = request.json['store_name']
    store_category = request.json['store_category']
    store_address = request.json['store_address']
    url_photo = request.json['url_photo']
    cycle = request.json['cycle']

    information.nama = nama
    information.email = email
    information.phone = phone
    information.store_name = store_name
    information.store_category = store_category
    information.store_address = store_address
    information.url_photo = url_photo
    information.cycle = cycle

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

# Detail Barang Batch Upload
@app.route('/detail-barang/upload/<id>', methods=['POST'])
def detail_barang_upload(id):

    data = request.json['data']

    for i in data:
        new_detail_barang = DetailBarang(id, datetime.fromisoformat(i['tanggal']), i['quantity'])
        db.session.add(new_detail_barang)
    
    db.session.commit()

    all_detail_barang = DetailBarang.query.filter_by(id_barang=id)
    result = many_detail_barang_schema.dump(all_detail_barang)

    return jsonify(result)

# Delete All Detail Barang
@app.route('/detail-barang/delete-all/<id>', methods=['DELETE'])
def delete_all_detail_barang(id):
    all_detail_barang = DetailBarang.query.filter_by(id_barang=id)

    for i in all_detail_barang:
        db.session.delete(i)
    
    db.session.commit()

    all_detail_barang = DetailBarang.query.filter_by(id_barang=id)
    result = many_detail_barang_schema.dump(all_detail_barang)

    return jsonify(result)


# Prediksi Model
class Prediksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_barang = db.Column(db.Integer)
    quantity = db.Column(db.Float)

    def __init__(self, id_barang, quantity):
        self.id_barang = id_barang
        self.quantity = quantity


# Prediksi Schema
class PrediksiSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_barang', 'quantity')


# Init Prediksi Schema
prediksi_schema = PrediksiSchema()
many_prediksi_schema = PrediksiSchema(many=True)

# Get All Prediksi By id_barang
@app.route('/prediksi/<id>', methods=['GET'])
def get_all_prediksi_by_id_barang(id):
    all_prediksi = Prediksi.query.filter_by(id_barang=id)
    result = many_prediksi_schema.dump(all_prediksi)

    return jsonify(result)

# Prediksi
@app.route('/prediksi-all/<string:username>', methods=['POST'])
def prediksi_all(username):
    all_barangs = Barang.query.filter_by(username=username)
    result = barangs_schema.dump(all_barangs)
    
    listOfListData = []

    for i in result:
        listData = []
        many_detail_barang = DetailBarang.query.filter_by(id_barang=i['id'])
        all_prediksi = Prediksi.query.filter_by(id_barang=i['id'])
        for z in all_prediksi:
            db.session.delete(z)
        data = many_detail_barang_schema.dump(many_detail_barang)
        for j in data:
            listData.append(j['quantity'])
        listOfListData.append(listData)

    db.session.commit()

    final_prediction = []

    information = Information.query.filter_by(username=username).first()
    information_result = information_schema.dump(information)

    for row in listOfListData:
        train, test = row[1:len(row)-information_result['cycle']], row[len(row)-information_result['cycle']:]

        # train autoregression
        model = AutoReg(train, lags=10)
        model_fit = model.fit()
        # make predictions
        predictions_one = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
        rmse_one = sqrt(mean_squared_error(test, predictions_one))
        
        # train autoregression
        window = 10
        model = AutoReg(train, lags=10)
        model_fit = model.fit()
        coef = model_fit.params
        # walk forward over time steps in test
        history = train[len(train)-window:]
        history = [history[i] for i in range(len(history))]
        predictions_two = list()
        for t in range(len(test)):
            length = len(history)
            lag = [history[i] for i in range(length-window,length)]
            yhat = coef[0]
            for d in range(window):
                yhat += coef[d+1] * lag[window-d-1]
            obs = test[t]
            predictions_two.append(yhat)
            history.append(obs)
        rmse_two = sqrt(mean_squared_error(test, predictions_two))

        if (rmse_one < rmse_two):
            final_prediction.append(predictions_two)
        else:
            final_prediction.append(predictions_one)

    index = 0

    for i in result:
        for y in final_prediction[index]:
            new_prediksi = Prediksi(i['id'], y)
            db.session.add(new_prediksi)
        index = index + 1

    db.session.commit()

    return "ok"


# Download Contoh File Detail
@app.route('/file/detail')
def get_file_detail():
	return send_file('data.csv', as_attachment=True)

# Download Contoh File Detail
@app.route('/file/barang')
def get_file_barang():
	return send_file('data2.csv', as_attachment=True)

def getApp():
    return app

# Run Server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)