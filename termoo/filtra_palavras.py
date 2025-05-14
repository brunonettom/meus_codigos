"""
Módulo simples para filtrar palavras com base em dificuldade.
Este é um arquivo de fallback para o jogo Termoo.
"""

from wordfreq import word_frequency

def lista_de_palavras(dificuldade=0.5):
    """
    Retorna uma lista de palavras filtrada por dificuldade.
    
    Args:
        dificuldade (float): Valor entre 0 e 1, onde 0 são palavras mais comuns
                             e 1 são palavras mais raras.
                             
    Returns:
        list: Lista de palavras filtradas por dificuldade
    """
    from lista_unificada_20_04_2025__20_32 import palavras
    
    if dificuldade <= 0:
        return palavras[:int(len(palavras) * 0.1)]  # 10% mais comuns
    elif dificuldade >= 1:
        return palavras[int(len(palavras) * 0.9):]  # 10% mais raras
    else:
        # Calcula índice com base na dificuldade
        indice_corte = int(len(palavras) * dificuldade)
        return palavras[:indice_corte]