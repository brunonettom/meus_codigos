"""
Teste de importações para verificar compatibilidade com Pygbag
"""
import sys
print(f"Plataforma: {sys.platform}")

# Importações básicas
try:
    import pygame
    print("✓ Pygame importado com sucesso")
except ImportError as e:
    print(f"✗ Erro ao importar Pygame: {e}")

try:
    import asyncio
    print("✓ Asyncio importado com sucesso")
except ImportError as e:
    print(f"✗ Erro ao importar Asyncio: {e}")
    
# Teste de funções assíncronas básicas
try:
    async def teste_async():
        print("  Função assíncrona executada")
        await asyncio.sleep(0.1)
        return True
        
    # Executar função assíncrona
    if sys.platform != 'emscripten':
        # No ambiente desktop
        print("Testando execução assíncrona no desktop:")
        asyncio.run(teste_async())
    else:
        # No ambiente web (emscripten)
        print("Detectado ambiente web (emscripten)")
        # No ambiente web seria executado de forma diferente
        print("A execução assíncrona funciona diferente no navegador")
    
    print("✓ Funções assíncronas testadas com sucesso")
except Exception as e:
    print(f"✗ Erro no teste de funções assíncronas: {e}")

# Loop principal simplificado (similar ao termoo_pygame_paia_mas_funiona.py)
async def main_simples():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
        tela.fill((0, 0, 0))
        pygame.display.flip()
        await asyncio.sleep(0)
    pygame.quit()

# Loop principal com estados (similar ao main.py)
async def main_estados():
    pygame.init()
    tela = pygame.display.set_mode((800, 600))
    estado = "inicial"
    rodando = True
    clock = pygame.time.Clock()
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
        tela.fill((0, 0, 0))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
    pygame.quit()

print("\nPara testar cada versão do loop principal, descomente a linha correspondente no final deste arquivo.")

# Descomente uma das linhas abaixo para testar
# if __name__ == "__main__":
#     if sys.platform == 'emscripten':
#         asyncio.run(main_simples())
#     else:
#         asyncio.run(main_simples())

# if __name__ == "__main__":
#     if sys.platform == 'emscripten':
#         asyncio.run(main_estados())
#     else:
#         asyncio.run(main_estados())
