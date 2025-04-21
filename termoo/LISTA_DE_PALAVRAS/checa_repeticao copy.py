import csv
from collections import Counter
import time
import json
import os
import matplotlib.pyplot as plt

HISTORICO_ARQUIVO = 'historico_repeticoes.json'

def salvar_historico(porcentagem):
    historico = []
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, 'r', encoding='utf-8') as f:
            try:
                historico = json.load(f)
            except json.JSONDecodeError:
                historico = []
    historico.append(porcentagem)
    with open(HISTORICO_ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(historico, f)

def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def plotar_grafico(historico):
    plt.clf()
    plt.plot(historico, marker='o', linestyle='-', color='blue')
    plt.title('Evolução da porcentagem de palavras repetidas')
    plt.xlabel('Execuções')
    plt.ylabel('Porcentagem de repetição (%)')
    plt.ylim(0, 100)
    plt.grid(True)
    plt.pause(0.1)

def analisa_arquivo(nome_arquivo='palavras_aleatorias.csv'):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor, None)

            palavras = [linha[0].strip() for linha in leitor if linha]
            total_palavras = len(palavras)
            contagem = Counter(palavras)

            # Calcula o total de repetições (quantas vezes a mais cada palavra apareceu)
            total_ocorrencias_repetidas = sum(c - 1 for c in contagem.values() if c > 1)

            porcentagem = (total_ocorrencias_repetidas / total_palavras * 100) if total_palavras > 0 else 0

            print(f"Total de palavras no arquivo: {total_palavras}")
            print(f"Total de repetições (ocorrências extras): {total_ocorrencias_repetidas}")
            print(f"Porcentagem de repetições: {porcentagem:.2f}%")

            salvar_historico(porcentagem)
            return porcentagem

    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao analisar o arquivo: {e}")
        return None

if __name__ == "__main__":
    plt.ion()
    historico = carregar_historico()
    plotar_grafico(historico)

    try:
        while True:
            porcentagem = analisa_arquivo()
            if porcentagem is not None:
                historico = carregar_historico()
                plotar_grafico(historico)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        plt.ioff()
        plt.show()
