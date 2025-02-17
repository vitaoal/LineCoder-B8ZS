import socket

def main():
    host = "127.0.0.1"
    port = 65432

    # Cria e conecta o socket ao servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print("Conectado ao servidor.")

        # Aguarda por uma resposta (broadcast) do servidor
        client_socket.settimeout(10)  # Timeout de 10 segundos
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print("Recebido:", data.decode('utf-8'))
        except socket.timeout:
            print("Nenhum dado recebido dentro do tempo limite.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        client_socket.close()
        print("Conexão encerrada.")

if __name__ == "__main__":
    main()