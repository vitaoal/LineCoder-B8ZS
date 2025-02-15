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
                    # Insere a violação de polaridade
                    if self.last_polarity == 1:
                        encoded += [1, 0, 0, 0, -1, 0, -1, 1]
                    else:
                        encoded += [-1, 0, 0, 0, 1, 0, 1, -1]
                    zero_count = 0
                    self.last_polarity *= -1
        return encoded

class B8ZSDecoder:
    @staticmethod
    def decode(encoded_sequence):
        decoded = []
        i = 0
        
        while i < len(encoded_sequence):
            if encoded_sequence[i] == 0:
                # Contar zeros consecutivos
                zeros = 0
                while i < len(encoded_sequence) and encoded_sequence[i] == 0:
                    zeros += 1
                    i += 1
                decoded.extend(['0'] * zeros)
            else:
                # Verificar padrão de violação (8 elementos)
                if i + 7 < len(encoded_sequence):
                    subsequence = encoded_sequence[i:i+8]
                    # Padrões válidos de substituição
                    if subsequence in [
                        [1, 0, 0, 0, -1, 0, -1, 1],
                        [-1, 0, 0, 0, 1, 0, 1, -1]
                    ]:
                        decoded.extend(['0'] * 8)
                        i += 8
                        continue
                # Bit normal (1)
                decoded.append('1')
                i += 1
                
        return ''.join(decoded)