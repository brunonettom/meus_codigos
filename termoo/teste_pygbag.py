"""
Teste específico para identificar problemas no main.py para compatibilidade com Pygbag
"""
import pygame
import sys
import asyncio

# Constantes
WIDTH, HEIGHT = 800, 600
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)

# Função para simular o alternar_tela_cheia que pode estar causando problemas no Pygbag
def alternar_tela_cheia_compativel():
    """Versão compatível com Pygbag da função alternar_tela_cheia"""
    global tela_cheia
    tela_cheia = not tela_cheia
    
    # Em Pygbag, FULLSCREEN pode causar problemas
    if tela_cheia and sys.platform != 'emscripten':
        return pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        # No navegador, sempre retornamos para o modo janela de tamanho fixo
        return pygame.display.set_mode((WIDTH, HEIGHT))

async def main():
    """Função principal para testar comportamentos específicos"""
    global tela_cheia
    tela_cheia = False
    
    pygame.init()
    pygame.font.init()
    
    # Inicialização da tela
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Teste Compatibilidade Pygbag")
    
    # Fonte
    font = pygame.font.SysFont("Arial", 24)
    
    # Status de testes
    testes = [
        {"nome": "Importação Pygame", "status": "OK"},
        {"nome": "Renderização básica", "status": "OK"},
        {"nome": "Eventos de teclado", "status": "Testando..."},
        {"nome": "Alternar tela cheia", "status": "Não testado"},
        {"nome": "wordfreq & filtra_palavras", "status": "Não testado"}
    ]
    
    # Loop principal
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                testes[2]["status"] = "OK"
                
                if event.key == pygame.K_f:
                    # Testar alternar tela cheia
                    try:
                        screen = alternar_tela_cheia_compativel()
                        testes[3]["status"] = "OK"
                    except Exception as e:
                        testes[3]["status"] = f"FALHA: {str(e)}"
                
                elif event.key == pygame.K_w:
                    # Testar importação de wordfreq e filtra_palavras
                    try:
                        from wordfreq import top_n_list
                        from filtra_palavras import lista_de_palavras
                        testes[4]["status"] = "OK"
                    except Exception as e:
                        testes[4]["status"] = f"FALHA: {str(e)}"
        
        # Renderização
        screen.fill(BRANCO)
        
        # Título
        title = font.render("Teste de Compatibilidade com Pygbag", True, PRETO)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
        # Instruções
        instrucoes = [
            "Pressione F para testar tela cheia",
            "Pressione W para testar wordfreq e filtra_palavras",
            "Pressione ESC para sair"
        ]
        
        y = 100
        for instrucao in instrucoes:
            text = font.render(instrucao, True, PRETO)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 30
        
        # Status dos testes
        y = 200
        for teste in testes:
            nome = teste["nome"]
            status = teste["status"]
            
            cor = PRETO
            if status == "OK":
                cor = VERDE
            elif status.startswith("FALHA"):
                cor = (255, 0, 0)
            
            text = font.render(f"{nome}: {status}", True, cor)
            screen.blit(text, (50, y))
            y += 30
        
        pygame.display.flip()
        clock.tick(60)
        
        # Crucial para Pygbag
        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    if sys.platform == 'emscripten':
        asyncio.run(main())
    else:
        asyncio.run(main())
