#!/usr/bin/env python3
import os
import unicodedata
from datetime import datetime

def normalizar(txt):
    """Remove acentos e transforma letras maiúsculas em minúsculas."""
    norm_txt = unicodedata.normalize('NFKD', txt).lower()
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)

# Função principal para processar o arquivo de palavras
def processar_palavras(arquivo_entrada, arquivo_saida):
    palavras = []

    # Verifica se o arquivo de entrada existe
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
        return

    # Lê o arquivo de entrada e processa as palavras
    with open(arquivo_entrada, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            palavra = linha.strip()  # Remove espaços e quebras de linha
            if palavra:  # Verifica se a palavra não está vazia
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

# Caminho dos arquivos

arquivo_entrada = 'C:/Users/BrunoLocal.BRUNO-note.000/Downloads/x/CÓDIGOS/termoo//LISTA/palavras_aleatorias_2.csv'  # Substitua pelo caminho correto
current_time = datetime.now()
formatted_time = current_time.strftime("%d_%m_%Y__%H_%M")
arquivo_saida = f'C:/Users/BrunoLocal.BRUNO-note.000/Downloads/x/CÓDIGOS/termoo/palavras_aleatorias_{formatted_time}.txt'

# Executa a função principal
processar_palavras(arquivo_entrada, arquivo_saida)
