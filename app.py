from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from util import allowed_file, process_video_async

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Manage CORS for SocketIO

# Apply CORS to Flask app
CORS(app, supports_credentials=True)  # Enable CORS for all routes, allowing credentials

UPLOAD_FOLDER = 'temp_vids'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        process_video_async(socketio, file_path)
        return jsonify({"message": "File successfully uploaded and processing started"}), 200

@socketio.on('connect', namespace='/video')
def test_connect():
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect', namespace='/video')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1',port=8080)