from crypt_tools import *
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Fazer uma pagina bonitinha pra exibir as msg
    return render_template('index.html')

# Testando a api do server.py
# A ideia é usar o script python apenas para decriptografar
# a mensagem que chega no front, usar webhook para interação
# em tempo real.
@app.route('/last_message', methods=['GET'])
def last_message():
    response = requests.get('http://localhost:5000/last_message')
    data = response.json()
    return data

if __name__ == '__main__':
    app.run(debug=True, port=5001)