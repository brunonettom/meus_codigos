"""
Teste da estrutura básica da tela de configuração e loop principal
Baseado na análise de main.py vs termoo_pygame_paia_mas_funiona.py
"""
import pygame
import sys
import asyncio

# Constantes simples
WIDTH, HEIGHT = 800, 600
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# Classe simplificada de configuração (similar ao main.py)
class TelaConfiguracao:
    def __init__(self, tela):
        self.tela = tela
        self.fonte = pygame.font.SysFont('Arial', 24)
        self.configuracoes = {
            "num_palavras": 4,
            "dificuldade": 50,
            "num_letras": 5,
            "num_tentativas": 9,
            "trapaca": False
        }
        
    def processar_eventos(self):
        """Processa eventos da tela de configuração"""
        resultado = {"acao": "continuar"}
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                resultado = {"acao": "sair"}
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    # Simula iniciar o jogo após pressionar Enter
                    resultado = {
                        "acao": "iniciar_jogo", 
                        "config": self.configuracoes
                    }
                elif evento.key == pygame.K_ESCAPE:
                    resultado = {"acao": "sair"}
        
        return resultado
    
    def renderizar(self):
        """Renderiza a tela de configuração"""
        self.tela.fill(BRANCO)
        texto = self.fonte.render("TELA DE CONFIGURAÇÃO - Pressione ENTER para começar", True, PRETO)
        self.tela.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

# Classe simplificada do jogo (similar ao TermooPygame no main.py)
class Jogo:
    def __init__(self, tela, config):
        self.tela = tela
        self.config = config
        self.fonte = pygame.font.SysFont('Arial', 24)
        self.rodando = True
    
    def processar_eventos(self):
        """Processa eventos do jogo"""
        resultado = "continuar"
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                resultado = "sair"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    resultado = "sair"
                elif evento.key == pygame.K_r:
                    resultado = "reiniciar"
        
        return resultado
    
    def renderizar(self):
        """Renderiza o jogo"""
        self.tela.fill(AZUL)
        texto = self.fonte.render("TELA DO JOGO - ESC para sair, R para reiniciar", True, BRANCO)
        self.tela.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

# Versão assíncrona (compatível com Pygbag, similar ao main.py)
async def main_async():
    pygame.init()
    pygame.font.init()
    
    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Teste - Versão Assíncrona")
    
    estado_atual = "configuracao"
    tela_config = TelaConfiguracao(tela)
    jogo = None
    
    clock = pygame.time.Clock()
    rodando = True
    
    print("Iniciando loop principal assíncrono...")
    
    while rodando:
        if estado_atual == "configuracao":
            resultado = tela_config.processar_eventos()
            if resultado["acao"] == "sair":
                rodando = False
            elif resultado["acao"] == "iniciar_jogo":
                jogo = Jogo(tela, resultado["config"])
                estado_atual = "jogo"
            
            tela_config.renderizar()
        
        elif estado_atual == "jogo":
            resultado = jogo.processar_eventos()
            if resultado == "sair":
                rodando = False
            elif resultado == "reiniciar":
                estado_atual = "configuracao"
                tela = pygame.display.get_surface()
                tela_config = TelaConfiguracao(tela)
            
            jogo.renderizar()
        
        # Limita a quantidade de frames por segundo
        clock.tick(60)
        
        # Crucial para compatibilidade com Pygbag
        await asyncio.sleep(0)
    
    pygame.quit()
    print("Loop principal encerrado")

# Versão síncrona (similar ao termoo_pygame_paia_mas_funiona.py)
def main_sync():
    pygame.init()
    pygame.font.init()
    
    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Teste - Versão Síncrona")
    
    # Estado inicial é a configuração
    tela_config = TelaConfiguracao(tela)
    jogo = None
    estado_atual = "configuracao"
    
    clock = pygame.time.Clock()
    rodando = True
    
    print("Iniciando loop principal síncrono...")
    
    while rodando:
        if estado_atual == "configuracao":
            resultado = tela_config.processar_eventos()
            if resultado["acao"] == "sair":
                rodando = False
            elif resultado["acao"] == "iniciar_jogo":
                jogo = Jogo(tela, resultado["config"])
                estado_atual = "jogo"
            
            tela_config.renderizar()
        
        elif estado_atual == "jogo":
            resultado = jogo.processar_eventos()
            if resultado == "sair":
                rodando = False
            elif resultado == "reiniciar":
                estado_atual = "configuracao"
                tela = pygame.display.get_surface()
                tela_config = TelaConfiguracao(tela)
            
            jogo.renderizar()
        
        # Limita a quantidade de frames por segundo
        clock.tick(60)
    
    pygame.quit()
    print("Loop principal encerrado")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        print("Executando versão síncrona (similar ao termoo_pygame_paia_mas_funiona.py)")
        main_sync()
    else:
        print("Executando versão assíncrona (similar ao main.py)")
        try:
            asyncio.run(main_async())
        except (KeyboardInterrupt, SystemExit):
            pygame.quit()
            print("Programa encerrado pelo usuário")
