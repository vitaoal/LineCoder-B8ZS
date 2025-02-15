from crypt_tools import *
from b8zse import B8ZSEncoder
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
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

@app.route('/last_message', methods=['GET'])
def get_last_message():
    global last_message
    if last_message is None:
        return jsonify({'message': 'No message available'}), 404
    return jsonify({'last_message': last_message})

if __name__ == '__main__':
    app.run(debug=True, port=5000)