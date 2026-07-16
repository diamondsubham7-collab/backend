from flask import Flask, request, jsonify
from flask_cors import CORS
from predictor import get_prediction, handle_result, get_level, reset_level
import json
import os
import re
from PIL import Image
import pytesseract
import io

app = Flask(__name__)
CORS(app)

HISTORY_FILE = 'history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

@app.route('/')
def home():
    return "Wingo Predictor API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    game = data.get('game', '30S')
    period = data.get('period', '')
    result = get_prediction(game)
    result['period'] = period
    return jsonify(result)

@app.route('/result', methods=['POST'])
def result():
    data = request.get_json()
    period = data.get('period', '')
    prediction = data.get('prediction', '')
    is_win = data.get('win', False)
    
    handle_result(is_win)
    
    history = load_history()
    history.append({
        'period': period,
        'prediction': prediction,
        'result': 'Win' if is_win else 'Loss'
    })
    if len(history) > 50:
        history = history[-50:]
    save_history(history)
    
    try:
        next_period = str(int(period) + 1)
    except:
        next_period = period
    
    return jsonify({
        'status': 'ok',
        'level': get_level() + 1,
        'history': history,
        'next_period': next_period
    })

@app.route('/history', methods=['GET'])
def history():
    return jsonify(load_history())

@app.route('/reset', methods=['POST'])
def reset():
    reset_level()
    return jsonify({'status': 'reset done'})

@app.route('/level', methods=['GET'])
def level():
    return jsonify({'level': get_level() + 1})

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    img = Image.open(io.BytesIO(file.read()))
    
    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    text = pytesseract.image_to_string(img, config='--psm 6')
    period = re.sub(r'\D', '', text)
    
    if len(period) < 14:
        return jsonify({'error': 'Could not read period number'}), 400
    
    return jsonify({'period': period[:17]})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)