"""
Módulo simples para filtrar palavras com base em dificuldade.
Este é um arquivo de fallback para o jogo Termoo.
"""

def lista_de_palavras(dificuldade=0.5):
    """
    Retorna uma lista de palavras com base na dificuldade.
    
    Args:
        dificuldade: um valor de 0 a 1, onde 1 é mais difícil
        
    Returns:
        Uma lista de palavras
    """
    # Lista básica de palavras em português
    palavras = ["abrir", "agora", "amigo", "campo", "carro", "chuva", "dente", "doido", 
               "festa", "filho", "frase", "gente", "humor", "idade", "ideia", "jovem", 
               "limpo", "março", "mundo", "natal", "norte", "papel", "pedra", "plano", 
               "praia", "preto", "prima", "quase", "radio", "roupa", "saude", "sonho", 
               "tempo", "terra", "texto", "times", "treino", "verde", "viver", "zumbi"]
    
    # Palavras mais difíceis
    palavras_dificeis = ["advento", "alicerce", "ambíguo", "análogo", "cônjuge", 
                         "exceção", "esdrúxulo", "efêmero", "idílico", "análise", 
                         "sintaxe", "conciso", "empírico", "inerente", "perspicaz"]
    
    # Adiciona palavras difíceis com base no nível de dificuldade
    num_palavras_dificeis = int(len(palavras_dificeis) * dificuldade)
    palavras.extend(palavras_dificeis[:num_palavras_dificeis])
    
    return palavras