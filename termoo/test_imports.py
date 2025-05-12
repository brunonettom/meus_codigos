import pygame
import asyncio
import sys

# Pygbag metadata - using Python comments for compatibility
# /// script
# dependencies = [
#     "wordfreq"
# ]
# ///

async def main():
    """Test importing external libraries with Pygbag"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Import Test")
    
    font = pygame.font.SysFont(None, 32)
    clock = pygame.time.Clock()
    
    # Results of import tests
    import_results = []
    
    # Test imports
    try:
        import wordfreq
        import_results.append("wordfreq: SUCCESS")
    except Exception as e:
        import_results.append(f"wordfreq: FAILED - {str(e)}")
    
    try:
        from wordfreq import word_frequency
        result = word_frequency('test', 'en')
        import_results.append(f"wordfreq.word_frequency: SUCCESS - test={result}")
    except Exception as e:
        import_results.append(f"wordfreq.word_frequency: FAILED - {str(e)}")
        
    # Try to create a minimal collection of words
    words = ["test", "game", "play", "code", "word"]
    import_results.append(f"Basic words array: {words}")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        
        # Display platform info
        platform_text = font.render(f"Platform: {sys.platform}", True, (0, 0, 0))
        screen.blit(platform_text, (20, 20))
        
        # Display import test results
        for i, result in enumerate(import_results):
            text = font.render(result, True, (0, 0, 0))
            screen.blit(text, (20, 70 + i*40))
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
