import pygame
import sys
import random
import unicodedata
import os
import asyncio

# Metadados para Pygbag no formato correto
# __PYGBAG_SCRIPT_BEGIN__
dependencies = [
    "wordfreq"
]
# __PYGBAG_SCRIPT_END__

# Tenta importar bibliotecas, com fallbacks para ambiente web
try:
    from wordfreq import word_frequency, top_n_list
    wordfreq_disponivel = True
    print("Wordfreq importado com sucesso")
except ImportError:
    wordfreq_disponivel = False
    print("Wordfreq não disponível, usando fallback")

# Palavras padrão caso outras fontes falhem
PALAVRAS_PADRAO = ["abrir", "agora", "amigo", "campo", "carro", "chuva", "dente", "doido", 
                 "festa", "filho", "frase", "gente", "humor", "idade", "ideia", "jovem", 
                 "limpo", "marco", "mundo", "natal", "norte", "papel", "pedra", "plano", 
                 "praia", "preto", "prima", "quase", "radio", "roupa", "saude", "sonho", 
                 "tempo", "terra", "texto", "times", "treino", "verde", "viver", "zumbi"]

# Função para obter as palavras
def obter_palavras(dificuldade=0.5):
    if wordfreq_disponivel:
        try:
            # Tenta usar wordfreq
            palavras = top_n_list('pt', 10000)
            return palavras
        except Exception as e:
            print(f"Erro ao usar wordfreq: {e}")
    
    # Fallback para as palavras padrão
    return PALAVRAS_PADRAO

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 180, 0)
AMARELO = (255, 200, 0)
CINZA_CLARO = (230, 230, 230)
CINZA_ESCURO = (80, 80, 80)
VERMELHO = (220, 0, 0)
AZUL = (50, 120, 220)

# Fontes
FONTE_PRINCIPAL = pygame.font.SysFont("Arial", 24)
FONTE_GRANDE = pygame.font.SysFont("Arial", 36, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 18)
FONTE_MUITO_PEQUENA = pygame.font.SysFont("Arial", 14)

# Variáveis globais para tela cheia
TELA_CHEIA = False
TAMANHO_JANELA = (800, 600)

# Função para alternar modo de tela cheia
def alternar_tela_cheia():
    global TELA_CHEIA
    TELA_CHEIA = not TELA_CHEIA
    if TELA_CHEIA:
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        return pygame.display.set_mode(TAMANHO_JANELA)

class TelaConfiguracao:
    # ...existing code...
    pass

class TermooPygame:
    """Classe principal do jogo Termoo com interface Pygame."""
    
    def __init__(self, config):
        """Inicializa o jogo com as configurações fornecidas."""
        # Configurações do jogo
        self.num_palavras = config["num_palavras"]
        self.num_letras = config["num_letras"]
        self.num_tentativas = config["num_tentativas"]
        self.dificuldade = config["dificuldade"]
        self.modo_trapaca = config["modo_trapaca"]
        
        # Configurações da tela
        self.tela = pygame.display.get_surface()  # Usa a superfície já criada
        self.largura_tela, self.altura_tela = self.tela.get_size()
        pygame.display.set_caption("Termoo")
        
        # Carrega dicionários - com tratamento especial para web
        if wordfreq_disponivel:
            try:
                self.dicionario_pt = top_n_list('pt', 10000)
            except Exception:
                self.dicionario_pt = PALAVRAS_PADRAO
        else:
            self.dicionario_pt = PALAVRAS_PADRAO
            
        self.palavras_possiveis = self._carregar_palavras_possiveis()
        
        # ...existing code...
    
    def _carregar_palavras_possiveis(self):
        """Carrega e filtra palavras possíveis para o jogo."""
        try:
            palavras = obter_palavras(self.dificuldade)
            # Filtra palavras pelo tamanho
            return [p for p in palavras if len(p) == self.num_letras and ' ' not in p and '-' not in p]
        except Exception as e:
            print(f"Erro ao carregar palavras: {e}")
            # Fallback para um conjunto básico de palavras
            return [p for p in PALAVRAS_PADRAO if len(p) == self.num_letras]
            
    # ...existing code...

# Função principal modificada para compatibilidade com Pygbag
async def main():
    """Função principal do jogo com compatibilidade para Pygbag."""
    pygame.init()
    pygame.font.init()
    
    # Tamanho inicial da tela
    tela = pygame.display.set_mode(TAMANHO_JANELA, pygame.RESIZABLE)
    pygame.display.set_caption("Termoo")
    
    # Configura para ambiente web se necessário
    if sys.platform == 'emscripten':
        import platform
        # Configuração específica para web
        platform.window.canvas.style.imageRendering = "pixelated"
        print("Executando no navegador via Pygbag")
        
        # Em dispositivos móveis, pode ser interessante ajustar o tamanho
        if platform.window.innerWidth < 600:
            tela = pygame.display.set_mode((320, 480), pygame.RESIZABLE)
    
    # Estados do jogo
    estado_atual = "configuracao"
    tela_config = TelaConfiguracao(tela)
    jogo = None
    
    # Loop principal do jogo
    clock = pygame.time.Clock()
    rodando = True
    
    # Adiciona instruções no console
    if sys.platform != 'emscripten':
        print("Pressione F11 ou Alt+Enter para alternar entre modo janela e tela cheia")
    
    while rodando:
        if estado_atual == "configuracao":
            resultado = tela_config.processar_eventos()
            if resultado["acao"] == "sair":
                rodando = False
            elif resultado["acao"] == "iniciar_jogo":
                jogo = TermooPygame(resultado["config"])
                estado_atual = "jogo"
            
            tela_config.renderizar()
        
        elif estado_atual == "jogo":
            resultado = jogo.processar_eventos()
            if resultado == "sair":
                rodando = False
            elif resultado == "reiniciar":
                estado_atual = "configuracao"
                tela = pygame.display.get_surface()  # Obter a superfície atual
                tela_config = TelaConfiguracao(tela)
            
            jogo.renderizar()
        
        # Limita a quantidade de frames por segundo
        clock.tick(60)
        
        # Para compatibilidade com Pygbag
        await asyncio.sleep(0)

# Ponto de entrada para execução
asyncio.run(main())
