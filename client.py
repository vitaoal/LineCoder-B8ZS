# python
from b8zse import B8ZSDecoder  # [b8zse.py](b8zse.py)
import socket
import threading
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor

chave_cesar = 3  # Chave para a Cifra de César

def decifra_cesar(mensagem_criptografada, chave):
    mensagem_original = ""
    for letra in mensagem_criptografada:
        if letra.isalpha():
            maiuscula = letra.isupper()
            letra = letra.lower()
            codigo_ascii = ord(letra)
            letra_original = chr(((codigo_ascii - ord('a') - chave) % 26) + ord('a'))
            if maiuscula:
                letra_original = letra_original.upper()
        else:
            letra_original = letra
        mensagem_original += letra_original
    return mensagem_original

class MainWindow(QWidget):
    new_message = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.decoder = B8ZSDecoder()
        self.client_socket = None
        self.initUI()
        self.new_message.connect(self.update_message)

    def initUI(self):
        grid_layout = QGridLayout()

        # Group 1: Decodificar Mensagem
        group1 = QGroupBox('')
        group1_layout = QVBoxLayout()
        group1_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.label = QLabel('Decodificar Mensagem:')
        self.label.setStyleSheet("font-weight: bold; color: gainsboro; border: none;")
        self.label_decoded = QLabel('Decoded Message')
        self.label_decoded.setStyleSheet("color: gainsboro;")
        self.text_input = QLineEdit()
        group1_layout.addWidget(self.label)
        group1_layout.addWidget(self.label_decoded)
        group1.setLayout(group1_layout)

        # Group 2: Conectar ao Servidor
        group2 = QGroupBox('Conectar ao Servidor')
        group2_layout = QVBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("IP do servidor")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Porta")
        self.connect_button = QPushButton("Conectar")
        self.connect_button.clicked.connect(self.connectToServer)
        self.server_msg_label = QLabel("Mensagens do servidor aparecerão aqui")
        group2_layout.addWidget(self.ip_input)
        group2_layout.addWidget(self.port_input)
        group2_layout.addWidget(self.connect_button)
        group2_layout.addWidget(self.server_msg_label)
        group2.setLayout(group2_layout)

        grid_layout.addWidget(group1, 0, 0)
        grid_layout.addWidget(group2, 0, 1)
        self.setLayout(grid_layout)

        # Estilo
        self.setStyleSheet("""
            color: gainsboro; background-color: #202020;
            border: 1px solid #565656; border-radius: 2px;
        """)

    def on_submit(self):
        coded_str = self.text_input.text()  
        coded_list = list(map(int, coded_str.split()))
        decoded_bin = self.decoder.decode(coded_list)
        print(f"Decoded binary: {decoded_bin}")

    def connectToServer(self):
        ip = self.ip_input.text().strip()
        port_str = self.port_input.text().strip()
        try:
            port = int(port_str)
        except ValueError:
            self.server_msg_label.setText("Porta inválida")
            return
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, port))
            self.server_msg_label.setText("Conectado ao servidor!")
            threading.Thread(target=self.listen_server, daemon=True).start()
        except Exception as e:
            self.server_msg_label.setText(f"Erro: {e}")

    def listen_server(self):
        buffer = ""
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            buffer += data.decode()
            # Processar todas as mensagens completas no buffer
            while '\n' in buffer:
                message, buffer = buffer.split('\n', 1)
                decoded_bin = self.decoder.decode(message)
                try:
                    # Converte de binário para texto (ASCII Estendido)
                    decrypted_message = ''.join(chr(int(decoded_bin[i:i+8], 2)) for i in range(0, len(decoded_bin), 8))
                    decrypted_message = decifra_cesar(decrypted_message, chave_cesar)
                    self.new_message.emit(decoded_bin)
                    self.label_decoded.setText(decrypted_message)
                except Exception as e:
                    print(f"Erro ao processar mensagem: {e}")

    def update_message(self, message):
        self.server_msg_label.setText(message)

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()