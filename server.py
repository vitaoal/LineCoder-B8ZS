from crypt_tools import *
from b8zse import B8ZSEncoder
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)
encoder = B8ZSEncoder()
key, iv = load_keys()

last_message = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    global last_message
    data = request.json.get('data')
    response = {'message': 'Data received', 'data': data}

    # Criptografia
    encrypted = encrypt(data, key, iv)

    # Binarização
    binary = ''.join(format(byte, '08b') for byte in encrypted)
    response['binary_data'] = binary

    # Codificação
    encoded_data = encoder.encode(binary)

    last_message = encoded_data
    return jsonify(response)

# Endpoint SSE
@app.route('/last_message', methods=['GET'])
def get_last_message():
    def stream():
        global last_message
        while True:
            if last_message is not None:
                yield f"data: {last_message}\n\n"
            else:
                yield f"data: No new message"
            time.sleep(1)
                
    return Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, port=5000)