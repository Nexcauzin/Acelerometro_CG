# Função para criar o Buffer Circular
def criar_buffer():
    return [None, None]

def adicionar_valor(buffer, valor):
    buffer[1], buffer[0] = buffer[0], valor

def obter_pares(buffer):
    return [(buffer[i], buffer[i+1]) for i in range(len(buffer)-1) if buffer[i] is not None and buffer[i+1] is not None]

buffer = criar_buffer()
buffer_ROL = criar_buffer()

for i in range(0, 10):
    adicionar_valor(buffer, i+1)
    buffer_pares = obter_pares(buffer)
    if buffer_pares:  # Verifica se buffer_pares não está vazio
        buffer_ROL = [buffer_pares[0][1], buffer_pares[0][0]]
        print("Valores no buffer:", buffer_ROL)


