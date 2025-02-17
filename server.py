import threading
import socket
from crypt_tools import *
from b8zse import B8ZSEncoder
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

host = "127.0.0.1"
port = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host,port))
clients = []
clients_lock = threading.Lock()

def broadcast(data):
    with clients_lock:
        for client in list(clients):
            try:
                client.sendall((data + '\n').encode())  # Adiciona delimitador
            except Exception as e:
                print(f"Erro ao enviar para o cliente: {e}")
                client.close()
                clients.remove(client)

def startServer():
    server_socket.listen(5)
    print(f"TCP Server iniciado em {host}:{port}")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address}")
        clients.append(client_socket)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.encoder = B8ZSEncoder()
        self.key, self.iv = load_keys()
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()

        # Create 4 group boxes
        group1 = QGroupBox('')
        group2 = QGroupBox('Group 2')

        # Group 1: add widgets
        group1_layout = QVBoxLayout()
        group1_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label = QLabel('Codificar Texto:')
        self.label.setStyleSheet("font-weight: bold; color: gainsboro; border: none;")

        self.text_input = QLineEdit()
        self.text_input.setStyleSheet("border: 1px solid #565656; border-radius: 2px;")

        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet("color: white; background-color: #3AACE5;")
        self.submit_button.setFixedWidth(int(self.width() * 0.2))
        self.submit_button.setFixedHeight(int(self.height() * 0.1))
        self.submit_button.clicked.connect(self.on_submit)
        
        group1_layout.addWidget(self.label)
        group1_layout.addWidget(self.text_input)
        group1_layout.addWidget(self.submit_button)

        # Exibir resultados
        self.encrypted_label = QLabel('Encrypted: ')
        self.encrypted_label.setWordWrap(True)
        self.binary_label = QLabel('Binary: ')
        self.binary_label.setWordWrap(True)
        self.coded_label = QLabel('Encoded Signal: ')
        self.coded_label.setWordWrap(True)
        group1_layout.addWidget(self.encrypted_label)
        group1_layout.addWidget(self.binary_label)
        group1_layout.addWidget(self.coded_label)

        group1.setLayout(group1_layout)

        # Add group boxes to the grid layout
        grid_layout.addWidget(group1, 0, 0)
        grid_layout.addWidget(group2, 1, 0)

        self.setLayout(grid_layout)
        self.setWindowTitle('B8ZS Encoder')
        #self.setFixedSize(400, 400)

        # Estilo
        self.setStyleSheet("""
            color: gainsboro; background-color: #202020;
            border: 1px solid #565656; border-radius: 2px;
        """)


    # Na função on_submit:
    def on_submit(self):
        text = self.text_input.text()

        # Encripta
        encrypted = encrypt(text, self.key, self.iv)

        # Binariza
        binary = ''.join(format(e, '08b') for e in encrypted)

        # Codifica
        coded = self.encoder.encode(binary)
        # Remova a linha redundante coded_str e envie diretamente
        broadcast(coded)  # coded já é a string com vírgulas
        # Atualize a UI conforme necessário
         # Display results in the interface
        self.encrypted_label.setText(f"Encrypted: {encrypted}")
        self.binary_label.setText(f"Binary: {binary}")
        self.coded_label.setText(f"Encoded Signal: {coded}")

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    threading.Thread(target=startServer, daemon=True).start()
    app.exec_()


if __name__ == "__main__":
    main()