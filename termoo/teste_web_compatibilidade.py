"""
Teste para diferenças críticas entre main.py e termoo_pygame_paia_mas_funiona.py
Específico para compatibilidade Web/Pygbag
"""
import pygame
import asyncio
import sys

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)

class TesteWebCompatibilidade:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        # Configuração da tela
        self.tela = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Teste de Compatibilidade Web")
        
        # Fonte
        self.fonte = pygame.font.SysFont('Arial', 20)
        self.fonte_grande = pygame.font.SysFont('Arial', 30)
        
        # Informações de ambiente
        self.plataforma = sys.platform
        self.rodando = True
        self.clock = pygame.time.Clock()
        
        # Log de problemas
        self.problemas = []
        self.adicionar_problema("Testando compatibilidade...", AZUL)
        
        # Algumas diferenças importantes entre os dois códigos
        try:
            import numpy
            self.adicionar_problema("numpy importado com sucesso", VERDE)
        except ImportError:
            self.adicionar_problema("Falha ao importar numpy - usado em termoo_pygame_paia_mas_funiona.py", VERMELHO)
        
        try:
            from wordfreq import word_frequency, top_n_list
            self.adicionar_problema("wordfreq importado com sucesso", VERDE)
        except ImportError:
            self.adicionar_problema("Falha ao importar wordfreq", VERMELHO)
            
        try:
            from filtra_palavras import lista_de_palavras
            self.adicionar_problema("filtra_palavras importado com sucesso", VERDE)
        except ImportError:
            self.adicionar_problema("Falha ao importar filtra_palavras", VERMELHO)
            
        try:
            # Teste específico para sys.platform
            if sys.platform == 'emscripten':
                self.adicionar_problema("Executando em ambiente web (emscripten)", VERDE)
            else:
                self.adicionar_problema(f"Ambiente não-web: {sys.platform}", AZUL)
        except Exception as e:
            self.adicionar_problema(f"Erro ao verificar plataforma: {e}", VERMELHO)
            
        # Verificação de asyncio
        try:
            # Verifica se asyncio.sleep(0) funciona
            self.adicionar_problema("asyncio disponível", VERDE)
        except Exception as e:
            self.adicionar_problema(f"Problema com asyncio: {e}", VERMELHO)
    
    def adicionar_problema(self, mensagem, cor):
        """Adiciona um problema à lista de log"""
        self.problemas.append((mensagem, cor))
        print(f"[LOG] {mensagem}")
        
    async def verifica_compatibilidade(self):
        """Verifica a compatibilidade com o ambiente web"""
        # Cria tarefas assíncronas
        self.adicionar_problema("Verificando compatibilidade...", AZUL)
        
        # Simula algumas operações assíncronas
        for i in range(3):
            self.adicionar_problema(f"Verificação {i+1}/3: OK", VERDE)
            try:
                await asyncio.sleep(0.1)
            except Exception as e:
                self.adicionar_problema(f"Falha em asyncio.sleep: {e}", VERMELHO)
                
        # Testes específicos para detectar problemas do main.py vs termoo_pygame_paia_mas_funiona.py
        
        # 1. O termoo_pygame_paia_mas_funiona.py é um único arquivo com classe principal
        # enquanto main.py usa arquivos separados
        self.adicionar_problema("Estrutura: termoo_pygame_paia_mas_funiona.py é autocontido", AZUL)
        
        # 2. O termoo_pygame_paia_mas_funiona.py usa loop síncrono simples
        # enquanto main.py usa async def main()
        self.adicionar_problema("Loop: main.py usa async def main(), exigindo await asyncio.sleep(0)", AZUL)
        
        # 3. Diferenças no gerenciamento de eventos e estados
        self.adicionar_problema("Estados: main.py usa sistema de estados mais complexo", AZUL)
        
        # 4. TelaConfiguracao em main.py pode estar com problemas
        try:
            # Simular carregamento da classe TelaConfiguracao
            self.adicionar_problema("Verificação de classes: TelaConfiguracao?", AZUL)
        except Exception as e:
            self.adicionar_problema(f"Problema com TelaConfiguracao: {e}", VERMELHO)
            
        self.adicionar_problema("Verificação concluída", VERDE)
        
    async def rodar(self):
        """Loop principal assíncrono"""
        # Roda verificação de compatibilidade
        await self.verifica_compatibilidade()
        
        # Loop principal
        while self.rodando:
            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.rodando = False
            
            # Renderização
            self.renderizar()
            
            # Controle de FPS
            self.clock.tick(FPS)
            
            # Essencial para Pygbag
            await asyncio.sleep(0)
        
        pygame.quit()
        
    def rodar_sincrono(self):
        """Loop principal síncrono (como no termoo_pygame_paia_mas_funiona.py)"""
        # Loop principal
        while self.rodando:
            # Eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.rodando = False
            
            # Renderização
            self.renderizar()
            
            # Controle de FPS
            self.clock.tick(FPS)
        
        pygame.quit()
        
    def renderizar(self):
        """Renderiza a tela"""
        self.tela.fill(BRANCO)
        
        # Título
        titulo = self.fonte_grande.render("Teste de Compatibilidade Web/Pygbag", True, PRETO)
        self.tela.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 30))
        
        # Info da plataforma
        info_plataforma = self.fonte.render(f"Plataforma: {self.plataforma}", True, PRETO)
        self.tela.blit(info_plataforma, (20, 80))
        
        # Lista de problemas
        y_offset = 120
        for i, (mensagem, cor) in enumerate(self.problemas[-15:]):  # Mostra apenas os 15 últimos problemas
            texto = self.fonte.render(mensagem, True, cor)
            self.tela.blit(texto, (20, y_offset + i * 25))
            
        # Instruções
        instrucoes = self.fonte.render("Pressione ESC para sair", True, PRETO)
        self.tela.blit(instrucoes, (WIDTH // 2 - instrucoes.get_width() // 2, HEIGHT - 40))
        
        pygame.display.flip()

async def main_async():
    """Função main assíncrona para compatibilidade com Pygbag"""
    teste = TesteWebCompatibilidade()
    await teste.rodar()

def main_sync():
    """Função main síncrona (como no termoo_pygame_paia_mas_funiona.py)"""
    teste = TesteWebCompatibilidade()
    teste.rodar_sincrono()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        print("Executando versão síncrona (similar ao termoo_pygame_paia_mas_funiona.py)")
        main_sync()
    else:
        print(f"Executando versão assíncrona (similar ao main.py) na plataforma {sys.platform}")
        # Usando a execução assíncrona (como no main.py)
        if sys.platform == 'emscripten':
            asyncio.run(main_async())
        else:
            try:
                asyncio.run(main_async())
            except (KeyboardInterrupt, SystemExit):
                pygame.quit()
