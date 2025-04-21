# import csv
# from collections import Counter
# import time

# def analisa_arquivo(nome_arquivo='palavras_aleatorias.csv'):
#     try:
#         with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
#             leitor = csv.reader(arquivo)
#             next(leitor, None)  # Pula o cabeçalho
            
#             palavras = [linha[0].strip() for linha in leitor if linha]
            
#             total_palavras = len(palavras)
#             contagem = Counter(palavras)
            
#             # Palavras que aparecem mais de uma vez
#             palavras_repetidas = [p for p, c in contagem.items() if c > 1]
#             total_repetidas = len(palavras_repetidas)
            
#             print(f"Total de palavras no arquivo: {total_palavras}")
#             print(f"Quantidade de palavras repetidas: {total_repetidas}")
#             print(f"Porcentagem de palavras repetidas: {total_repetidas / total_palavras * 100:.2f}%")
            
#             # Opcional: mostrar as palavras repetidas e suas quantidades
#             # for p in palavras_repetidas:
#             #     print(f"{p}: {contagem[p]} vezes")
            
#     except FileNotFoundError:
#         print(f"Arquivo '{nome_arquivo}' não encontrado.")
#     except Exception as e:
#         print(f"Erro ao analisar o arquivo: {e}")

# if __name__ == "__main__":
#     while True:
#         # try:
#         analisa_arquivo()
#         time.sleep(1)
#         #     break
#         # except KeyboardInterrupt:
#         #     print("Interrompido pelo usuário.")
#         #     break
#         # except Exception as e:
#         #     print(f"Erro inesperado: {e}")
#     #analisa_arquivo()


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
    plt.clf()  # Limpa o gráfico anterior
    plt.plot(historico, marker='o', linestyle='-', color='blue')
    plt.title('Evolução da porcentagem de palavras repetidas')
    plt.xlabel('Execuções')
    plt.ylabel('Porcentagem de repetição (%)')
    plt.ylim(0, 100)
    plt.grid(True)
    plt.pause(0.1)  # Pausa para atualizar o gráfico

def analisa_arquivo(nome_arquivo='palavras_aleatorias.csv'):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            leitor = csv.reader(arquivo)
            next(leitor, None)  # Pula o cabeçalho
            
            palavras = [linha[0].strip() for linha in leitor if linha]
            
            total_palavras = len(palavras)
            contagem = Counter(palavras)
            
            palavras_repetidas = [p for p, c in contagem.items() if c > 1]
            total_repetidas = len(palavras_repetidas)
            
            porcentagem = (total_repetidas / total_palavras * 100) if total_palavras > 0 else 0
            
            print(f"Total de palavras no arquivo: {total_palavras}")
            print(f"Quantidade de palavras repetidas: {total_repetidas}")
            print(f"Porcentagem de palavras repetidas: {porcentagem:.2f}%")
            
            salvar_historico(porcentagem)
            return porcentagem
            
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao analisar o arquivo: {e}")
        return None

if __name__ == "__main__":
    plt.ion()  # Modo interativo ligado para atualização do gráfico
    historico = carregar_historico()
    plotar_grafico(historico)
    
    try:
        while True:
            porcentagem = analisa_arquivo()
            if porcentagem is not None:
                historico = carregar_historico()
                plotar_grafico(historico)
            time.sleep(1)  # Aguarda 1 segundo antes da próxima análise
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
        plt.ioff()
        plt.show()
