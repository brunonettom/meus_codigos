#!/usr/bin/env python3

import unicodedata
from datetime import datetime
from palavras_aleatorias_20_04_2025__19_56 import palavras_2 as lista1
from listaDePalavrasFinal_01_12_2024__22_28 import palavras as lista2
from palavras_aleatorias_20_04_2025__20_13 import palavras as lista3

# Função que remove acentos e transforma em minúsculas
#!/usr/bin/env python3

import unicodedata
from datetime import datetime

# Função que remove acentos e transforma em minúsculas
def normalizar(txt):
    norm_txt = unicodedata.normalize('NFKD', txt).lower()
    return ''.join(c for c in norm_txt if not unicodedata.combining(c))



def processar_listas(lista_de_listas, arquivo_saida):
    palavras = []

    # Junta todas as listas em uma só e processa as palavras
    for sublista in lista_de_listas:
        for palavra in sublista:
            palavra = palavra.strip()
            if palavra:
                palavra_normalizada = normalizar(palavra)
                palavras.append(palavra_normalizada)

    # Remove duplicatas e ordena
    palavras = sorted(set(palavras))

    # Salva a lista em um novo arquivo no formato desejado
    with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
        arquivo.write(' = [')
        for i, palavra in enumerate(palavras):
            if i < len(palavras) - 1:
                arquivo.write(f'"{palavra}", ')
            else:
                arquivo.write(f'"{palavra}"')
        arquivo.write(']')

    print(f'Total de palavras processadas: {len(palavras)}')
    print(f'Arquivo "{arquivo_saida}" criado com sucesso!')

# Suponha que você tenha várias listas
# Nome do arquivo de saída com data/hora
current_time = datetime.now().strftime("%d_%m_%Y__%H_%M")
arquivo_saida = f'C:/Users/BrunoLocal.BRUNO-note.000/Downloads/x/CÓDIGOS/termoo/lista_unificada_{current_time}.py'

# Chamada da função
processar_listas([lista1, lista2, lista3], arquivo_saida)

