class B8ZSEncoder:
    def __init__(self):
        self.last_polarity = 1  # 1 para positivo, -1 para negativo

    def encode(self, binary_str):
        encoded = []
        zero_count = 0

        for bit in binary_str:
            if bit == '1':
                self.last_polarity *= -1
                encoded.append(self.last_polarity)
                zero_count = 0
            else:
                zero_count += 1
                encoded.append(0)
                if zero_count == 8:
                    encoded = encoded[:-8]  # Remove os 8 zeros
                    # Insere o padrão de substituição CORRETO
                    if self.last_polarity == 1:
                        encoded += [0, 0, 0, 1, -1, 0, -1, 1]
                    else:
                        encoded += [0, 0, 0, -1, 1, 0, 1, -1]
                    zero_count = 0
                    self.last_polarity *= -1  # Atualiza a polaridade
        return ','.join(map(str, encoded))

class B8ZSDecoder:
    @staticmethod
    def decode(encoded_sequence_str):
        encoded_sequence = list(map(int, encoded_sequence_str.split(',')))
        decoded = []
        i = 0
        n = len(encoded_sequence)
        
        substitution_patterns = [
            [0, 0, 0, 1, -1, 0, -1, 1],
            [0, 0, 0, -1, 1, 0, 1, -1]
        ]
        
        while i < n:
            # Verifica se há espaço para um padrão de substituição (8 elementos)
            if i + 8 <= n:
                current_subseq = encoded_sequence[i:i+8]
                if current_subseq in substitution_patterns:
                    decoded.extend(['0'] * 8)
                    i += 8
                    continue
            # Processa elementos individualmente
            if encoded_sequence[i] == 0:
                decoded.append('0')
            else:
                decoded.append('1')
            i += 1
        return ''.join(decoded)
    
def main():
    encoder = B8ZSEncoder()
    decoder = B8ZSDecoder()

    # Lista de testes com as strings a serem codificadas e decodificadas
    test_cases = ["Lorem", "Ipsum", "sin dolor"]

    for case in test_cases:
        print("Entrada:", case)
        # Converter cada caractere para uma string binária de 8 bits
        binary_str = ''.join(format(ord(c), '08b') for c in case)
        print("Binário:", binary_str)
        encoded = encoder.encode(binary_str)
        print("Codificado:", encoded)
        decoded_binary = decoder.decode(encoded)
        # Converter a string binária de volta para texto (cada 8 bits)
        decoded_text = ''.join(chr(int(decoded_binary[i:i+8], 2)) for i in range(0, len(decoded_binary), 8))
        print("Decodificado:", decoded_text)
        print()
    
    # Teste com 8 zeros (binário: 00000000)
    encoder = B8ZSEncoder()
    binary_str = "00000000"
    encoded = encoder.encode(binary_str)
    print("Encoded:", encoded)  # Deve retornar: 0,0,0,1,-1,0,-1,1 (polaridade inicial +1)

    decoded = B8ZSDecoder.decode(encoded)
    print("Decoded:", decoded)  # Deve retornar: 00000000

if __name__ == "__main__":
    main()