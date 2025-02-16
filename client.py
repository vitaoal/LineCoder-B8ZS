from crypt_tools import *
import requests
import ast
from b8zse import B8ZSDecoder  # [b8zse.py](b8zse.py)
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
key, iv = load_keys()

@app.route('/')
def index():
    # Fazer uma pagina bonitinha pra exibir as msg
    return render_template('index_client.html')

# Testando a api do server.py
# A ideia é usar o script python apenas para decriptografar
# a mensagem que chega no front, usar SSE para interação em
# tempo real
@app.route('/decode', methods=['POST'])
def decode():
    data = request.get_json()
    encoded_message_str = data['message']  # Recebe a representação textual da lista
    # Converte a string para uma lista real de inteiros
    encoded_message = ast.literal_eval(encoded_message_str)
    
    # Decodifica o padrão B8ZS para recuperar a string binária original
    binary_str = B8ZSDecoder.decode(encoded_message)
    
    # Separa a string binária em bytes (8 bits) e converte para um objeto bytes
    encrypted_bytes = bytes(
        int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8)
    )
    
    # Descriptografa a mensagem
    decrypted_message = decrypt(encrypted_bytes, key, iv)
    
    return jsonify({'message': decrypted_message})

if __name__ == '__main__':
    app.run(debug=True, port=5001)