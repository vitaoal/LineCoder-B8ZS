import threading
import socket
from b8zse import B8ZSEncoder
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


host = socket.gethostbyname(socket.gethostname())
port = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
clients = []
clients_lock = threading.Lock()

chave_cesar = 3  # Chave para a Cifra de César

def cifra_cesar(mensagem, chave):
    mensagem_criptografada = ""
    for letra in mensagem:
        if letra.isalpha():
            maiuscula = letra.isupper()
            letra = letra.lower()
            codigo_ascii = ord(letra)
            letra_criptografada = chr(((codigo_ascii - ord('a') + chave) % 26) + ord('a'))
            if maiuscula:
                letra_criptografada = letra_criptografada.upper()
        else:
            letra_criptografada = letra
        mensagem_criptografada += letra_criptografada
    return mensagem_criptografada

def broadcast(data):
    with clients_lock:
        for client in list(clients):
            try:
                client.sendall((data + '\n').encode())
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

        # Grupo 2: Exibir gráfico dos sinais
        group2 = QGroupBox('Gráfico dos Sinais (Binário)')
        group2_layout = QVBoxLayout()
        self.fig = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.fig)
        group2_layout.addWidget(self.canvas)
        group2.setLayout(group2_layout)

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
        encrypted = cifra_cesar(text, chave_cesar)

        # Binariza
        binary = ''.join(format(ord(c), '08b') for c in encrypted)

        # Codifica
        coded = self.encoder.encode(binary)
        broadcast(coded)  # coded já é a string com vírgulas
        
        # Atualize a UI conforme necessário
        # Display results in the interface
        self.encrypted_label.setText(f"Criptografado (César): {encrypted}")
        self.binary_label.setText(f"Binário: {binary}")
        self.coded_label.setText(f"Codificado (B8ZS): {coded}")

        # Gera os dados para o gráfico.
        # Mensagem não decodificada: a representação binária ("binary")
        binary_nd = [int(bit) for bit in binary]
        
        # Tenta converter o sinal codificado (B8ZS) em uma lista de bits.
        # Supondo que "coded" seja uma string com dígitos separados por vírgula.
        try:
            binary_coded = [int(bit.strip()) for bit in coded.split(',')]
        except Exception:
            binary_coded = []
        
        # Atualiza o gráfico no grupo 2
        self.fig.clf()  # Limpa a figura

        ax1 = self.fig.add_subplot(211)
        ax1.stem(range(len(binary_nd)), binary_nd, linefmt='b-', markerfmt='bo', basefmt=" ")
        ax1.set_title("Mensagem Não Decodificada (Binário)")
        ax1.set_ylim(-0.5, 1.5)
        ax1.set_ylabel("Bit")
        
        ax2 = self.fig.add_subplot(212)
        ax2.stem(range(len(binary_coded)), binary_coded, linefmt='r-', markerfmt='ro', basefmt=" ")
        ax2.set_title("Sinal Codificado (B8ZS)")
        ax2.set_ylim(-0.5, 1.5)
        ax2.set_xlabel("Índice")
        ax2.set_ylabel("Bit")

        self.canvas.draw()
        

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    threading.Thread(target=startServer, daemon=True).start()
    app.exec_()

if __name__ == "__main__":
    main()