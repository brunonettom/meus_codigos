import unicodedata
from wordfreq import word_frequency, top_n_list
from lista_unificada_20_04_2025__20_32 import palavras  # Sua lista de palavras


def normalizar(palavra):
    norm_txt = unicodedata.normalize('NFKD', palavra).lower()
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)

def tira_espacos(palavras):
    return [palavra for palavra in palavras if " "not in palavra]

def eh_ingles(palavra, frequencia_min=1e-6):
    return word_frequency(palavra, 'en') > frequencia_min

def escolhe_palavras(palavras, mais_comuns=True,porcentagem_do_topo=0.8):

    palavras_ptbr = [palavra for palavra in palavras if not eh_ingles(palavra)]

    palavras_sem_espaco=tira_espacos(palavras_ptbr)
    
    #n de escolhidos
    n_total=len(top_n_list('pt', 100000))
    n_de_escolhidos=int(n_total*porcentagem_do_topo)

    topo_normalizado = set(normalizar(p) for p in top_n_list('pt', n_de_escolhidos))

    if mais_comuns:
        palavras_escolhidas = [palavra for palavra in palavras_sem_espaco if palavra in topo_normalizado]
    else:
        palavras_escolhidas = [palavra for palavra in palavras_sem_espaco if palavra not in topo_normalizado]

    return palavras_escolhidas


def lista_de_palavras(dificuldade):
    return escolhe_palavras(palavras, mais_comuns=True, porcentagem_do_topo=dificuldade)

# print(palavras_escolhidas, len(palavras_escolhidas))