from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Server Flask berhasil dijalankan'}), 200

@app.route('/about')
def about():
    return 'About'