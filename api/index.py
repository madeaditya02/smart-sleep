from flask import Flask, jsonify, request
from fuzzy_logic.fuzzy_sleep_quality import FuzzyKualitasTidur

app = Flask(__name__)
fuzzy = FuzzyKualitasTidur()

@app.route('/')
def home():
    return jsonify({'message': 'Server Flask berhasil dijalankan'}), 200

@app.route('/sleep', methods=['POST'])
def sleep():
    data = request.get_json()

    if 'detak_jantung' not in data:
        return jsonify({'error': 'Field "detak_jantung" diperlukan'}), 400

    try:
        bpm = float(data['detak_jantung'])
    except ValueError:
        return jsonify({'error': 'Nilai detak_jantung harus numerik'}), 400

    if bpm < 40 or bpm > 120:
        return jsonify({'warning': 'Nilai detak_jantung di luar jangkauan fuzzy (40–120 bpm)'}), 400

    hasil = fuzzy.analisis(bpm)

    return jsonify({
        'detak_jantung': bpm,
        **hasil
    }), 200